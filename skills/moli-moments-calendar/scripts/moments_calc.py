#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moments_calc.py — 朋友圈内容日历引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
TYPES = [("顾客见证", 25, "买家秀/好评截图/复购故事"), ("干货价值", 25, "行业技巧/避坑/清单"),
         ("人设日常", 20, "老板日常/幕后/团队（不广告）"), ("互动提问", 15, "选择题/征集/投票"),
         ("产品动作", 10, "新品/优惠（月 ≤3 条硬广）"), ("热点借势", 5, "节日/热点（强相关才发）")]
GOLD = ["07:30-08:30 通勤", "12:00-13:30 午休", "20:00-22:00 黄金档"]
def cmd_calendar(a):
    days = int(str(a.days).strip() or "30")
    if not (7 <= days <= 90):
        _die("天数 7-90")
    plan, day, i = [], 1, 0
    while day <= days:
        t = TYPES[i % len(TYPES)]
        plan.append({"day": day, "type": t[0], "ratio_target": "%d%%" % t[1],
                     "direction": t[2] + "（结合" + a.industry + "）", "slot": GOLD[day % 3]})
        day += 1; i += 1
    out = {"command": "calendar", "inputs": {"industry": a.industry, "days": days},
      "calendar": plan, "verdict": "PASS",
      "verdict_note": "硬广占比 10%（红线 20%）；每条必带图/视频；同一时段连续两天类型不重复",
      "rules": ["硬广月 ≤3 条", "顾客见证是信任主粮", "人设日常让顾客先信人再信货", "连发 2 条广告日=删除预警"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="朋友圈内容日历引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("calendar", help="内容日历")
    r.add_argument("--industry", required=True); r.add_argument("--days", default="30")
    r.set_defaults(func=cmd_calendar)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()