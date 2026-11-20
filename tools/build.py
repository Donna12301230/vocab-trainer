"""把 data/*.json 的內建單字庫打包進 src/template.html，輸出 index.html。

用法（在專案資料夾執行）：
    python tools/build.py

data/ 裡每個 .json 檔是一個內建單字庫，格式：
    {
      "id": "tsl",                 # 英數代號，不可重複；改了會讓舊進度對不上
      "name": "TSL 多益 1250",      # 顯示名稱
      "size": 50,                  # 每組幾個字（沒有 groups 時依這個數量切組）
      "groups": [{"name": "主題", "n": 26}, ...],  # 可省略；依主題分組，n 加總要等於單字數
      "ids": [1, 2, ...],          # 可省略；每個字的固定編號（進度靠它記錄），省略時用順序 1, 2, 3…
      "source": "TOEIC Service List 1.2",   # 可省略
      "credit": "資料來源與授權說明",          # 可省略，顯示在首頁底部
      "words": [["英文", "詞性", "中文", "說明", "備註（可省略）"], ...]
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
FB_PLACEHOLDER = "/*__FIREBASE__*/null"


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
            if not (isinstance(w, list) and len(w) in (4, 5) and w[0] and w[2]):
                sys.exit(f"{path.name} 第 {i + 1} 個單字格式不對：{w!r}")
        if "ids" in bank:
            ids_ = bank["ids"]
            if len(ids_) != len(bank["words"]) or len(set(ids_)) != len(ids_) or not all(isinstance(i, int) and i > 0 for i in ids_):
                sys.exit(f"{path.name} 的 ids 必須是和單字數一樣多、不重複的正整數")
        if "groups" in bank:
            total = sum(g["n"] for g in bank["groups"])
            if total != len(bank["words"]) or not all(g.get("name") and g["n"] > 0 for g in bank["groups"]):
                sys.exit(f"{path.name} 的 groups 數量加總 {total} 和單字數 {len(bank['words'])} 不一致")
        banks.append(bank)
        groups = f"，{len(bank['groups'])} 個主題" if "groups" in bank else ""
        print(f"  {path.name}: {bank['name']}，{len(bank['words'])} 字{groups}")
    if not banks:
        sys.exit("data/ 裡沒有單字庫")

    html = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        sys.exit("template.html 找不到資料插入點")
    data = json.dumps(banks, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = html.replace(PLACEHOLDER, data)

    # 雲端同步：有 firebase-config.json 才開啟（這組設定本來就是公開的，安全性靠 firestore.rules）
    fb = ROOT / "firebase-config.json"
    if fb.exists() and FB_PLACEHOLDER in html:
        cfg = json.loads(fb.read_text(encoding="utf-8"))
        html = html.replace(FB_PLACEHOLDER, json.dumps(cfg, separators=(",", ":")))
        print(f"  雲端同步：Firebase 專案 {cfg.get('projectId')}")
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"已輸出 {OUT.name}（{OUT.stat().st_size // 1024} KB）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
