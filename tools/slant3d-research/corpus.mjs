// Local research bookkeeping. Acquisition is performed by yt-dlp and ffmpeg.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const run = 'D:/openscad/runs/slant3d-design-research-20261009';
const archive = 'D:/openscad/artifacts/slant3d-research';
const action = process.argv[2];
const read = p => JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const write = (p, s) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, s); };
const flatten = (item, tab = '') => item.entries
  ? item.entries.flatMap(x => flatten(x, item.title ?? tab))
  : [{ id: item.id, title: item.title, url: item.url, duration: item.duration ?? null, tab }];
const topics = [
  ['supports', /support|brim|raft|overhang|falling over|first layer|warp|ejection|diagonal/i],
  ['fits', /tolerance|grip fin|pins|rods|hole|magnet|inserts|thread|screw/i],
  ['mechanisms', /snap|hinge|spring|latch|joining|connect|loop|handle|bracket|gear/i],
  ['strength', /strong|strength|reinforce|ribs|truss|micro.?feature|thin|indestructible|cavit/i],
  ['finish', /surface|texture|layer line|shrink line|fillet|chamfer|curved|text for|designing text|domes|sphere/i],
  ['products', /design|redesign|enclosure|box|lid|drawer|vase|water.?resistant|waterproof|feet|vent|scoop|cube|deadly sins|stop pausing/i],
];

