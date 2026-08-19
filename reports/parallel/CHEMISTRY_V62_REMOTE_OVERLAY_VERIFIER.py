#!/usr/bin/env python3
"""Reconstruct and verify the exact overlay parts on the committed worker branch."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tarfile
from pathlib import Path
from urllib.request import urlopen

if len(sys.argv) != 2:
    raise SystemExit("usage: verify_remote_overlay_raw.py OUTPUT_DIR")
out_dir = Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)
commit = "b68754b96c1ab495a8ce86fc6e4d89b6d46c7c87"
base = f"https://raw.githubusercontent.com/rynmrde/Konkor/{commit}/radiology_v620_chemistry_patch"
parts: list[Path] = []
for index in range(8):
    name = f"overlay.tar.xz.part{index:02d}"
    path = out_dir / name
    with urlopen(f"{base}/{name}", timeout=60) as response, path.open("wb") as output:
        shutil.copyfileobj(response, output)
    parts.append(path)
archive = out_dir / "overlay.tar.xz"
with archive.open("wb") as output:
    for part in parts:
        with part.open("rb") as source:
            shutil.copyfileobj(source, output)
expected = "1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502"
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
if digest != expected:
    raise SystemExit(f"SHA mismatch: {digest}")
with tarfile.open(archive, "r:xz") as tar:
    names = tar.getnames()
required = {".", "./README.md", "./app/src/main/assets/radiology1405_bank_v6_2.db.gz", "./app/src/main/java/com/radiology1405/prep/data/BankStore.kt"}
if not required <= set(names):
    raise SystemExit(f"missing members: {sorted(required - set(names))}")
report = {"commit": commit, "parts": [part.stat().st_size for part in parts], "sha256": digest, "members": names}
(out_dir / "remote_overlay_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"commit": commit, "parts": len(parts), "sha256": digest, "members": len(names)}))
