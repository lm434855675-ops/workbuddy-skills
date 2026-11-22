#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
member_calc.py — moli-member-activity 测算引擎（increment / conflict / offline）。

用法:
    python3 member_calc.py increment --members 126000 --high-value-rate 15% --reach-rate 60% --open-rate 12% --order-rate 8% --aov 168 --gross-margin-rate 45% --discount-rate 12% --reach-cost 0.045 --baseline-daily-gmv 38000 --days 3
    python3 member_calc.py conflict --benefits "生日券,每年度一次,20元,全品类" --benefits "会员日券,每月一次,30元,全品类" --new "周年庆券,一次性,50元,全品类"
    python3 member_calc.py offline --invited 120 --attend-rate 70% --deal-rate 25% --aov 5000

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
    s = str(s).strip()
    try:
        if s.endswith("%"):
            v = float(s[:-1]) / 100.0
        else:
            v = float(s)
    except ValueError:
        die(1, "%s 必须是数字或百分数: %r" % (name, s))
    if not (0 < v <= 1):
        die(2, "%s 须在 (0,1]: %r" % (name, s))
    return v


def _benefit(spec):
    parts = [p.strip() for p in spec.split(",")]
    if len(parts) != 4:
        die(1, "--benefits/--new 需 4 段: 名称,频次,金额,适用范围。实际: %r" % spec)
    try:
        amount = float(parts[2].replace("元", ""))
    except ValueError:
        die(1, "金额必须是数字(可带'元'): %r" % parts[2])
    return {"名称": parts[0], "频次": parts[1], "金额": amount, "范围": parts[3]}


def cmd_increment(args):
    gm = _rate(args.gross_margin_rate, "gross-margin-rate")
    disc = _rate(args.discount_rate, "discount-rate")
    if disc >= gm:
        die(2, "让利率 %s ≥ 毛利率 %s，必亏" % (disc, gm))
    if args.aov <= 0:
        die(1, "客单价必须 > 0")
    hv = _rate(args.high_value_rate, "high-value-rate")
    reach = _rate(args.reach_rate, "reach-rate")
    openr = _rate(args.open_rate, "open-rate")
    order = _rate(args.order_rate, "order-rate")
    reach_cost = _rate(args.reach_cost, "reach-cost")
    members = args.members
    hv_members = members * hv
    base_members = members - hv_members
    # 分层测算：高价值档客单x2、让利x0.5、转化x1.5（经验系数，可校准）
    gmv_hv = hv_members * reach * openr * order * 1.5 * (args.aov * 2)
    gmv_base = base_members * reach * openr * order * args.aov
    gmv = gmv_hv + gmv_base
    baseline = args.baseline_daily_gmv * args.days
    discount_cost = gmv * disc
    reach_cost = members * reach * reach_cost
    total_cost = discount_cost + reach_cost
    incremental = gmv - baseline
    inc_profit = incremental * gm - total_cost
    roi = inc_profit / total_cost if total_cost else 0
    result = {
        "高价值会员数": round(hv_members, 0),
        "预估活动GMV": round(gmv, 0),
        "平日基线GMV": round(baseline, 0),
        "增量GMV(扣基线)": round(incremental, 0),
        "权益让利成本": round(discount_cost, 0),
        "触达成本": round(reach_cost, 0),
        "总成本": round(total_cost, 0),
        "增量利润": round(inc_profit, 0),
        "ROI": "%.2f" % roi,
        "保本下单转化率": "%.2f%%" % ((total_cost / (args.aov * gm) / max(members * reach, 1)) * 100),
        "口径": "分层系数为经验值(高价值客单x2/转化x1.5)，须用真实分层数据校准；不构成业绩承诺",
    }
    out(result, args.json)


def cmd_conflict(args):
    benefits = [_benefit(b) for b in args.benefits]
    new = _benefit(args.new)
    problems = []
    # 同范围叠加金额检查
    same_scope = [b for b in benefits if b["范围"] == new["范围"]]
    if same_scope:
        total = new["金额"] + sum(b["金额"] for b in same_scope)
        if total > 100:
            problems.append("同范围(%s)可叠加金额 %.0f 元超 100 元红线" % (new["范围"], total))
        overlap = [b["名称"] for b in same_scope]
        problems.append("新权益与 %s 适用范围重叠(%s)，需确认是否互斥" % ("、".join(overlap), new["范围"]))
    # 频次检查
    freq_words = ("每天", "每周")
    if any(w in new["频次"] for w in freq_words):
        problems.append("新权益频次为'%s'，高频权益易被薅且成本不可控" % new["频次"])
    verdict = "必改" if any("超" in p or "高频" in p for p in problems) else "建议"
    out({"新权益": new, "存量权益": benefits, "结论": verdict, "问题": problems}, args.json)
    sys.exit(2 if verdict == "必改" else 0)


def cmd_offline(args):
    ar = _rate(args.attend_rate, "attend-rate")
    dr = _rate(args.deal_rate, "deal-rate")
    if args.aov <= 0:
        die(1, "客单价必须 > 0")
    attendees = args.invited * ar
    deals = attendees * dr
    gmv = deals * args.aov
    result = {
        "邀约人数": args.invited,
        "预估到场": round(attendees, 0),
        "预估成交单": round(deals, 0),
        "预估现场GMV": round(gmv, 0),
        "经验参照": "到场率≥65%、成交率≥20%、48小时跟进覆盖率100%",
        "口径": "预估基于输入假设，须用历史活动数据校准",
    }
    out(result, args.json)


def main():
    ap = argparse.ArgumentParser(description="moli-member-activity calc engine")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("increment")
    p.add_argument("--members", type=float, required=True)
    p.add_argument("--high-value-rate", required=True)
    p.add_argument("--reach-rate", required=True)
    p.add_argument("--open-rate", required=True)
    p.add_argument("--order-rate", required=True)
    p.add_argument("--aov", type=float, required=True)
    p.add_argument("--gross-margin-rate", required=True)
    p.add_argument("--discount-rate", required=True)
    p.add_argument("--reach-cost", required=True)
    p.add_argument("--baseline-daily-gmv", type=float, required=True)
    p.add_argument("--days", type=float, required=True)
    p.set_defaults(fn=cmd_increment)

    p = sub.add_parser("conflict")
    p.add_argument("--benefits", action="append", required=True)
    p.add_argument("--new", required=True)
    p.set_defaults(fn=cmd_conflict)

    p = sub.add_parser("offline")
    p.add_argument("--invited", type=float, required=True)
    p.add_argument("--attend-rate", required=True)
    p.add_argument("--deal-rate", required=True)
    p.add_argument("--aov", type=float, required=True)
    p.set_defaults(fn=cmd_offline)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
