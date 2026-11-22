#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""meeting_calc.py — 行动项校验引擎。四要素：task/owner/deadline/criterion。退出码 0/1/9。"""
import argparse, json, sys, re

def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg)); sys.exit(code)

BLACKLIST = ["尽快", "后续", "相关同事", "尽快推进", "待定", "TBD", "有人"]

def cmd_actions(a):
    if not a.file:
        _die("缺少 --file 行动项 JSON")
    try:
        items = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(items, list) or not items:
        _die("输入必须是非空数组（task/owner/deadline/criterion）")
    ok, bad = [], []
    for i, it in enumerate(items):
        task = str(it.get("task", "")).strip()
        owner = str(it.get("owner", "")).strip()
        deadline = str(it.get("deadline", "")).strip()
        crit = str(it.get("criterion", "")).strip()
        probs = []
        if not task: probs.append("缺 task")
        if not owner: probs.append("缺 owner")
        elif any(b in owner for b in ["相关", "有人", "团队", "大家"]): probs.append("owner 是黑话（%s）" % owner)
        if not deadline: probs.append("缺 deadline")
        elif not re.search(r"\d", deadline): probs.append("deadline 无具体日期（%s）" % deadline)
        if any(b in deadline for b in BLACKLIST[:4]): probs.append("deadline 是黑话（%s）" % deadline)
        if not crit: probs.append("缺 criterion(验收标准)")
        (ok if not probs else bad).append({"no": i + 1, "task": task, "owner": owner, "deadline": deadline, "criterion": crit, "problems": probs})
    out = {
        "command": "actions", "total": len(items), "passed": len(ok), "rejected": len(bad),
        "tracker": ok, "rejected_items": bad,
        "verdict": "PASS" if not bad else "FAIL",
        "verdict_note": ("%d 条行动项全部四要素齐全，可直接发追踪表" % len(ok)) if not bad else
                        "%d 条不合格打回重写：%s。不合格条目不入追踪表" % (len(bad), "；".join("第%d条:%s" % (b["no"], "/".join(b["problems"])) for b in bad)),
        "rules": ["四要素缺一不可", "追踪表 24h 内发出", "下次会议第一议程=过追踪表"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser(description="会议行动项校验引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("actions", help="行动项四要素校验")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_actions)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()