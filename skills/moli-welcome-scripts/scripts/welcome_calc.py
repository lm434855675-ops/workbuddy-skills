#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""welcome_calc.py — 欢迎语四要素校验引擎。退出码 0/1/9。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def cmd_check(a):
    try:
        items = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(items, list) or not items:
        _die("输入必须是非空数组（scene/welcome）")
    ok, bad = [], []
    for i, it in enumerate(items):
        scene = str(it.get("scene", "")).strip()
        w = str(it.get("welcome", "")).strip()
        probs = []
        if not scene: probs.append("缺 scene")
        if not w: probs.append("缺 welcome")
        else:
            if ("欢迎" not in w) and ("你好" not in w) and ("您好" not in w):
                probs.append("缺身份开场（欢迎/你好）")
            hook_ok = any(x in w for x in ("领", "送", "券", "礼"))
            if not hook_ok: probs.append("缺钩子（领/送/券/礼）")
            act_ok = any(x in w for x in ("点击", "回复", "领取"))
            if not act_ok: probs.append("缺行动指令（点击/回复/领取）")
        (ok if not probs else bad).append({"no": i + 1, "scene": scene, "welcome": w, "problems": probs})
    out = {"command": "check", "total": len(items), "passed": len(ok), "rejected": len(bad),
      "passed_items": ok, "rejected_items": bad,
      "verdict": "PASS" if not bad else "FAIL",
      "verdict_note": ("%d 条欢迎语过四要素校验（身份+钩子+行动），可直接配置" % len(ok)) if not bad else
                      "%d 条打回：%s" % (len(bad), "；".join("第%d条:%s" % (b["no"], "/".join(b["problems"])) for b in bad)),
      "rules": ["欢迎语 3 行内讲完", "钩子即时兑现", "行动指令唯一（只让做一件事）"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="欢迎语校验引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="欢迎语四要素校验")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()