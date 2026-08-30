#!/usr/bin/env python3
"""Deterministic lint for an llm-wiki instance. No third-party deps."""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

REQUIRED_WIKI_KEYS = (
    "topic",
    "slug",
    "github",
    "pages_url",
    "source_policy",
    "volatile_days",
)
REQUIRED_PAGE_KEYS = ("title", "layout", "nav_order")
RAW_MAX_BYTES = 64_000
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
TOKEN_RE = re.compile(r"__[A-Z][A-Z0-9_]*__")
MD_LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
PIN_PAGE_RE = re.compile(r"^-\s*page:\s*(\S+)\s*$", re.MULTILINE)

SECTION_PARENTS = {
    Path("docs/sources/index.md"): "Sources",
    Path("docs/concepts/index.md"): "Concepts",
    Path("docs/entities/index.md"): "Entities",
    Path("docs/analyses/index.md"): "Analyses",
    Path("docs/meta/index.md"): "Meta",
}


def find_wiki_root(start: Path) -> Optional[Path]:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "WIKI.md").is_file():
            return candidate
    return None


def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    m = FM_RE.match(text)
    if not m:
        return None
    data = {}  # type: Dict[str, str]
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#") or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip().strip("\"'")
    return data


def docs_md_files(root: Path) -> List[Path]:
    docs = root / "docs"
    out = []  # type: List[Path]
    for dirpath, dirnames, filenames in os.walk(docs):
        dirnames[:] = [d for d in dirnames if d not in {".git", "_site"}]
        for name in filenames:
            if name.endswith(".md"):
                out.append(Path(dirpath) / name)
    return sorted(out)


def rel_docs(root: Path, path: Path) -> Path:
    return path.relative_to(root)


def resolve_link(from_file: Path, target: str) -> Optional[Path]:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target:
        target = target.split(" ", 1)[0]
    if target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    if target.startswith("/"):
        return from_file  # sentinel: absolute path, invalid
    path_part = target.split("#", 1)[0]
    if not path_part:
        return None
    return (from_file.parent / path_part).resolve()


def catalog_targets(root: Path, catalog_text: str) -> Set[Path]:
    catalog = root / "docs" / "catalog.md"
    found = set()  # type: Set[Path]
    for raw in MD_LINK_RE.findall(catalog_text):
        resolved = resolve_link(catalog, raw)
        if resolved is None:
            continue
        found.add(resolved)
    return found


def leftover_tokens(rel: str, text: str, errors: List[str]) -> None:
    for match in TOKEN_RE.finditer(text):
        errors.append("{0}: leftover init token `{1}`".format(rel, match.group(0)))


def body_of(text: str) -> str:
    m = FM_RE.match(text)
    if m:
        return text[m.end() :]
    return text


