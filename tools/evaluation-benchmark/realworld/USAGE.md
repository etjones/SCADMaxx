# Real-world SCAD benchmark

The corpus is frozen separately from the engine source at
`D:/openscad/artifacts/realworld-scad-corpus-20261004`. Tools belong to the controls repository;
downloaded third-party source and run evidence do not belong in the upstream feature patch.

## Setup and collection

Acquisition is sequential, with ten seconds between uncached GitHub search requests and two seconds between
repository acquisitions. HTTP rate-limit responses honor Retry-After and X-RateLimit-Reset, with bounded retries.
Search caches are keyed by query text and page. Use --query repeatedly for broader discovery, --pages for depth,
and --exclude-manifest PATH to collect additions without selecting normalized-source duplicates of an older corpus.
Use --all to index every unique nonempty SCAD file without count or diversity caps, including helpers and tests.
All raw downloaded sources remain retained even when duplicated or excluded from the manifest.
Additional sequential importers: import_thingiverse.py ROOT (pinned public SCAD dataset mirror),
import_codecad.py ROOT --limit 25 (pinned university GitLab source sample), and
import_webfiles.py ROOT CATALOG.json (explicit public source URLs with author, license and source-site metadata).
Dataset mirrors may omit external assets; their SCAD text is not a claim of complete dependency acquisition.

```powershell
uv sync --project D:/openscad/scadmaxx/tools/evaluation-benchmark/realworld
uv run --project D:/openscad/scadmaxx/tools/evaluation-benchmark/realworld python corpus.py `
  D:/openscad/artifacts/realworld-scad-corpus-20261004
