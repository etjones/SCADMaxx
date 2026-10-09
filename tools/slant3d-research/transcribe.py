"""Resumable local speech transcription of the acquired Slant 3D corpus.

Run with uv run --with faster-whisper==1.2.1 --with av==18.1.0 python transcribe.py --watch.
This produces timestamped evidence; it does not review or validate design claims.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import time
import traceback

RUN = Path("D:/openscad/runs/slant3d-design-research-20261009")
ARCHIVE = Path("D:/openscad/artifacts/slant3d-research")


def atomic_json(target: Path, value: object) -> None:
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small.en")
    parser.add_argument("--device", default="cuda", choices=("cuda", "cpu"))
    parser.add_argument("--compute-type", default="int8_float16")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--include-captioned", action="store_true")
    parser.add_argument("--id", action="append", dest="ids")
    args = parser.parse_args()

    runtime = ARCHIVE / "runtime"
    dll_handles = []
    if os.name == "nt" and runtime.exists():
        os.environ["PATH"] = str(runtime) + os.pathsep + os.environ["PATH"]
        dll_handles.append(os.add_dll_directory(str(runtime)))

    from faster_whisper import BatchedInferencePipeline, WhisperModel

    entries = json.loads((RUN / "videos.json").read_text(encoding="utf-8-sig"))
    by_id = {entry["id"]: entry for entry in entries}
    priority = [line.rsplit("=", 1)[-1] for line in
                (RUN / "design-video-urls.txt").read_text(encoding="utf-8-sig").splitlines()]
    rank = {video_id: index for index, video_id in enumerate(priority)}
    output = ARCHIVE / "speech-transcripts" / args.model
    output.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"event": "loading-model", "model": args.model, "device": args.device}), flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type,
                         download_root=str(ARCHIVE / "models"), cpu_threads=4, num_workers=1)
    pipeline = BatchedInferencePipeline(model=model)
    failed: dict[str, float] = {}
    while True:
        if (RUN / "STOP-TRANSCRIPTION").exists():
            print("Stop marker found; retained completed transcripts.", flush=True)
            return
        candidates = {}
        for folder in ("audio", "media"):
            for source in (ARCHIVE / folder).glob("*.opus"):
                video_id = source.stem
                if video_id not in by_id or (args.ids and video_id not in args.ids):
                    continue
                if source.stat().st_size == 0 or time.time() - source.stat().st_mtime < 60:
                    continue  # Do not decode a file that the extractor is still writing.
                if (output / (video_id + ".json")).exists():
                    continue
                if not args.include_captioned and (ARCHIVE / "transcripts" / (video_id + ".txt")).exists():
                    continue
                if time.time() - failed.get(video_id, 0) < 1800:
                    continue
                candidates[video_id] = source
        def order(video_id: str) -> tuple:
            caption_exists = (ARCHIVE / "transcripts" / (video_id + ".txt")).exists()
            entry = by_id[video_id]
            non_design = any(word in entry['title'].lower() for word in ('podcast', 'printing news', 'interview'))
            return (video_id not in rank, caption_exists, rank.get(video_id, 9999),
                    non_design, not bool(entry.get('topics')), entry.get('duration') or 60)
        ids = sorted(candidates, key=order)
        if not ids:
            atomic_json(RUN / "speech-transcription-status.json", {
                "updated": time.time(), "model": args.model, "state": "waiting" if args.watch else "finished-current-files",
                "completed": len(list(output.glob("*.json"))), "failed_ids": list(failed),
                "review": "pending", "all_channel_complete": False,
            })
            if not args.watch:
                return
            time.sleep(20)
            continue
        video_id = ids[0]
        source = candidates[video_id]
        started = time.time()
        try:
            metadata = json.loads(source.with_suffix('.info.json').read_text(encoding='utf-8'))
            source_language = metadata.get('language')
            if source_language and not source_language.startswith('en'):
                raise ValueError(f'English source audio required; selected track is {source_language}')
            print(json.dumps({"event": "transcribing", "id": video_id, "title": by_id[video_id]["title"]}), flush=True)
            segments, info = pipeline.transcribe(str(source), language="en", beam_size=5, vad_filter=True,
                                                 batch_size=args.batch_size)
            rows = []
            text_path = output / (video_id + ".txt")
            partial_path = text_path.with_suffix(".txt.partial")
            with partial_path.open("w", encoding="utf-8") as stream:
                stream.write(f"{by_id[video_id]['title']}\nhttps://www.youtube.com/watch?v={video_id}\n"
                             f"Source: local audio ASR, faster-whisper {args.model}; review pending.\n\n")
                for segment in segments:
                    rows.append({"start": segment.start, "end": segment.end, "text": segment.text.strip(),
                                 "avg_logprob": segment.avg_logprob, "no_speech_prob": segment.no_speech_prob})
                    stream.write(f"[{segment.start:.2f}] {segment.text.strip()}\n")
                    stream.flush()
            partial_path.replace(text_path)
            atomic_json(output / (video_id + ".json"), {
                "id": video_id, "source_audio": str(source), "model": args.model,
                "device": args.device, "compute_type": args.compute_type,
                "batch_size": args.batch_size,
                "source_language": source_language, "source_format": metadata.get('format_id'),
                "duration_after_vad": info.duration_after_vad,
                "speech_seconds": sum(row['end'] - row['start'] for row in rows),
                "low_coverage": sum(row['end'] - row['start'] for row in rows) < info.duration * 0.2,
                "duration": info.duration, "language": info.language,
                "elapsed_seconds": time.time() - started, "review": "pending", "segments": rows,
            })
            atomic_json(RUN / "speech-transcription-status.json", {
                "updated": time.time(), "model": args.model, "state": "running", "last_id": video_id,
                "completed": len(list(output.glob("*.json"))), "failed_ids": list(failed),
                "review": "pending", "all_channel_complete": False,
            })
            print(json.dumps({"event": "completed", "id": video_id, "elapsed": round(time.time() - started, 2)}), flush=True)
        except Exception:
            failed[video_id] = time.time()
            (output / (video_id + ".error.txt")).write_text(traceback.format_exc(), encoding="utf-8")
            print(json.dumps({"event": "failed", "id": video_id}), flush=True)


if __name__ == "__main__":
    main()
