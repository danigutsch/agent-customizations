#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Literal, TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]
BASELINE_MANIFEST_PATH = ROOT / "scripts" / "tool_file_baselines.json"
SEMVER_PATTERN = re.compile(r"\b(?P<version>\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.\-]+)?)\b")
SPEC_KIT_VERSION_MARKERS = ("specify", "spec kit", "speckit")


class VersionSignal(TypedDict):
    value: str
    source: str


class BaselineVariant(TypedDict):
    label: str
    sha256: str


class BaselineEntry(TypedDict):
    source: str
    source_path: str
    upstream_ref: str
    current: list[BaselineVariant]
    historical: list[BaselineVariant]


class BaselineMatch(TypedDict):
    source: str
    source_path: str
    upstream_ref: str
    matched_variant: str | None
    exact_status: Literal["current", "historical", "unmatched"]


class FileMatch(TypedDict):
    path: str
    family: str
    kind: str
    matched_by: str
    fingerprint: str
    git_state: str
    marker_hits: list[str]
    version_signal: VersionSignal | None
    baseline: BaselineMatch | None
    drift_status: Literal["current", "outdated", "modified", "unknown"]
    remediation: str
    notes: list[str]


class Summary(TypedDict):
    total_matches: int
    by_family: dict[str, int]
    by_drift_status: dict[str, int]


class Report(TypedDict):
    repo: str
    repo_root: str | None
    files: list[FileMatch]
    summary: Summary


class CandidateSpec(TypedDict):
    family: Literal["aspire", "speckit"]
    kind: str
    pattern: str
    match_mode: Literal["exact", "glob"]
    required_markers: tuple[str, ...]
    version_markers: tuple[str, ...]
    remediation: str


CANDIDATE_SPECS: tuple[CandidateSpec, ...] = (
    {
        "family": "aspire",
        "kind": "skill",
        "pattern": ".github/skills/aspire/SKILL.md",
        "match_mode": "exact",
        "required_markers": ("Aspire",),
        "version_markers": ("aspire", "version"),
        "remediation": "Rerun `aspire agent init` in the downstream Aspire project to refresh tool-provided files.",
    },
    {
        "family": "speckit",
        "kind": "agent",
        "pattern": ".github/agents/speckit.*.agent.md",
        "match_mode": "glob",
        "required_markers": (),
        "version_markers": SPEC_KIT_VERSION_MARKERS,
        "remediation": "Refresh the Spec Kit integration with `specify init` or the narrower Spec Kit integration flow used by the downstream project.",
    },
    {
        "family": "speckit",
        "kind": "prompt",
        "pattern": ".github/prompts/speckit.*.prompt.md",
        "match_mode": "glob",
        "required_markers": (),
        "version_markers": SPEC_KIT_VERSION_MARKERS,
        "remediation": "Refresh the Spec Kit integration with `specify init` or the narrower Spec Kit integration flow used by the downstream project.",
    },
    {
        "family": "speckit",
        "kind": "context",
        "pattern": ".github/copilot-instructions.md",
        "match_mode": "exact",
        "required_markers": ("<!-- SPECKIT START -->",),
        "version_markers": SPEC_KIT_VERSION_MARKERS,
        "remediation": "Refresh the Spec Kit Copilot integration if this file is intended to stay generator-owned.",
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a repository for Aspire- and Spec Kit-provided generated files and report "
            "provenance, bundled-baseline matches, and conservative drift signals."
        )
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository root to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format. Defaults to text.",
    )
    parser.add_argument(
        "--family",
        action="append",
        choices=["aspire", "speckit"],
        help="Filter to one or more file families.",
    )
    return parser.parse_args()


def selected_specs(requested_families: list[str] | None) -> list[CandidateSpec]:
    if not requested_families:
        return list(CANDIDATE_SPECS)
    return [spec for spec in CANDIDATE_SPECS if spec["family"] in requested_families]


def find_matches(repo: Path, specs: list[CandidateSpec]) -> list[tuple[Path, CandidateSpec]]:
    matches: dict[Path, CandidateSpec] = {}
    for spec in specs:
        if spec["match_mode"] == "exact":
            path = repo / spec["pattern"]
            if path.is_file():
                matches[path] = spec
            continue

        for path in repo.glob(spec["pattern"]):
            if path.is_file():
                matches[path] = spec

    return [(path, matches[path]) for path in sorted(matches)]


def normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    normalized_lines = [
        line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    return "\n".join(normalized_lines).strip() + "\n"


def fingerprint_for(path: Path) -> str:
    content = normalized_text(path).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def load_baselines() -> dict[str, BaselineEntry]:
    if not BASELINE_MANIFEST_PATH.is_file():
        return {}

    data = json.loads(BASELINE_MANIFEST_PATH.read_text(encoding="utf-8"))
    files = data.get("files", {})
    return cast(dict[str, BaselineEntry], files)


def baseline_match_for(
    relative_path: str, fingerprint: str, baselines: dict[str, BaselineEntry]
) -> BaselineMatch | None:
    entry = baselines.get(relative_path)
    if entry is None:
        return None

    for variant in entry["current"]:
        if variant["sha256"] == fingerprint:
            return {
                "source": entry["source"],
                "source_path": entry["source_path"],
                "upstream_ref": entry["upstream_ref"],
                "matched_variant": variant["label"],
                "exact_status": "current",
            }

    for variant in entry["historical"]:
        if variant["sha256"] == fingerprint:
            return {
                "source": entry["source"],
                "source_path": entry["source_path"],
                "upstream_ref": entry["upstream_ref"],
                "matched_variant": variant["label"],
                "exact_status": "historical",
            }

    return {
        "source": entry["source"],
        "source_path": entry["source_path"],
        "upstream_ref": entry["upstream_ref"],
        "matched_variant": None,
        "exact_status": "unmatched",
    }


def marker_hits(content: str, spec: CandidateSpec) -> list[str]:
    haystack = content.casefold()
    hits: list[str] = []
    for marker in spec["required_markers"]:
        if marker.casefold() in haystack:
            hits.append(marker)
    return hits


def version_signal_for(content: str, spec: CandidateSpec) -> VersionSignal | None:
    lowered = content.casefold()
    for marker in spec["version_markers"]:
        if marker.casefold() not in lowered:
            continue

        marker_index = lowered.find(marker.casefold())
        window = content[max(0, marker_index - 40) : marker_index + 120]
        match = SEMVER_PATTERN.search(window)
        if match is not None:
            return {
                "value": match.group("version"),
                "source": f"near marker `{marker}`",
            }

    return None


def repo_root(path: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def git_state_for(repo_root_path: Path | None, path: Path) -> str:
    if repo_root_path is None:
        return "not-repo"

    relative_path = path.relative_to(repo_root_path).as_posix()
    result = subprocess.run(
        ["git", "-C", str(repo_root_path), "status", "--porcelain", "--", relative_path],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return "unknown"

    output = result.stdout.strip()
    if not output:
        tracked = subprocess.run(
            ["git", "-C", str(repo_root_path), "ls-files", "--error-unmatch", "--", relative_path],
            text=True,
            capture_output=True,
            check=False,
        )
        return "clean" if tracked.returncode == 0 else "untracked"

    first_status = output[:2]
    if "?" in first_status:
        return "untracked"
    return "modified"


def drift_status_for(
    baseline: BaselineMatch | None,
    version_signal: VersionSignal | None,
    git_state: str,
) -> Literal["current", "outdated", "modified", "unknown"]:
    if baseline is not None:
        if baseline["exact_status"] == "current":
            return "current"
        if baseline["exact_status"] == "historical":
            return "outdated"
        if git_state == "modified":
            return "modified"
        if git_state == "clean":
            return "outdated"
        return "unknown"

    if version_signal is not None:
        return "current"
    if git_state == "modified":
        return "modified"
    return "unknown"


def version_signal_note(
    version_signal: VersionSignal | None, baseline: BaselineMatch | None
) -> str | None:
    if version_signal is not None:
        return None

    if baseline is None:
        return "No embedded semantic version marker was found; this tool falls back to provenance and git-state inspection."

    return "No embedded semantic version marker was found; this tool compares the file fingerprint against bundled upstream baselines."


def baseline_notes(baseline: BaselineMatch | None, git_state: str) -> list[str]:
    if baseline is None:
        return ["No bundled upstream baseline is maintained for this specific path yet."]

    baseline_id = f"{baseline['source']}@{baseline['upstream_ref']} ({baseline['source_path']})"
    variant = baseline["matched_variant"]

    if baseline["exact_status"] == "current":
        return [
            f"Fingerprint matches the current bundled baseline for {baseline_id} [{variant or 'current'}]."
        ]

    if baseline["exact_status"] == "historical":
        return [
            f"Fingerprint matches a historical bundled baseline for {baseline_id} [{variant or 'historical'}]."
        ]

    notes = [f"Fingerprint does not match any bundled current baseline for {baseline_id}."]
    if git_state == "clean":
        notes.append(
            "Because the file is tracked and clean in Git, it is treated as likely outdated tool output."
        )
    return notes


def git_state_note(git_state: str) -> str | None:
    if git_state == "not-repo":
        return "Target directory is not a Git repository, so local modification state could not be checked."
    if git_state == "untracked":
        return "File is present but untracked by Git in the inspected repository."
    if git_state == "clean":
        return "File is tracked and currently clean in Git."
    if git_state == "modified":
        return "File has uncommitted Git changes in the inspected repository."
    return None


def family_note(spec: CandidateSpec) -> str:
    if spec["family"] == "aspire":
        return "Aspire-generated skill files are documented as setup-provided agent context."
    return "Spec Kit files are treated as tool-generated workflow scaffolding unless deliberately curated."


def notes_for(
    spec: CandidateSpec,
    git_state: str,
    version_signal: VersionSignal | None,
    baseline: BaselineMatch | None,
) -> list[str]:
    notes: list[str] = []

    signal_note = version_signal_note(version_signal, baseline)
    if signal_note is not None:
        notes.append(signal_note)

    notes.extend(baseline_notes(baseline, git_state))

    state_note = git_state_note(git_state)
    if state_note is not None:
        notes.append(state_note)

    notes.append(family_note(spec))
    return notes


def analyze_match(
    path: Path,
    repo: Path,
    repo_root_path: Path | None,
    spec: CandidateSpec,
    baselines: dict[str, BaselineEntry],
) -> FileMatch | None:
    content = normalized_text(path)
    hits = marker_hits(content, spec)
    if len(hits) < len(spec["required_markers"]):
        return None

    relative_path = path.relative_to(repo).as_posix()
    fingerprint = fingerprint_for(path)
    version_signal = version_signal_for(content, spec)
    git_state = git_state_for(repo_root_path, path)
    baseline = baseline_match_for(relative_path, fingerprint, baselines)
    return {
        "path": relative_path,
        "family": spec["family"],
        "kind": spec["kind"],
        "matched_by": spec["pattern"],
        "fingerprint": fingerprint,
        "git_state": git_state,
        "marker_hits": hits,
        "version_signal": version_signal,
        "baseline": baseline,
        "drift_status": drift_status_for(baseline, version_signal, git_state),
        "remediation": spec["remediation"],
        "notes": notes_for(spec, git_state, version_signal, baseline),
    }


def summarize(files: list[FileMatch]) -> Summary:
    by_family: dict[str, int] = {}
    by_drift_status: dict[str, int] = {}
    for file_match in files:
        by_family[file_match["family"]] = by_family.get(file_match["family"], 0) + 1
        status = file_match["drift_status"]
        by_drift_status[status] = by_drift_status.get(status, 0) + 1
    return {
        "total_matches": len(files),
        "by_family": by_family,
        "by_drift_status": by_drift_status,
    }


def build_report(repo: Path, specs: list[CandidateSpec]) -> Report:
    resolved_repo = repo.expanduser().resolve()
    repo_root_path = repo_root(resolved_repo)
    baselines = load_baselines()
    files: list[FileMatch] = []
    for path, spec in find_matches(resolved_repo, specs):
        file_match = analyze_match(path, resolved_repo, repo_root_path, spec, baselines)
        if file_match is not None:
            files.append(file_match)

    return {
        "repo": str(resolved_repo),
        "repo_root": str(repo_root_path) if repo_root_path is not None else None,
        "files": files,
        "summary": summarize(files),
    }


def print_text_report(report: Report) -> None:
    print(f"Tool-provided file inspection for {report['repo']}")
    if report["repo_root"] is not None:
        print(f"Git root: {report['repo_root']}")

    if not report["files"]:
        print("No matching Aspire or Spec Kit tool-provided files were found.")
        return

    for file_match in report["files"]:
        print(
            f"- {file_match['path']} [{file_match['family']}:{file_match['kind']}] "
            f"=> {file_match['drift_status']}"
        )
        print(f"  matched by: {file_match['matched_by']}")
        print(f"  fingerprint: {file_match['fingerprint']}")
        print(f"  git state: {file_match['git_state']}")
        baseline = file_match["baseline"]
        if baseline is not None:
            variant = baseline["matched_variant"] or "none"
            print(
                f"  baseline: {baseline['source']}@{baseline['upstream_ref']} "
                f"({baseline['exact_status']}, variant={variant}, source={baseline['source_path']})"
            )
        else:
            print("  baseline: none")
        if file_match["version_signal"] is not None:
            version_signal = file_match["version_signal"]
            print(f"  version signal: {version_signal['value']} ({version_signal['source']})")
        else:
            print("  version signal: none")
        print(f"  marker hits: {', '.join(file_match['marker_hits'])}")
        for note in file_match["notes"]:
            print(f"  note: {note}")
        print(f"  remediation: {file_match['remediation']}")

    summary = report["summary"]
    print(
        "Summary: "
        f"{summary['total_matches']} file(s), "
        f"families={json.dumps(summary['by_family'], sort_keys=True)}, "
        f"statuses={json.dumps(summary['by_drift_status'], sort_keys=True)}"
    )


def main() -> None:
    args = parse_args()
    report = build_report(args.repo, selected_specs(cast(list[str] | None, args.family)))

    if args.format == "json":
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    print_text_report(report)


if __name__ == "__main__":
    main()
