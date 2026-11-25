#!/usr/bin/env python3
"""Expose this checkout's skills through Codex's supported discovery folders."""

import argparse
from pathlib import Path
import sys


def install(source: Path, destination: Path, dry_run: bool) -> int:
    skills = sorted(path for path in (source / "skills").iterdir() if (path / "SKILL.md").is_file())
    collisions = []
    pending = []
    for skill in skills:
        target = destination / skill.name
        if target.is_symlink() and target.resolve() == skill.resolve():
            continue
        if target.exists() or target.is_symlink():
            collisions.append(target)
        else:
            pending.append((skill, target))
    if collisions:
        print("Existing skills would be overwritten; nothing changed:", file=sys.stderr)
        for path in collisions:
            print(f"  {path}", file=sys.stderr)
        return 1
    for skill, target in pending:
        print(f"{'Would link' if dry_run else 'Linking'} {target} -> {skill}")
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for skill, target in pending:
            target.symlink_to(skill, target_is_directory=True)
    print(f"{len(skills)} skills; {len(pending)} {'planned' if dry_run else 'created'}, {len(skills) - len(pending)} already linked.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument("--project", type=Path, help="Repository to receive .agents/skills links")
    location.add_argument("--user", action="store_true", help="Link into ~/.agents/skills for all repositories")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    destination = (Path.home() / ".agents/skills") if args.user else (args.project.expanduser().resolve() / ".agents/skills")
    return install(source, destination, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