```

Run commands from this tool directory, or use absolute script paths. `uv.lock` pins the numerical dependencies.
Use a writable `--cache-dir` if the machine's default uv cache is unavailable.

Discovery retains public GitHub search responses. Every repository is pinned by the archive's full Git commit
identifier and SHA-256; retained source/assets have individual hashes. License files and source links stay with
the files. UNKNOWN/NOASSERTION is not permission to redistribute; this is a local research corpus, not a
relicensed combined model package. Source scripts, build scripts and repository instructions are never executed.

Selection is deterministic, source-deduplicated and round-robin across repositories and directories: at most
25 files/repository, 10 files/directory, 40 files/owner. The 1,000 entries are **static candidates**, not a claim
that every file is a standalone valid solid. Empty library entry points, missing dependencies, 2D-only files,
warnings, invalid geometry and timeouts stay visible. Acquisition failures and size limits are recorded separately.
These limits and GitHub discovery introduce selection bias; this is not a random sample of all online SCAD use.

`--select-only` rebuilds the manifest from downloaded snapshots; do not use it after freezing a benchmark series.
To change membership, create a new corpus version. No quality reduction, parameter overrides, generated variants,
dependency auto-installation or silent source repair takes place during timed runs.
Retain `manifest.json` and `sources/*.json` together. `corpus.py ROOT --restore` downloads missing files from those
pinned source records, validates archived bytes and the individual file inventory, and refuses modified retained
files. It does not rediscover current branches or change the manifest. A changed upstream archive checksum needs
investigation, even if the URL still names the same commit.

## Run a baseline or adjacent paired comparisons

```powershell
uv run python benchmark.py `
  --corpus D:/openscad/artifacts/realworld-scad-corpus-20261004 `
  --output D:/openscad/runs/my-realworld-comparison `
  --build baseline=D:/openscad/runs/20261004-evaluation-math-fastpath/baseline/openscad.com `
  --build candidate=D:/openscad/runs/20261004-evaluation-math-fastpath/candidate/openscad.com `
  --stages ast csg preview stl off --repetitions 3 --timeout 30
```

Use only `--build baseline=...` to retain an initial baseline. Add future executables with explicit labels.
Repeat `--build-argument=candidate=--enable=FEATURE` for explicit runtime experimental switches. Arguments are retained
in each build identity and every command; compilation alone does not establish which features were exercised.
`--limit 20` or `--ids id1,id2` provides a smoke run. `--resume` requires the same immutable configuration,
source hashes, binary/runtime identities and runner, and skips completed samples. Failed cases count as completed;
use a new run to retry them with a longer timeout. Do not run two writers into the same output directory.

The frozen `baseline` runtime contains the original feature base and matching Windows build repairs, without the
phase-1 interpreter shortcut. The preserved phase-1 candidate uses the same compiler/dependencies. A current
worktree HEAD alone does not identify either edited build: metadata records executable, companion EXE, DLL,
build-info, corpus and dependency hashes. Existing SCAD models keep their original parameter/detail settings.

Runs are sequential. Build order alternates for adjacent pairs and model/stage order is seeded. Timeouts terminate
the child process tree. Raw logs, exact arguments, exit status, dependencies, native summaries, output files/hashes,
and every sample are retained. Avoid concurrent builds/benchmarks and use multiple repetitions for decisions.
Fresh process does not mean cold OS disk cache. System fonts, graphics drivers and machine state also affect results.

| Stage | Measured wall-time scope |
| --- | --- |
| `ast` | Startup, source loading/parsing, model instantiation, AST serialization |
| `csg` | Startup, parsing, language evaluation, CSG serialization |
| `preview` | Startup, evaluation, CSG preparation, offscreen drawing, PNG encoding |
| `stl` | Startup, evaluation, full geometry, binary STL serialization |
| `off` | Startup, evaluation, full geometry, indexed OFF serialization |

AST export also instantiates the model in this OpenSCAD revision; it is not a pure parser timer.
These scopes overlap. **Do not subtract separate runs to infer pure phase cost.** Native render summaries are
retained independently and exclude interpreter work. PNG generation is not native GUI first-present latency.
STL/OFF wall times also include the requested native summary/statistics output; all compared builds use the same flags.
Editor opening, source edit/reparse, warm parameter changes and first displayed frame need a future instrumented
GUI adapter; the current CLI harness must not label them as measured. Keep identical timing hooks in baseline
and candidate before adding parse/instantiate/normalization/backend/export/display substage comparisons.

## Compare, inspect and export

```powershell
uv run python report.py D:/openscad/runs/my-realworld-comparison `
  --output D:/openscad/runs/my-realworld-comparison-report
```

Multiple run directories can be supplied to compare a retained baseline with future runs. Corpus/dependencies,
backend, image size, machine, timeout, stage definitions and cache policy must match. Same labels must identify the same runtime. Adjacent
paired measurements in a single run are preferred to separate days. CSV, JSON, PNG graphs and a standalone
searchable/sortable HTML table are generated; no web service is needed. Report generation is outside timed runs.

Every successful candidate repetition and repeated baseline is compared against the first baseline output.
`ast`/`csg` comparison is textual; `preview` includes pixel difference metrics. Neither proves 3D equivalence.
STL/OFF compare meshes without alignment, scaling or repair. Exact identical triangle surfaces pass independent
of order; otherwise deterministic bidirectional point-to-triangle distances include sampled surface points,
vertices and triangle centers. Large meshes cap each sample group; maximum/RMS/p95 distances are **sampled
estimates, not a Hausdorff upper bound**. Retriangulated surfaces may pass the tolerance without identical faces.

Default tolerance: `1e-5 + 1e-6 * bounding_box_diagonal`, in model units (usually mm). Override `--absolute` and
`--relative` explicitly. Volume tolerance is tied to surface area times distance tolerance. Bounds, watertightness,
winding, connected components and Euler characteristic are checked independently. Unchanged invalid meshes are
inconclusive, not accepted. STL has no indices: exact-position vertex merging is necessary for its topology
check; OFF preserves original indexing. Zero-byte/failed/warning outputs are not eligible for speed ratios.
Sampling cannot prove the absence of every small defect; inspect flagged models and increase `--samples` when needed.

Tests: `uv run python -m unittest -v test_benchmark`.

The initial corpus-wide run is a one-repetition, five-second-per-operation survey of CSG, preview and STL.
Treat timeouts as censored slow cases, not completion times. The report shows how many candidates completed every
requested stage cleanly; it does not rename the whole corpus as validated solids. Paired validation selects a
documented subset of successful models using `select_paired_sample.py`; that subset is success-conditioned and
must not be used to claim a corpus-wide speedup. Use longer limits and repeated adjacent pairs for decisions.

See [GUI-INSTRUMENTATION.md](GUI-INSTRUMENTATION.md) for the unimplemented native opening/edit/first-present adapter.
