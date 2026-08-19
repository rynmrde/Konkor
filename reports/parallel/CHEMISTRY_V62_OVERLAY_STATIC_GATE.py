#!/usr/bin/env python3
"""Static integration gate for the v6.2 Chemistry overlay applied after V6.1.4."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: verify_v620_overlay.py INTEGRATED_PROJECT")
root = Path(sys.argv[1])
asset_old = root / "app/src/main/assets/radiology1405_bank_v6_1.db.gz"
asset_new = root / "app/src/main/assets/radiology1405_bank_v6_2.db.gz"
bank_store = root / "app/src/main/java/com/radiology1405/prep/data/BankStore.kt"
progress = root / "app/src/main/java/com/radiology1405/prep/data/ProgressDatabase.kt"

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

checks = {
    "archived v6.1 asset remains": asset_old.exists(),
    "v6.2 asset exists": asset_new.exists(),
    "v6.2 gzip hash": asset_new.exists() and digest(asset_new) == "47ba0670e5c3b22e5823dfb577ade40267f530fd40f7d4a2b8c8119b9f67cbce",
    "BankStore opens v6.2 asset": bank_store.exists() and all(token in bank_store.read_text(encoding="utf-8") for token in ("radiology1405_bank_v6_2.db", "ed84693259455e6da488af23a7fa39c6548ea64e95bee6a93ba5cedf8f7656c6", "EXPECTED_QUESTIONS = 1221", "EXPECTED_AUTHORED = 1117")),
    "separate progress database remains": progress.exists() and "radiology1405_progress_v6.db" in progress.read_text(encoding="utf-8"),
    "no destructive Room migration": progress.exists() and "fallbackToDestructiveMigration" not in progress.read_text(encoding="utf-8"),
}
for name, okay in checks.items():
    print(f"{'PASS' if okay else 'FAIL'} {name}")
if not all(checks.values()):
    raise SystemExit(1)
