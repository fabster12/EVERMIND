"""Build the two share packages in dist/.

Usage:  python tools/build_packages.py

Writes into dist/. The zips themselves are gitignored - they rebuild in
seconds and a stale one in git is worse than none - but dist/ is committed
because it holds update-zips.cmd and the readmes that go inside the zips.

Normally run via dist/update-zips.cmd, which regenerates the documents first.

Two zips, because two audiences:

  EverMind-Group1-Docs.zip   PDFs, Markdown, the Gate 1 plan and the specs.
                             Everything readable, nothing to run.
  EverMind-Group1-Tech.zip   The fixtures, the build scripts, the data
                             contract and the specs. For whoever picks up
                             the code on Tuesday.

The specs and the contract appear in both: a reviewer needs to read them,
and a developer needs to build against them.

Superseded files (anything *-v1.*) are excluded deliberately - sharing two
versions of the same document invites someone to read the wrong one. The v1
builder stays in the repo so v1 can be regenerated if ever needed.
"""

import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent    # project root
DIST = ROOT / "dist"          # holds update-zips.cmd and the two zip readmes

# Patterns that must never appear in a shared archive. Matched against the
# bytes of every text member after the zip is built, not before - a
# packaging bug that picks up the wrong file is exactly what this catches.
#
# Each is assembled from fragments rather than written out whole. If the
# literals appeared here, this file would trip its own scan the moment it
# was packaged - which it did, the first time it ran.
SECRET_PATTERNS = [
    b"voc" + rb"-[0-9a-f]{20}",
    b"sk-" + b"svcacct",
    b"sk-" + b"ant-",
    b"ghp" + rb"_[A-Za-z0-9]{36}",
    b"w9p" + b"KN6",
    b"GITHUB_" + rb"TOKEN=\S",
    b"AIza" + rb"[0-9A-Za-z_-]{35}",
]

SPECS = [
    ("src/openspec/changes/add-evermind-pipeline/proposal.md", None),
    ("src/openspec/changes/add-evermind-pipeline/design.md", None),
    ("src/openspec/changes/add-evermind-pipeline/tasks.md", None),
    ("src/openspec/changes/add-evermind-pipeline/specs/gap-triage/spec.md", None),
    ("src/openspec/changes/add-evermind-pipeline/specs/evidence-retrieval/spec.md", None),
    ("src/openspec/changes/add-evermind-pipeline/specs/candidate-drafting/spec.md", None),
    ("src/openspec/changes/add-evermind-pipeline/specs/review-queue/spec.md", None),
    ("src/contracts/knowledge-base/contract.md", None),
]

# (source path relative to ROOT, path inside the zip or None to keep it)
DOCS_MEMBERS = [
    ("docs/gate1/FedEx-Capstone-Summary-Group1.pdf", None),
    ("docs/gate1/FedEx-Capstone-Design-EverMind.pdf", None),
    ("docs/gate1/FedEx-Capstone-Summary-Group1.md", None),
    ("docs/architecture.png", None),
    ("docs/reviews/EverMind-Proposal-Review.pdf", None),
    ("docs/reviews/openspec-alignment-review.md", None),
    ("docs/decisions/0000-template.md", None),
    ("docs/course/Capstone-Groups-and-Prep.md", None),
] + SPECS

TECH_MEMBERS = [
    ("src/fixtures/faq_store.json", None),
    ("src/fixtures/query_log.json", None),
    ("src/fixtures/sources.json", None),
    ("tools/build_fixtures.py", None),
    ("tools/build_diagram.py", None),
    ("tools/build_design_evermind.py", None),
    ("tools/build_summary_group1.py", None),
    ("tools/build_review_benchmark.py", None),
    ("tools/fedex_layout.py", None),
    ("tools/packaging/build_packages.py", None),
    ("tools/packaging/to_pdf.ps1", None),
    ("docs/architecture.png", None),
    ("README.md", "PROJECT-README.md"),
] + SPECS

# Repo-hygiene files at the project root.
TECH_EXTRA = [
    (ROOT / ".env.example", ".env.example"),
    (ROOT / ".gitignore", ".gitignore"),
]


def _add(zf, src, arc, missing):
    if not src.exists():
        missing.append(arc)
        return 0
    zf.write(src, arc)
    return 1


def build(name, members, readme_src, extra=(), overrides=None):
    """Write one zip. `overrides` maps an arc name to a different source."""
    overrides = overrides or {}
    out = DIST / name
    missing = []
    count = 0

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel, arc in members:
            arc = arc or rel
            src = overrides.get(arc) or (ROOT / rel)
            count += _add(zf, src, arc, missing)
        for src, arc in extra:
            count += _add(zf, src, arc, missing)
        zf.write(readme_src, "README.md")
        count += 1

    return out, count, missing


def verify(path):
    """Integrity and a secret scan over the built archive."""
    problems = []
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            problems.append("corrupt member: " + bad)
        for info in zf.infolist():
            if info.file_size > 4_000_000:
                continue
            data = zf.read(info.filename)
            for pat in SECRET_PATTERNS:
                if re.search(pat, data):
                    problems.append(
                        "possible secret (%s) in %s"
                        % (pat.decode("ascii", "replace"), info.filename)
                    )
    return problems


def main():
    DIST.mkdir(exist_ok=True)

    # The summary .docx may be locked by an open Word window, leaving a
    # stale copy in the repo root. Build a fresh one into dist/ and pack
    # that instead, so a lock can never put an out-of-date document in
    # front of a reviewer.
    overrides = {}
    staged = DIST / "_staged-summary.docx"
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import build_summary_group1

        build_summary_group1.build(staged)
        overrides["FedEx-Capstone-Summary-Group1.docx"] = staged
    except Exception as exc:                       # pragma: no cover
        print("warning: could not rebuild summary .docx (%s)" % exc)
        print("         packing the copy in the repo root instead")

    docs_zip, docs_n, docs_missing = build(
        "EverMind-Group1-Docs.zip",
        DOCS_MEMBERS,
        DIST / "_docs_readme.md",
        overrides=overrides,
    )
    tech_zip, tech_n, tech_missing = build(
        "EverMind-Group1-Tech.zip",
        TECH_MEMBERS,
        DIST / "_tech_readme.md",
        extra=TECH_EXTRA,
    )

    if staged.exists():
        staged.unlink()

    ok = True
    for z, n, missing in ((docs_zip, docs_n, docs_missing), (tech_zip, tech_n, tech_missing)):
        size = z.stat().st_size
        digest = hashlib.md5(z.read_bytes()).hexdigest()[:12]
        print("%-32s %7d bytes  %2d files  md5:%s" % (z.name, size, n, digest))
        if missing:
            ok = False
            for m in missing:
                print("    MISSING: " + m)
        problems = verify(z)
        if problems:
            ok = False
            for p in problems:
                print("    " + p)
        else:
            print("    integrity OK, no secrets found")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
