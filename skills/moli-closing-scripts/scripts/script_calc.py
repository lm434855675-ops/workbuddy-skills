#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""script_calc.py — 话术校验引擎。四要素：scene/trigger/script/toboo。退出码 0/1/9。"""
import argparse, json, sys

def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg)); sys.exit(code)

FORBIDDEN = ["保证", "百分百", "稳赚", "肯定能", "绝对", "包治", "第一"]

def cmd_check(a):
    if not a.file:
        _die("缺少 --file 话术 JSON")
    try:
        items = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(items, list) or not items:
        _die("输入必须是非空数组（scene/trigger/script/toboo）")
    ok, bad = [], []
    for i, it in enumerate(items):
        scene = str(it.get("scene", "")).strip()
        trigger = str(it.get("trigger", "")).strip()
        script = str(it.get("script", "")).strip()
        toboo = str(it.get("toboo", "")).strip()
        probs = []
        if not scene: probs.append("缺 scene")
        if not trigger: probs.append("缺 trigger(触发条件)")
        if not script: probs.append("缺 script")
        elif "？" not in script and "?" not in script: probs.append("话术无提问（只会说不会问）")
        if not toboo: probs.append("缺 toboo(禁区)")
        else:
            for w in FORBIDDEN:
                if w in script: probs.append("含违禁承诺「%s」（合规红线）" % w); break
        (ok if not probs else bad).append({"no": i + 1, "scene": scene, "trigger": trigger, "script": script, "toboo": toboo, "problems": probs})
    scenes = {}
    for it in ok:
        scenes.setdefault(it["scene"], []).append(it)
    out = {
        "command": "check", "total": len(items), "passed": len(ok), "rejected": len(bad),
        "library": [{"scene": k, "scripts": v} for k, v in scenes.items()],
        "rejected_items": bad,
        "verdict": "PASS" if not bad else "FAIL",
        "verdict_note": ("%d 条话术全部过校验，按 %d 个场景归档" % (len(ok), len(scenes))) if not bad else
                        "%d 条打回：%s" % (len(bad), "；".join("第%d条:%s" % (b["no"], "/".join(b["problems"])) for b in bad)),
        "rules": ["每条话术必须含提问", "违禁承诺直接打回（合规红线）", "异议预埋在成交段后"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser(description="话术校验引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="话术四要素+合规校验")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()