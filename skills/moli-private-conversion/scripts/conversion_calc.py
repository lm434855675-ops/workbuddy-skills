#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conversion_calc.py — moli-private-conversion 测算引擎（capacity / gmv / rhythm）。

用法:
    python3 conversion_calc.py capacity --daily-leads 1500 --staff 20 --per-staff-hourly 8 --work-hours 8 --response-rate 0.7
    python3 conversion_calc.py gmv --daily-leads 1500 --response-rate 0.7 --deep-rate 0.4 --close-rate 0.12 --aov 599 --repurchase 1.6
    python3 conversion_calc.py rhythm --cycle 14 --touch-points 6 --key-days "1,3,7,10,12,14"

退出码: 0 成功; 1 参数错误; 2 测算无解。
"""
import argparse
import json
import sys


def die(code, msg):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def out(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for k, v in data.items():
            print("%s: %s" % (k, v))


def _rate(s, name):
    try:
        v = float(s)
    except ValueError:
        die(1, "%s 必须是数字: %r" % (name, s))
    if not (0 < v <= 1):
        die(2, "%s 须在 (0,1]: %r" % (name, v))
    return v


def cmd_capacity(args):
    if args.staff <= 0:
        die(2, "客服人数必须 > 0")
    rr = _rate(args.response_rate, "response-rate")
    cap = args.staff * args.per_staff_hourly * args.work_hours * rr
    gap = args.daily_leads - cap
    gap_pct = gap / cap if cap else 0
    if gap <= 0:
        action = "承载力充足，重点优化话术转化率"
    elif gap_pct <= 0.2:
        action = "缺口20%以内：优先话术提效，不加人"
    elif gap_pct <= 1.0:
        action = "缺口20-100%：高峰增援+低意向分流，暂缓进线投放"
    else:
        action = "缺口超100%：结构性缺口，放缓进线投放，扩团队/上自动化承接"
    result = {
        "日进线": args.daily_leads,
        "日承接上限": round(cap, 0),
        "缺口": round(gap, 0),
        "缺口比例": "%.0f%%" % (gap_pct * 100),
        "决策": action,
        "人均日处理": round(cap / args.staff, 1),
    }
    out(result, args.json)


def cmd_gmv(args):
    rr = _rate(args.response_rate, "response-rate")
    dr = _rate(args.deep_rate, "deep-rate")
    cr = _rate(args.close_rate, "close-rate")
    if args.aov <= 0:
        die(1, "客单价必须 > 0")
    if args.repurchase < 1:
        die(2, "复购系数须 ≥1")
    responded = args.daily_leads * rr
    deep = responded * dr
    orders = deep * cr
    gmv = orders * args.aov
    ltv_gmv = gmv * args.repurchase
    result = {
        "日响应进线": round(responded, 0),
        "日深聊": round(deep, 0),
        "日成交单": round(orders, 1),
        "日GMV": round(gmv, 0),
        "月GMV(30天)": round(gmv * 30, 0),
        "年GMV(含复购系数%.1f)" % args.repurchase: round(ltv_gmv * 365, 0),
        "口径": "基于输入假设测算，不构成业绩承诺；假设须用真实漏斗数据校准",
    }
    out(result, args.json)


def cmd_rhythm(args):
    if args.cycle < 1 or args.touch_points < 1:
        die(1, "周期与触达点数必须 ≥1")
    if args.touch_points > args.cycle:
        die(2, "触达点数(%d)不能超过周期天数(%d)" % (args.touch_points, args.cycle))
    days = [int(x) for x in args.key_days.split(",") if x.strip()]
    if len(days) != args.touch_points:
        die(1, "key-days 数量(%d)与 touch-points(%d) 不一致" % (len(days), args.touch_points))
    if days != sorted(days) or days[0] < 1 or days[-1] > args.cycle:
        die(2, "key-days 须升序且落在 [1, cycle] 内")
    gaps = [days[i + 1] - days[i] for i in range(len(days) - 1)]
    min_gap = min(gaps) if gaps else None
    result = {
        "周期": args.cycle,
        "触达排布": days,
        "间隔天数": gaps,
        "最紧间隔": min_gap,
        "节奏判定": "合理" if (min_gap is None or min_gap >= 2) else "过密：相邻触达<2天，有骚扰风险，重排",
    }
    out(result, args.json)
    if min_gap is not None and min_gap < 2:
        die(2, "触达过密：相邻间隔 %d 天 < 2 天，有骚扰风险" % min_gap)


def main():
    ap = argparse.ArgumentParser(description="moli-private-conversion calc engine")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("capacity")
    p.add_argument("--daily-leads", type=float, required=True)
    p.add_argument("--staff", type=float, required=True)
    p.add_argument("--per-staff-hourly", type=float, required=True)
    p.add_argument("--work-hours", type=float, required=True)
    p.add_argument("--response-rate", required=True)
    p.set_defaults(fn=cmd_capacity)

    p = sub.add_parser("gmv")
    p.add_argument("--daily-leads", type=float, required=True)
    p.add_argument("--response-rate", required=True)
    p.add_argument("--deep-rate", required=True)
    p.add_argument("--close-rate", required=True)
    p.add_argument("--aov", type=float, required=True)
    p.add_argument("--repurchase", type=float, default=1.0)
    p.set_defaults(fn=cmd_gmv)

    p = sub.add_parser("rhythm")
    p.add_argument("--cycle", type=int, required=True)
    p.add_argument("--touch-points", type=int, required=True)
    p.add_argument("--key-days", required=True)
    p.set_defaults(fn=cmd_rhythm)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
