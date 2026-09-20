#!/usr/bin/env python3
"""Validate the minimal DiamaneOS overlay and resolved Android manifests."""

import argparse
from pathlib import Path, PurePosixPath
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
OVERLAY = ROOT / "diamaneos.xml"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_XML_BYTES = 16 * 1024 * 1024
ALLOWED_OVERLAY_ELEMENTS = {
    "remote", "project", "extend-project", "remove-project",
}


class ManifestError(ValueError):
    """A manifest violates the repository's bounded overlay policy."""


def _root(path: Path) -> ET.Element:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ManifestError(f"cannot read {path}: {exc}") from None
    if len(data) > MAX_XML_BYTES:
        raise ManifestError(f"manifest exceeds {MAX_XML_BYTES} bytes")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ManifestError(f"invalid XML: {exc}") from None
    if root.tag != "manifest":
        raise ManifestError("root element must be manifest")
    return root


def _safe_path(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ManifestError(f"unsafe {label}: {value!r}")
    return value


def _commit(value: str, label: str) -> str:
    if SHA_RE.fullmatch(value or "") is None:
        raise ManifestError(f"{label} must be an exact 40-character commit")
    return value


def validate_overlay(path: Path = OVERLAY) -> None:
    root = _root(path)
    unsupported = sorted({child.tag for child in root
                          if child.tag not in ALLOWED_OVERLAY_ELEMENTS})
    if unsupported:
        raise ManifestError("unsupported overlay elements: "
                            + ", ".join(unsupported))

    remotes = root.findall("remote")
    if len(remotes) != 1:
        raise ManifestError("overlay must declare exactly one remote")
    remote = remotes[0]
    if remote.attrib != {
            "name": "diamaneos",
            "fetch": "https://codeberg.org/DiamaneOS/"}:
        raise ManifestError("overlay remote must be the canonical DiamaneOS remote")

    names = set()
    paths = set()
    for project in root.findall("project"):
        name = project.get("name", "")
        checkout = _safe_path(project.get("path", ""), "project path")
        if not name:
            raise ManifestError("project name is required")
        if project.get("remote") != "diamaneos":
            raise ManifestError(f"project {name} must use the diamaneos remote")
        _commit(project.get("revision", ""), f"project {name} revision")
        if name in names:
            raise ManifestError(f"duplicate project name: {name}")
        if checkout in paths:
            raise ManifestError(f"duplicate project path: {checkout}")
        names.add(name)
        paths.add(checkout)

    extensions = set()
    for project in root.findall("extend-project"):
        name = project.get("name", "")
        if not name:
            raise ManifestError("extend-project name is required")
        if project.get("remote") != "diamaneos":
            raise ManifestError(
                f"extend-project {name} must select the diamaneos remote")
        _commit(project.get("revision", ""),
                f"extend-project {name} revision")
        if project.get("path"):
            _safe_path(project.get("path", ""), "extend-project path")
        if name in extensions:
            raise ManifestError(f"duplicate extend-project name: {name}")
        extensions.add(name)

    removals = set()
    for project in root.findall("remove-project"):
        name = project.get("name", "")
        if not name:
            raise ManifestError("remove-project name is required")
        if name in removals:
            raise ManifestError(f"duplicate remove-project name: {name}")
        removals.add(name)


def validate_resolved(path: Path) -> int:
    root = _root(path)
    projects = root.findall("project")
    if not projects:
        raise ManifestError("resolved manifest contains no projects")
    paths = set()
    for project in projects:
        name = project.get("name", "")
        if not name:
            raise ManifestError("resolved project name is required")
        checkout = _safe_path(project.get("path", name),
                              "resolved project path")
        _commit(project.get("revision", ""),
                f"resolved project {name} revision")
        if checkout in paths:
            raise ManifestError(f"duplicate resolved project path: {checkout}")
        paths.add(checkout)
    return len(projects)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="validate the committed DiamaneOS overlay")
    mode.add_argument("--resolved", type=Path,
                      help="validate immutable revisions in repo manifest -r output")
    args = parser.parse_args(argv)
    try:
        if args.check:
            validate_overlay()
            print("overlay: valid; no floating upstream revision authority")
        else:
            count = validate_resolved(args.resolved)
            print(f"resolved manifest: {count} projects, immutable revisions, "
                  "unique paths")
    except ManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
