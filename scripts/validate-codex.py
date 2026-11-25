#!/usr/bin/env python3
"""Validate this collection's Codex discovery, metadata, and local references."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")


ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", "node_modules", "__pycache__"}


def main() -> int:
    errors = []
    files = sorted(path for path in ROOT.rglob("*") if path.is_file() and not IGNORED.intersection(path.relative_to(ROOT).parts))
    skills = [path for path in files if path.name == "SKILL.md"]
    public = sorted((ROOT / "skills").glob("*/SKILL.md"))
    for path in skills:
        label = path.relative_to(ROOT)
        text = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            errors.append(f"{label}: missing YAML frontmatter")
            continue
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"{label}: invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{label}: frontmatter must be a mapping")
            continue
        if data.get("name") != path.parent.name or not re.fullmatch(r"[a-z0-9-]{1,64}", str(data.get("name", ""))):
            errors.append(f"{label}: invalid name or folder mismatch")
        description = data.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{label}: description must contain 1–1024 characters")
        if "disable-model-invocation" in data:
            errors.append(f"{label}: move invocation policy to agents/openai.yaml")
        metadata = path.parent / "agents/openai.yaml"
        if metadata.exists():
            try:
                config = yaml.safe_load(metadata.read_text())
                if not isinstance(config, dict):
                    raise ValueError("metadata must be a mapping")
                policy = config.get("policy", {})
                if not isinstance(policy, dict):
                    raise ValueError("policy must be a mapping")
                if "allow_implicit_invocation" in policy and type(policy["allow_implicit_invocation"]) is not bool:
                    raise ValueError("allow_implicit_invocation must be a boolean")
            except (yaml.YAMLError, ValueError) as exc:
                errors.append(f"{metadata.relative_to(ROOT)}: {exc}")

    discovery = ROOT / ".agents/skills"
    for path in public:
        link = discovery / path.parent.name
        if not link.is_symlink() or link.resolve() != path.parent.resolve():
            errors.append(f"{link.relative_to(ROOT)}: expected link to canonical public skill")
    if discovery.exists():
        for link in discovery.iterdir():
            if not (ROOT / "skills" / link.name / "SKILL.md").is_file():
                errors.append(f"{link.relative_to(ROOT)}: unexpected discovery entry")

    manifest_path = ROOT / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text())
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be an object")
        for key in ["name", "version", "description"]:
            if not isinstance(manifest.get(key), str) or not manifest[key].strip():
                errors.append(f"plugin.json: {key} must be a non-empty string")
        if isinstance(manifest.get("name"), str) and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]):
            errors.append("plugin.json: name must use lowercase kebab-case")
        if isinstance(manifest.get("version"), str) and not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", manifest["version"]):
            errors.append("plugin.json: version must be a semantic version")
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("plugin.json: missing portable schema")
        extension = manifest["extensions"]["com.openai"]
        package_paths = [extension["onboardingSkill"]]
        if "logo" in extension["interface"]:
            package_paths.append(extension["interface"]["logo"])
        for value in package_paths:
            if (not isinstance(value, str) or not value.startswith("./")
                    or not (ROOT / value).resolve().is_relative_to(ROOT.resolve())
                    or not (ROOT / value).is_file()):
                errors.append(f"plugin.json: invalid package path {value}")
        for key in ["displayName", "shortDescription", "longDescription", "developerName"]:
            field = extension["interface"].get(key)
            if not isinstance(field, str) or not field.strip():
                errors.append(f"plugin.json: missing interface {key}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"plugin.json: invalid manifest: {exc}")

    links = 0
    for path in files:
        if path.suffix != ".md":
            continue
        # Examples inside fenced code blocks are not navigable document links.
        prose = re.sub(r"^(`{3,}|~{3,}).*?^\1[^\n]*$", "", path.read_text(), flags=re.M | re.S)
        targets = [match.group(1) for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", prose)]
        targets.extend(match.group(1) for match in re.finditer(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|\S+)", prose, flags=re.M))
        for target in targets:
            target = target.strip()
            if target.startswith("<"):
                if ">" not in target:
                    errors.append(f"{path.relative_to(ROOT)}: unterminated link {target}")
                    continue
                target = target[1:target.index(">")]
            else:
                target = target.split(' "', 1)[0]
            try:
                parsed = urlsplit(target)
            except ValueError as exc:
                errors.append(f"{path.relative_to(ROOT)}: malformed link {target}: {exc}")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if any(char in parsed.path for char in "<>{}*"):
                continue
            resolved = path.parent / unquote(parsed.path)
            links += 1
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link {target}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} problems", file=sys.stderr)
        return 1
    print(f"PASS: {len(skills)} skills, {len(public)} discovery links, manifest, invocation metadata, {links} local references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
