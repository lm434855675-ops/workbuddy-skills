#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""followup_calc.py — 客户分级与跟进排期计算引擎。退出码 0/1/9。"""
import argparse, json, sys

def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg)); sys.exit(code)

def _num(v, field):
    if v is None: _die("缺少字段 %s" % field)
    s = str(v).strip().replace(",", "")
    if not s: _die("字段 %s 为空" % field)
    for suf in ("天", "日", "元"):
        if s.endswith(suf): s = s[:-len(suf)].strip(); break
    try: return float(s)
    except ValueError: _die("字段 %s 不是合法数字: %r" % (field, v))

CADENCE = {"A": {"interval": 3, "channel": "企微 1v1 + 电话", "rule": "内容六选一轮换，纯催单不计入"},
           "B": {"interval": 7, "channel": "企微 + 朋友圈", "rule": "价值内容为主，优惠每月 ≤1 次"},
           "C": {"interval": 14, "channel": "群发 + 朋友圈", "rule": "3 轮无反应转沉默池"}}

def cmd_grade(a):
    if not a.file: _die("缺少 --file 客户 JSON")
    try:
        leads = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(leads, list) or not leads:
        _die("输入必须是非空数组（lead/heat/last_touch_days/status）")
    out, overdue = [], []
    for i, ld in enumerate(leads):
        lead = str(ld.get("lead", "lead%d" % (i + 1)))
        heat = _num(ld.get("heat", ld.get("h")), "heat")
        last = _num(ld.get("last_touch_days", ld.get("t")), "last_touch_days")
        status = str(ld.get("status", "咨询过")).strip()
        if not (0 <= heat <= 100): _die("leads[%d] heat 应为 0-100" % i)
        tier = "A" if heat >= 70 else ("B" if heat >= 40 else "C")
        interval = CADENCE[tier]["interval"]
        od = last - interval
        is_overdue = od > 0
        if is_overdue:
            overdue.append({"lead": lead, "tier": tier, "overdue_days": round(od, 1)})
        out.append({"lead": lead, "tier": tier, "heat": heat, "status": status,
                    "interval_days": interval, "channel": CADENCE[tier]["channel"],
                    "overdue": is_overdue, "overdue_days": round(max(od, 0), 1)})
    tiers = {}
    for o in out: tiers.setdefault(o["tier"], []).append(o)
    summary = [{"tier": k, "count": len(v), "interval": CADENCE[k]["interval"],
                "channel": CADENCE[k]["channel"], "rule": CADENCE[k]["rule"],
                "overdue": sum(1 for x in v if x["overdue"])} for k, v in sorted(tiers.items())]
    out2 = {
        "command": "grade", "inputs": {"leads": len(leads)},
        "tiers": summary, "roster": out,
        "overdue_list": sorted(overdue, key=lambda x: -x["overdue_days"]),
        "verdict": "PASS",
        "verdict_note": "逾期跟进 %d 人（A级逾期优先电话兜底）。C 级 3 轮无反应转沉默池，大促批量唤醒" % len(overdue),
        "rules": ["A 3天/B 7天/C 14天，逾期当天预警", "每次跟进带价值，纯催单不计入", "A级逾期2次电话兜底"],
    }
    print(json.dumps(out2, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser(description="客户分级与跟进排期引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("grade", help="客户分级 + 跟进排期 + 逾期预警")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_grade)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()