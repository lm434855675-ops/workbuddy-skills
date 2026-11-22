#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""weekly_calc.py — 私域内容周历引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
WEEK = [("周一", "干货", "行业技巧/清单"), ("周二", "案例", "顾客见证+数据"), ("周三", "互动", "提问/征集/投票"),
        ("周四", "干货或产品", "深度内容或新品（硬广 ≤1/周）"), ("周五", "优惠或邀请", "周末活动预告（唯一硬广位）"),
        ("周六", "人设日常", "老板幕后/探店"), ("周日", "轻互动", "投票/征集下周想看什么")]
def cmd_week(a):
    ch = [c.strip() for c in str(a.channels).split(",") if c.strip()]
    out = {"command": "week", "inputs": {"industry": a.industry, "channels": ch},
      "week": [{"day": d, "type": t, "direction": dr + "（结合" + a.industry + "）", "channels": ch} for d, t, dr in WEEK],
      "verdict": "PASS",
      "verdict_note": "硬广位每周仅 1 个（周五）。广告占比红线 20%，超了顾客屏蔽你",
      "rules": ["硬广周 ≤1 条", "干货/案例/人设占 70%+", "每周日晚固定收集下周选题"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="私域内容周历引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("week", help="一周内容周历")
    r.add_argument("--industry", required=True); r.add_argument("--channels", required=True)
    r.set_defaults(func=cmd_week)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()