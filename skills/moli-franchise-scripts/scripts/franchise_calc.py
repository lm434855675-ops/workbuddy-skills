#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""franchise_calc.py - 招商话术合规校验引擎。退出码 0/1/9。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
FORBIDDEN = ["稳赚", "保本", "躺赚", "零风险", "保证回本", "肯定赚钱", "稳赚不赔", "躺着赚钱", "闭眼赚"]
def cmd_check(a):
    try:
        items = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(items, list) or not items:
        _die("输入必须是非空数组（scene/script/toboo）")
    ok, bad = [], []
    for i, it in enumerate(items):
        scene = str(it.get("scene", "")).strip()
        script = str(it.get("script", "")).strip()
        toboo = str(it.get("toboo", "")).strip()
        probs = []
        if not scene: probs.append("缺 scene")
        if not script: probs.append("缺 script")
        else:
            for w in FORBIDDEN:
                if w in script:
                    probs.append("含收益承诺「%s」（商业特许经营红线+广告法风险）" % w); break
            if ("？" not in script) and ("?" not in script):
                probs.append("话术无提问（单向输出无互动）")
        if not toboo: probs.append("缺 toboo(禁区)")
        (ok if not probs else bad).append({"no": i + 1, "scene": scene, "script": script, "toboo": toboo, "problems": probs})
    out = {"command": "check", "total": len(items), "passed": len(ok), "rejected": len(bad),
      "passed_items": ok, "rejected_items": bad,
      "verdict": "PASS" if not bad else "FAIL",
      "verdict_note": ("%d 条招商话术过合规校验" % len(ok)) if not bad else
                      "%d 条打回：%s" % (len(bad), "；".join("第%d条:%s" % (b["no"], "/".join(b["problems"])) for b in bad)),
      "rules": ["收益类表述只讲测算逻辑不讲承诺", "回本口径=已签约门店实测区间，非保证", "签约动作二选一+期限"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="招商话术合规校验引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="招商话术合规校验")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()