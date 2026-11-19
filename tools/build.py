"""把 data/*.json 的內建單字庫打包進 src/template.html，輸出 index.html。

用法（在專案資料夾執行）：
    python tools/build.py

data/ 裡每個 .json 檔是一個內建單字庫，格式：
    {
      "id": "tsl",                 # 英數代號，不可重複；改了會讓舊進度對不上
      "name": "TSL 多益 1250",      # 顯示名稱
      "size": 50,                  # 每組幾個字
      "source": "TOEIC Service List 1.2",   # 可省略
      "credit": "資料來源與授權說明",          # 可省略，顯示在首頁底部
      "words": [["英文", "詞性", "中文", "英英解釋"], ...]
    }
檔名排序決定顯示順序（例如 01_tsl.json、02_xxx.json），第一個是預設單字庫。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "template.html"
OUT = ROOT / "index.html"
PLACEHOLDER = "/*__BANKS__*/[]"


def main() -> int:
    banks = []
    ids = set()
    for path in sorted((ROOT / "data").glob("*.json")):
        bank = json.loads(path.read_text(encoding="utf-8"))
        for key in ("id", "name", "words"):
            if key not in bank:
                sys.exit(f"{path.name} 缺少欄位：{key}")
        if bank["id"] in ids:
            sys.exit(f"{path.name} 的 id 重複：{bank['id']}")
        ids.add(bank["id"])
        bank.setdefault("size", 50)
        for i, w in enumerate(bank["words"]):
            if not (isinstance(w, list) and len(w) == 4 and w[0] and w[2]):
                sys.exit(f"{path.name} 第 {i + 1} 個單字格式不對：{w!r}")
        banks.append(bank)
        print(f"  {path.name}: {bank['name']}，{len(bank['words'])} 字")
    if not banks:
        sys.exit("data/ 裡沒有單字庫")

    html = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        sys.exit("template.html 找不到資料插入點")
    data = json.dumps(banks, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(html.replace(PLACEHOLDER, data), encoding="utf-8", newline="\n")
    print(f"已輸出 {OUT.name}（{OUT.stat().st_size // 1024} KB）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
