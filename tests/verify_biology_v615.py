#!/usr/bin/env python3
import gzip, hashlib, json, sqlite3, sys, tempfile
from pathlib import Path
BASE_SHA = "d63219dd6f1621644df495f6b195763924b5c282961cfecf544f7541ab3b673c"
PATCHED_SHA = "00f881e78e26326532b8b771134970052ddb296fc0e556ab30a980c95656ef14"
PATCH_SHA = "3943af9a9d83872c846c7458fae330184be44b7b1aead7502f1c2620c99ebb5d"
root = Path(__file__).resolve().parents[1]
asset = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "app/src/main/assets/radiology1405_bank_v6_1.db.gz"
patch_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "app/src/main/assets/biology_v615_patch.json"
assert hashlib.sha256(asset.read_bytes()).hexdigest() == "b5f47e9803638a37798be398ff4a087f336aafa78470e6f5ad94ac3aa5d7fe14"
assert hashlib.sha256(patch_path.read_bytes()).hexdigest() == PATCH_SHA
patch = json.loads(patch_path.read_text(encoding="utf-8"))
assert patch["base_db_sha256"] == BASE_SHA and patch["patched_db_sha256"] == PATCHED_SHA
with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
    tmp.write(gzip.decompress(asset.read_bytes())); tmp.flush()
    assert hashlib.sha256(Path(tmp.name).read_bytes()).hexdigest() == BASE_SHA
    conn = sqlite3.connect(tmp.name)
    try:
        for update in patch["updates"]:
            raw, = conn.execute("SELECT full_json FROM question WHERE id=?", (update["id"],)).fetchone()
            question = json.loads(raw); question.update(update["fields"])
            conn.execute("UPDATE question SET source_type=?, full_json=? WHERE id=?", (update["source_type"], json.dumps(question, ensure_ascii=False, separators=(",", ":")), update["id"]))
        conn.commit()
        assert conn.execute("PRAGMA quick_check").fetchone()[0] == "ok"
        assert conn.execute("SELECT COUNT(*) FROM question").fetchone()[0] == 1216
        assert conn.execute("SELECT COUNT(*) FROM question WHERE source_type='real_exam'").fetchone()[0] == 17
        assert conn.execute("SELECT COUNT(*) FROM question WHERE source_type='official_exam_stem_training'").fetchone()[0] == 71
    finally: conn.close()
    assert hashlib.sha256(Path(tmp.name).read_bytes()).hexdigest() == PATCHED_SHA
print("BIOLOGY_V615_COMPACT_PATCH_OK")
