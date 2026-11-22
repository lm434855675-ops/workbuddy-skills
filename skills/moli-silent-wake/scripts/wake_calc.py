#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wake_calc.py — 沉默顾客唤醒引擎。退出码 0/1/9。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def _num(v, f):
    s = str(v).strip().replace(",", "").replace("元", "")
    if s.endswith("%"): s = s[:-1].strip()
    for suf in ("天", "日"): 
        if s.endswith(suf): s = s[:-len(suf)].strip(); break
    try: return float(s)
    except ValueError: _die("参数 %s 非法: %r" % (f, v))
def cmd_plan(a):
    try:
        leads = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(leads, list) or not leads:
        _die("输入必须是非空数组（lead/silent_days）")
    avg = _num(a.avg_order, "--avg-order"); m = _num(a.gross_margin, "--gross-margin")
    margin = m / 100 if m > 1 else m
    if not (0 < margin < 1):
        _die("毛利率 0-100%")
    buckets = {"30-59天": [], "60-89天": [], "90天+": []}
    for i, ld in enumerate(leads):
        d = _num(ld.get("silent_days", ld.get("d")), "silent_days")
        lead = str(ld.get("lead", "lead%d" % (i + 1)))
        k = "30-59天" if d < 60 else ("60-89天" if d < 90 else "90天+")
        buckets[k].append({"lead": lead, "silent_days": d})
    strat = {
      "30-59天": {"count": len(buckets["30-59天"]), "action": "价值型触达：新案例+专属券（不降价）", "channel": "企微 1v1"},
      "60-89天": {"count": len(buckets["60-89天"]), "action": "回归礼：大额券（成本 ≤ 毛利 20%）+到店理由", "channel": "企微+短信"},
      "90天+": {"count": len(buckets["90天+"]), "action": "放弃个性化，等大促批量唤醒（一条群发）", "channel": "群发"},
    }
    total = sum(len(v) for v in buckets.values())
    out = {"command": "plan", "inputs": {"leads": total, "avg_order": avg, "gross_margin": margin},
      "buckets": strat, "verdict": "PASS",
      "verdict_note": "回归券红线：单张成本 ≤ 客单毛利的 20%%（即 ≤ %.2f 元）。90 天以上顾客唤醒率通常 <10%%，别烧钱" % (avg * margin * 0.2),
      "rules": ["唤醒顺序 30→60→90（近的先醒）", "一次只发一条，48h 无回复不追发", "唤醒成功当天转 A 级跟进"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="沉默顾客唤醒引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("plan", help="唤醒方案")
    r.add_argument("--file", required=True); r.add_argument("--avg-order", required=True); r.add_argument("--gross-margin", required=True)
    r.set_defaults(func=cmd_plan)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()