if (action === 'index') {
  const raw = read(path.join(run, 'channel-raw.json'));
  const entries = [...new Map(flatten(raw).map(x => [x.id, x])).values()];
  for (const item of entries) {
    item.topics = topics.filter(([, re]) => re.test(item.title)).map(([name]) => name);
    item.priority = item.tab.endsWith('Videos') && item.topics.length > 0
      && !/podcast|3d printing news|ep\.?\s*\d|financial|filament|industry|interview|\bCEO\b|STL theft|model theft|designers|CAD Software|AI tools|ChatGPT/i.test(item.title);
    item.review = 'pending';
  }
  write(path.join(run, 'videos.json'), JSON.stringify(entries, null, 2));
  write(path.join(run, 'all-audio-urls.txt'), entries.map(x => `https://www.youtube.com/watch?v=${x.id}`).join('\n') + '\n');
  const priority = entries.filter(x => x.priority);
  write(path.join(run, 'design-video-urls.txt'), priority.map(x => `https://www.youtube.com/watch?v=${x.id}`).join('\n') + '\n');
  write(path.join(run, 'inventory.md'), '# Slant 3D channel inventory\n\n'
    + `Captured 2026-10-09 from https://www.youtube.com/@slant3d. Channel ID: ${raw.channel_id}.\n\n`
    + `Unique entries: ${entries.length}. Priority design videos: ${priority.length}. All entries remain in the audio queue.\n`
    + 'Topic labels and priority are title-based acquisition aids, not evidence that a trick works or a completed review.\n\n'
    + '| ID | Tab | Title | Topics | Duration (s) | Review |\n| --- | --- | --- | --- | --- | --- |\n'
    + entries.map(x => `| [${x.id}](${x.url}) | ${x.tab} | ${x.title.replaceAll('|', '/')} | ${x.topics.join(', ')} | ${x.duration ?? 'unknown'} | pending |`).join('\n') + '\n');
  console.log(JSON.stringify({ entries: entries.length, priority: priority.length,
    tabs: [...new Set(entries.map(x => x.tab))].map(tab => ({ tab, count: entries.filter(x => x.tab === tab).length })),
    knownHours: entries.reduce((sum, x) => sum + (x.duration ?? 0), 0) / 3600 }));
} else if (action === 'transcripts') {
  const entries = read(path.join(run, 'videos.json'));
  const sources = ['audio', 'media'];
  for (const dir of sources) {
    for (const name of fs.readdirSync(path.join(archive, dir)).filter(x => x.endsWith('.en.json3'))) {
      const id = name.slice(0, -'.en.json3'.length);
      const raw = read(path.join(archive, dir, name));
      const lines = (raw.events ?? []).filter(x => x.segs).map(x => {
        const value = x.segs.map(s => s.utf8 ?? '').join('').replace(/\s+/g, ' ').trim();
        return value ? `[${(x.tStartMs / 1000).toFixed(2)}] ${value}` : '';
      }).filter(Boolean);
      const entry = entries.find(x => x.id === id);
      write(path.join(archive, 'transcripts', `${id}.txt`), `${entry?.title ?? id}\nhttps://www.youtube.com/watch?v=${id}\nSource: YouTube English captions; not independently transcribed audio.\n\n${lines.join('\n')}\n`);
    }
  }
  console.log(`${fs.readdirSync(path.join(archive, 'transcripts')).length} transcript files`);
} else if (action === 'read') {
  const speechMode = process.argv[3] === '--speech';
  for (const spec of process.argv.slice(speechMode ? 4 : 3)) {
    const [id, range] = spec.split('@');
    const [from, until] = range ? range.split(':').map(Number) : [0, Infinity];
    const file = path.join(archive, speechMode ? 'speech-transcripts/small.en' : 'transcripts', `${id}.txt`);
    if (!fs.existsSync(file)) { console.log(`${id}: transcript unavailable`); continue; }
    const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
    console.log(lines.slice(0, 3).join('\n'));
    let start = 0, text = '';
    for (const line of lines.slice(3)) {
      const match = /^\[([\d.]+)\] (.*)$/.exec(line);
      if (!match) continue;
      const seconds = Number(match[1]);
      if (seconds < from || seconds > until) continue;
      if (text && seconds - start >= 30) { console.log(`[${start.toFixed(1)}] ${text}`); text = ''; }
      if (!text) start = seconds;
      text += `${match[2]} `;
    }
    if (text) console.log(`[${start.toFixed(1)}] ${text}`);
  }
} else if (action === 'frame') {
  const [id, ...secondsList] = process.argv.slice(3);
  for (const seconds of secondsList) {
    const file = path.join(archive, 'frames', `${id}-${seconds.padStart(4, '0')}.png`);
    if (!fs.existsSync(file)) {
      const result = spawnSync('E:/Dropbox/bin/ffmpeg-6.1-full_build/bin/ffmpeg.exe',
        ['-hide_banner', '-loglevel', 'error', '-ss', seconds, '-i', path.join(archive, 'media', `${id}.mkv`),
         '-frames:v', '1', '-update', '1', file], { encoding: 'utf8' });
      if (result.status !== 0) throw new Error(result.stderr);
    }
    write(`${file}.json`, JSON.stringify({ id, seconds: Number(seconds),
      video: `media/${id}.mkv`, sha256: crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),
      review: 'pending' }, null, 2));
    console.log(file);
  }
} else if (action === 'extra-queue') {
  const entries = read(path.join(run, 'videos.json'));
  const ids = new Set(entries.map(x => x.id));
  const selected = process.argv.slice(3);
  for (const id of selected) if (!ids.has(id)) throw new Error(`Uninventoried video: ${id}`);
  write(path.join(run, 'extra-video-urls.txt'), selected.map(id => `https://www.youtube.com/watch?v=${id}`).join('\n') + '\n');
  console.log(`${selected.length} additional video URLs`);
} else if (action === 'repair-audio') {
  // Move only individually identified files inside the retained research archive.
  const records = [];
  const bad = new Set();
  const safeMove = (source, target) => {
    const root = path.resolve(archive) + path.sep;
    if (![source, target].every(p => path.resolve(p).startsWith(root))) throw new Error('Move outside archive');
    fs.mkdirSync(path.dirname(target), { recursive: true });
    if (fs.existsSync(target)) throw new Error(`Target already exists: ${target}`);
    fs.renameSync(source, target);
  };
  const audioDir = path.join(archive, 'audio');
  const files = fs.readdirSync(audioDir);
  for (const name of files.filter(x => x.endsWith('.info.json'))) {
    const meta = read(path.join(audioDir, name));
    if (!meta.language || meta.language.startsWith('en')) continue;
    bad.add(meta.id);
    const destination = path.join(archive, 'audio-other-languages', meta.language);
    for (const file of files.filter(x => x.startsWith(meta.id + '.'))) {
      safeMove(path.join(audioDir, file), path.join(destination, file));
    }
    records.push({ id: meta.id, language: meta.language, previousFormat: meta.format_id,
                   retainedAt: path.relative(archive, destination), originalEnglishReacquisition: 'queued' });
  }
  for (const name of fs.readdirSync(run).filter(x => x.startsWith('audio') && x.endsWith('archive.txt'))) {
    const file = path.join(run, name);
    const original = fs.readFileSync(file, 'utf8');
    const backup = `${file}.before-language-fix`;
    if (!fs.existsSync(backup)) write(backup, original);
    write(file, original.split(/\r?\n/).filter(line => !bad.has(line.split(' ')[1])).filter(Boolean).join('\n') + '\n');
  }
  const speechDir = path.join(archive, 'speech-transcripts/small.en');
  for (const name of fs.readdirSync(speechDir).filter(x => x.endsWith('.json'))) {
    const meta = read(path.join(speechDir, name));
    if (!bad.has(meta.id) || !meta.source_audio.replaceAll('\\', '/').includes('/audio/')) continue;
    const record = records.find(x => x.id === meta.id);
    meta.review = 'requires-original-English-retranscription';
    meta.source_audio = path.join(archive, record.retainedAt, `${meta.id}.opus`);
    write(path.join(speechDir, name), JSON.stringify(meta, null, 2));
    const destination = path.join(archive, 'speech-transcripts/small.en-other-languages');
    for (const ext of ['.json', '.txt', '.error.txt']) {
      const file = path.join(speechDir, meta.id + ext);
      if (fs.existsSync(file)) safeMove(file, path.join(destination, meta.id + ext));
    }
  }
  const journal = path.join(run, 'language-repair.json');
  const previous = fs.existsSync(journal) ? read(journal) : [];
  write(journal, JSON.stringify([...previous, ...records], null, 2));
  const entries = read(path.join(run, 'videos.json'));
  const pending = entries.filter(x => !['audio', 'media'].some(dir => fs.existsSync(path.join(archive, dir, `${x.id}.opus`))));
  for (let shard = 0; shard < 4; shard++) {
    write(path.join(run, `audio-shard-${shard}.txt`), pending.filter((_, i) => i % 4 === shard)
      .map(x => `https://www.youtube.com/watch?v=${x.id}`).join('\n') + '\n');
  }
  console.log(JSON.stringify({ wrongLanguageFilesPreserved: bad.size, pendingOriginalEnglish: pending.length }));
} else if (action === 'audio-review') {
  const file = path.join(run, 'audio-reviews.json');
  const previous = fs.existsSync(file) ? read(file) : [];
  for (const spec of process.argv.slice(3)) {
    const [id, range] = spec.split('@');
    const transcript = read(path.join(archive, 'speech-transcripts/small.en', `${id}.json`));
    const metadata = read(transcript.source_audio.replace(/\.[^.]+$/, '.info.json'));
    if (metadata.language && !metadata.language.startsWith('en')) throw new Error('Non-English track');
    previous.push({ id, range: range ?? 'selected excerpts', sourceAudio: transcript.source_audio,
                    sourceLanguage: metadata.language ?? 'unspecified', model: transcript.model,
                    review: 'ASR-text-excerpts-reviewed', physicalValidation: 'not-performed' });
  }
  write(file, JSON.stringify([...new Map(previous.map(x => [x.id, x])).values()], null, 2));
  console.log(`${previous.length} audio review records`);
} else if (action === 'coverage') {
  const entries = read(path.join(run, 'videos.json'));
  const refRoot = path.resolve(import.meta.dirname, '../../skills/scadmaxx/references');
  const inventory = fs.readFileSync(path.join(refRoot, '3d-print-tricks-inventory.md'), 'utf8');
  const cited = new Set([...inventory.matchAll(/youtube\.com\/watch\?v=([A-Za-z0-9_-]{11})/g)].map(x => x[1]));
  const reviewFile = path.join(run, 'audio-reviews.json');
  const speechReviewed = new Set(fs.existsSync(reviewFile) ? read(reviewFile).map(x => x.id) : ['uMA-Wt-z_BU']);
  const completedDownloads = new Set(fs.readdirSync(run).filter(x => x.endsWith('archive.txt')).flatMap(name =>
    fs.readFileSync(path.join(run, name), 'utf8').split(/\r?\n/).map(line => /^youtube ([A-Za-z0-9_-]{11})$/.exec(line)?.[1]).filter(Boolean)));
  const speech = path.join(archive, 'speech-transcripts/small.en');
  const rows = entries.map(entry => ({ ...entry,
    audio: ['audio', 'media'].filter(dir => fs.existsSync(path.join(archive, dir, `${entry.id}.opus`))).map(dir => `${dir}/${entry.id}.opus`),
    completedDownload: completedDownloads.has(entry.id),
    retainedVideo: fs.existsSync(path.join(archive, 'media', `${entry.id}.mkv`)) ? `media/${entry.id}.mkv` : null,
    captions: fs.existsSync(path.join(archive, 'transcripts', `${entry.id}.txt`)),
    speechTranscript: fs.existsSync(path.join(speech, `${entry.id}.json`)),
    review: cited.has(entry.id) ? (speechReviewed.has(entry.id) ? 'audio-ASR-excerpts-inventoried' : 'caption-excerpts-inventoried') : 'pending',
    physicalValidation: 'not-performed',
  }));
  write(path.join(run, 'coverage.json'), JSON.stringify(rows, null, 2));
  write(path.join(run, 'missing-audio-urls.txt'), rows.filter(x => !x.audio.length || !x.completedDownload)
    .map(x => `https://www.youtube.com/watch?v=${x.id}`).join('\n') + '\n');
  const visual = fs.readFileSync(path.join(refRoot, '3d-print-visual-evidence.md'), 'utf8');
  for (const line of visual.split('\n').filter(x => x.startsWith('| ['))) {
    const columns = line.split('|').map(x => x.trim());
    const id = /watch\?v=([A-Za-z0-9_-]{11})/.exec(columns[1])?.[1];
    for (const seconds of columns[2].split(',').map(x => x.trim())) {
      const file = path.join(archive, 'frames', `${id}-${seconds.padStart(4, '0')}.png.json`);
      if (fs.existsSync(file)) {
        const meta = read(file);
        meta.review = 'inspected'; meta.observation = columns[3];
        write(file, JSON.stringify(meta, null, 2));
      }
    }
  }
  const summary = { updated: new Date().toISOString(), entries: rows.length,
    trickRows: [...inventory.matchAll(/^\| T\d{3} \|/gm)].length,
    extractedAudioFiles: rows.filter(x => x.audio.length).length,
    completedAudioDownloads: rows.filter(x => x.audio.length && x.completedDownload).length,
    retainedVideos: rows.filter(x => x.retainedVideo).length,
    captionTranscripts: rows.filter(x => x.captions).length,
    speechTranscripts: rows.filter(x => x.speechTranscript).length,
    sourcesWithInventoriedExcerpts: rows.filter(x => x.review !== 'pending').length,
    sourcesPendingReview: rows.filter(x => x.review === 'pending').length,
    allAudioAcquired: rows.every(x => x.audio.length && x.completedDownload),
    wholeChannelReviewed: false,
  };
  write(path.join(run, 'coverage-summary.json'), JSON.stringify(summary, null, 2));
  write(path.join(run, 'coverage.md'), '# Slant 3D acquisition and review coverage\n\n'
    + 'Snapshot: ' + summary.updated + '. Excerpt review is not whole-video review or physical validation.\n\n'
    + Object.entries(summary).map(([key, value]) => `- ${key}: ${value}`).join('\n')
    + '\n\n| Video | Title | Completed audio download | Video retained | Captions | Local ASR | Review |\n'
    + '| --- | --- | --- | --- | --- | --- | --- |\n'
    + rows.map(x => `| [${x.id}](https://www.youtube.com/watch?v=${x.id}) | ${x.title.replaceAll('|', '/')} | ${x.audio.length && x.completedDownload} | ${!!x.retainedVideo} | ${x.captions} | ${x.speechTranscript} | ${x.review} |`).join('\n') + '\n');
  console.log(JSON.stringify(summary));
} else if (action === 'status') {
  const entries = read(path.join(run, 'videos.json'));
  const names = ['audio', 'media', 'transcripts'].flatMap(dir => fs.readdirSync(path.join(archive, dir)).map(name => ({ dir, name })));
  const report = { date: new Date().toISOString(), entries: entries.length,
    audio: new Set(names.filter(x => /\.(opus|m4a|mp3|ogg)$/.test(x.name)).map(x => x.name.split('.')[0])).size,
    video: new Set(names.filter(x => /^[A-Za-z0-9_-]{11}\.(mkv|mp4)$/.test(x.name)).map(x => x.name.split('.')[0])).size,
    captions: new Set(names.filter(x => x.name.endsWith('.en.json3')).map(x => x.name.slice(0, -'.en.json3'.length))).size,
    transcripts: names.filter(x => x.dir === 'transcripts').length };
  write(path.join(run, 'acquisition-status.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report));
} else {
  throw new Error('Use index, transcripts, read [--speech], frame, extra-queue, repair-audio, audio-review, coverage or status');
}
