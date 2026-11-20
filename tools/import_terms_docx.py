"""把「中山資管英文術語_A4列印.docx」轉成內建單字庫 data/02_mis_terms.json。

docx 格式：每個主題一個段落標題「主題名稱（數量）」，後面接一張表格，
表頭為 English｜中文｜說明｜考過。

用法（在專案資料夾執行，需要 python-docx）：
    python tools/import_terms_docx.py "D:/雅婷/02學習/空大/修課/中山資管英文術語/中山資管英文術語_A4列印.docx"
    python tools/build.py
"""
import json
import pathlib
import re
import sys

import docx

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "02_mis_terms.json"
HEADING = re.compile(r"^(.+?)（(\d+)）$")


def clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s.replace("\n", " ")).strip()
    return "" if s in ("—", "-", "–") else s


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = docx.Document(sys.argv[1])
    headings = [(m.group(1).strip(), int(m.group(2)))
                for p in d.paragraphs if (m := HEADING.match(p.text.strip()))]
    if len(headings) != len(d.tables):
        sys.exit(f"主題標題有 {len(headings)} 個，表格有 {len(d.tables)} 張，對不起來")

    # 每個術語有固定編號（進度靠編號記錄）：已存在的術語沿用舊編號，新術語接著往後編
    old_ids = {}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        old_ids = {w[0]: i for w, i in zip(old["words"], old.get("ids", range(1, len(old["words"]) + 1)))}
    next_id = max(old_ids.values(), default=0) + 1

    groups, words, ids = [], [], []
    for (name, expected), table in zip(headings, d.tables):
        rows = table.rows
        header = [c.text.strip() for c in rows[0].cells]
        if header[:2] != ["English", "中文"]:
            sys.exit(f"「{name}」的表頭不是 English｜中文：{header}")
        count = 0
        for r in rows[1:]:
            cells = [clean(c.text) for c in r.cells]
            en, zh = cells[0], cells[1]
            if not en or not zh:
                continue
            explain = cells[2] if len(cells) > 2 else ""
            exam = cells[3] if len(cells) > 3 else ""
            if en in old_ids:
                ids.append(old_ids[en])
            else:
                ids.append(next_id)
                next_id += 1
            words.append([en, "", zh, explain, f"考過：{exam}" if exam else ""])
            count += 1
        if count != expected:
            print(f"注意：「{name}」標題寫 {expected} 個，表格讀到 {count} 個")
        groups.append({"name": name, "n": count})

    bank = {
        "id": "mis",
        "name": "中山資管英文術語",
        "source": "中山資管甲組 94–115 學年度考古題",
        "credit": "依中山資管甲組 94–115 學年度考古題整理；「考過」是出現的題號，可以到考古題練習頁找題。",
        "size": 50,
        "groups": groups,
        "ids": ids,
        "words": words,
    }
    if len(set(ids)) != len(ids):
        dup = sorted({w[0] for w, i in zip(words, ids) if ids.count(i) > 1})
        sys.exit(f"有重複的英文術語，請在 docx 裡改成不同寫法：{dup}")
    new = [w[0] for w, i in zip(words, ids) if w[0] not in old_ids] if old_ids else []
    OUT.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"已輸出 {OUT.relative_to(ROOT)}：{len(groups)} 個主題、{len(words)} 個術語")
    if new:
        print(f"新增 {len(new)} 個：{'、'.join(new[:10])}{' …' if len(new) > 10 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