def lint(root: Path) -> List[str]:
    errors = []  # type: List[str]
    wiki_md = root / "WIKI.md"
    if not wiki_md.is_file():
        return ["WIKI.md: missing"]

    wiki_text = wiki_md.read_text(encoding="utf-8")
    wiki_fm = parse_frontmatter(wiki_text)
    leftover_tokens("WIKI.md", wiki_text, errors)
    if wiki_fm is None:
        errors.append("WIKI.md: missing YAML frontmatter")
    else:
        for key in REQUIRED_WIKI_KEYS:
            if not wiki_fm.get(key):
                errors.append(f"WIKI.md: missing frontmatter key `{key}`")
        if wiki_fm.get("source_policy") and wiki_fm["source_policy"] != "excerpts-only":
            errors.append("WIKI.md: source_policy must be `excerpts-only`")

    required_files = [
        "AGENTS.md",
        "docs/index.md",
        "docs/catalog.md",
        "docs/sources/index.md",
        "docs/concepts/index.md",
        "docs/entities/index.md",
        "docs/analyses/index.md",
        "docs/meta/index.md",
        "docs/meta/log.md",
        "docs/meta/pins.md",
        "_config.yml",
        "Gemfile",
        ".github/workflows/pages.yml",
        "raw/sources/.gitkeep",
    ]
    for rel in required_files:
        if not (root / rel).is_file():
            errors.append(f"{rel}: missing")

    pages = []  # type: List[Path]
    if (root / "docs").is_dir():
        pages = docs_md_files(root)

    catalog_path = root / "docs" / "catalog.md"
    catalog_text = catalog_path.read_text(encoding="utf-8") if catalog_path.is_file() else ""
    catalog_set = catalog_targets(root, catalog_text) if catalog_text else set()

    for path in pages:
        rel = rel_docs(root, path).as_posix()
        text = path.read_text(encoding="utf-8")
        leftover_tokens(rel, text, errors)
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        for key in REQUIRED_PAGE_KEYS:
            if not fm.get(key):
                errors.append(f"{rel}: missing frontmatter key `{key}`")
        if fm.get("layout") and fm["layout"] != "default":
            errors.append(f"{rel}: layout must be `default`")
        if fm.get("nav_order") and not re.fullmatch(r"-?\d+", fm["nav_order"]):
            errors.append(f"{rel}: nav_order must be an integer")

        parent_title = SECTION_PARENTS.get(Path(rel))
        if parent_title and fm.get("title") and fm["title"] != parent_title:
            errors.append(f"{rel}: title must be `{parent_title}`")
        if parent_title and fm.get("has_children") != "true":
            errors.append(f"{rel}: section parent must set has_children: true")

        body = body_of(text)
        if WIKILINK_RE.search(text):
            errors.append(f"{rel}: contains [[wikilink]]; use relative .md links")
        if re.search(r"\{[:%]", body):
            errors.append(f"{rel}: contains Jekyll '{{:' or '{{%' in body")

        for raw in MD_LINK_RE.findall(text):
            href = raw.strip()
            if href.startswith("/"):
                errors.append(f"{rel}: absolute path link `{href}`")
                continue
            resolved = resolve_link(path, href)
            if resolved is None:
                continue
            if resolved.suffix == ".md" or href.split("#", 1)[0].endswith(".md"):
                if not resolved.is_file():
                    errors.append(f"{rel}: broken link `{href}`")

        if path.name != "catalog.md":
            if path.resolve() not in catalog_set:
                errors.append(f"{rel}: not listed in docs/catalog.md")

    if catalog_path.is_file():
        for raw in MD_LINK_RE.findall(catalog_text):
            resolved = resolve_link(catalog_path, raw)
            if resolved is None:
                continue
            if raw.strip().startswith("/"):
                errors.append(f"docs/catalog.md: absolute path link `{raw}`")
                continue
            target = raw.split("#", 1)[0].split(" ", 1)[0]
            if target.endswith(".md") and not resolved.is_file():
                errors.append(f"docs/catalog.md: broken link `{raw}`")

    pins = root / "docs" / "meta" / "pins.md"
    if pins.is_file():
        pin_text = pins.read_text(encoding="utf-8")
        for page in PIN_PAGE_RE.findall(pin_text):
            pin_target = (root / "docs" / page).resolve()
            if not pin_target.is_file():
                errors.append(f"docs/meta/pins.md: page does not exist: {page}")

    raw_dir = root / "raw" / "sources"
    if raw_dir.is_dir():
        for path in sorted(raw_dir.glob("*.md")):
            rel = path.relative_to(root).as_posix()
            size = path.stat().st_size
            if size > RAW_MAX_BYTES:
                errors.append(f"{rel}: {size} bytes exceeds {RAW_MAX_BYTES} (full scrape?)")
            raw_text = path.read_text(encoding="utf-8")
            leftover_tokens(rel, raw_text, errors)
            raw_fm = parse_frontmatter(raw_text)
            if raw_fm is None:
                errors.append(f"{rel}: missing YAML frontmatter")
            else:
                for key in ("url", "title", "retrieved", "slug"):
                    if not raw_fm.get(key):
                        errors.append(f"{rel}: missing frontmatter key `{key}`")

    for rel in ("LICENSE", "README.md", "AGENTS.md", "_config.yml", "Gemfile"):
        extra = root / rel
        if extra.is_file():
            leftover_tokens(rel, extra.read_text(encoding="utf-8"), errors)

    return errors


def main() -> int:
    start = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    root = find_wiki_root(start)
    if root is None:
        print("error: no WIKI.md above this directory", file=sys.stderr)
        return 2
    errors = lint(root)
    if not errors:
        print(f"ok: {root}")
        return 0
    for e in errors:
        print(e)
    print(f"{len(errors)} error(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
