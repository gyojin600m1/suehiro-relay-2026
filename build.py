#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.json を index.html に差し込むだけ。UIは template.html を触らない。"""
import json, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(io.open(os.path.join(HERE, "data.json"), encoding="utf-8"))

# 検算: 上位4人がリレーメンバー。4位と5位が同着なら選出が確定しないので止める。
for r in data["races"]:
    ok = [x for x in r["results"] if x["status"] == "通常"]
    ranks = [x["rank"] for x in ok]
    if ranks.count(4) > 1:
        raise SystemExit(f"✗ {r['no']} は4位が同着です。上位4人を機械的に決められません。")
    n4 = len([x for x in ok if x["rank"] and x["rank"] <= 4])
    print(f"  {r['no']} {r['gender']}: {len(ok)}名中 上位4人 = {n4}名")

tpl = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = re.sub(r"/\*__DATA__\*/.*?/\*__DATA_END__\*/",
              lambda _: "/*__DATA__*/" + payload + "/*__DATA_END__*/", tpl, flags=re.S)
if html == tpl:
    raise SystemExit("✗ template.html に差し込み口がありません")
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("✓ index.html を書き出しました (%.0f KB)" % (len(html) / 1024))
