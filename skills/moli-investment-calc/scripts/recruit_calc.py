#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recruit_calc.py — moli-investment-calc 测算引擎（back-solve / tier / stack / rhythm）。

用法:
    python3 recruit_calc.py back-solve --target-gmv 10000000 --months 6 --agent-price 20000 --avg-order 15000 --repurchase-months 2
    python3 recruit_calc.py tier --tiers "联创,50000,300,1" --tiers "总代,10000,180,5" --tiers "区代,2000,120,20" --retail 299 --cost 60
    python3 recruit_calc.py stack --cost 60 --retail 299 --agent-price 120 --volume-rebate 15% --signup-gift 10% --season-discount 8%
    python3 recruit_calc.py rhythm --target-agents 500 --weeks 12 --curve logistic

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
    return v / 100.0 if v > 1 else v


def cmd_back_solve(args):
    if args.months <= 0 or args.target_gmv <= 0:
        die(1, "目标与周期必须 > 0")
    if args.agent_price <= 0 or args.avg_order <= 0:
        die(1, "进货价与均单必须 > 0")
    if args.repurchase_months < 1:
        die(2, "复购月数须 ≥1")
    first = args.agent_price
    repurchase_per_agent = args.avg_order * (args.months / args.repurchase_months)
    per_agent_total = first + repurchase_per_agent
    agents_needed = args.target_gmv / per_agent_total
    monthly_agents = agents_needed / args.months
    result = {
        "目标回款": args.target_gmv,
        "周期(月)": args.months,
        "单代理全周期贡献(首批+复购)": round(per_agent_total, 0),
        "其中首批": round(first, 0),
        "其中复购": round(repurchase_per_agent, 0),
        "所需代理总数": round(agents_needed, 0),
        "月均新增代理": round(monthly_agents, 0),
        "口径": "回款=首批进货+复购，分列考核；复购率假设为线性，实际须按曲线校准；不构成回款承诺",
    }
    out(result, args.json)


def cmd_tier(args):
    if args.retail <= args.cost:
        die(2, "零售价(%s) 必须 > 成本(%s)" % (args.retail, args.cost))
    if len(args.tiers) > 3:
        die(2, "代理层级 %d 超过三层封顶红线" % len(args.tiers))
    rows = []
    for spec in args.tiers:
        parts = [p.strip() for p in spec.split(",")]
        if len(parts) != 4:
            die(1, "--tiers 需 4 段: 层级,进货价,零售价,该层代理商数。实际: %r" % spec)
        name, buy, retail, headcount = parts[0], float(parts[1]), float(parts[2]), int(parts[3])
        if buy <= args.cost:
            die(2, "层级 %s 进货价 %.0f ≤ 成本 %.0f，必亏" % (name, buy, args.cost))
        if buy >= retail:
            die(2, "层级 %s 进货价 %.0f ≥ 零售价 %.0f，无零售空间" % (name, buy, retail))
        margin = (retail - buy) / retail
        gap = (retail - buy) / retail
        rows.append({
            "层级": name, "进货价": buy, "零售价": retail, "该层代理商数": headcount,
            "该层毛利率": "%.0f%%" % (margin * 100),
            "零售-进货价差": "%.0f%% %s" % (gap * 100, "超40%红线-窜价风险高" if gap > 0.4 else "可控"),
        })
    base_margin = (args.retail - args.cost) / args.retail
    out({"分层明细": rows, "整体毛利率": "%.0f%%" % (base_margin * 100),
         "口径": "相邻价差红线40%为经验值；让利率须另行过 stack 检查"}, args.json)


def cmd_stack(args):
    if args.cost <= 0 or args.retail <= 0 or args.agent_price <= 0:
        die(1, "成本/零售价/进货价必须 > 0")
    if args.retail <= args.cost:
        die(2, "零售价必须 > 成本")
    if args.agent_price <= args.cost:
        die(2, "进货价必须 > 成本")
    vr = _rate(args.volume_rebate, "volume-rebate")
    sg = _rate(args.signup_gift, "signup-gift")
    sd = _rate(args.season_discount, "season-discount")
    total_give = vr + sg + sd
    # 让利成本按进货价为基准：即时折扣降净价，返利与赠货按兑现成本计
    net_price = args.agent_price * (1 - sd)
    give_cost = args.agent_price * (vr + sg) + args.agent_price * sd
    cap = (args.retail - args.cost) * 0.6  # 红线：总让利成本 < (零售-成本)x60%
    result = {
        "各项叠加": {"量返": "%.0f%%" % (vr * 100), "签约赠": "%.0f%%" % (sg * 100), "季节折扣": "%.0f%%" % (sd * 100)},
        "叠加让利率(对进货价)": "%.0f%%" % (total_give * 100),
        "折后净进货价": round(net_price, 2),
        "总让利成本": round(give_cost, 2),
        "红线(零售-成本x60%)": round(cap, 2),
        "让利占空间比": "%.0f%%" % (give_cost / cap * 100),
        "结论": "合规" if (net_price > args.cost and give_cost <= cap) else "必改：砍返利/降折扣/提进货价",
        "提示": "返利建议与动销挂钩，不与拉人头挂钩；层级只讲销售分润",
    }
    out(result, args.json)
    if net_price <= args.cost:
        die(2, "叠加后净进货价 %.2f ≤ 成本 %.0f，品牌方亏本" % (net_price, args.cost))
    if give_cost > cap:
        die(2, "总让利成本 %.0f 击穿 60%% 红线 %.0f：砍返利或提进货价" % (give_cost, cap))


def cmd_rhythm(args):
    if args.target_agents <= 0 or args.weeks <= 0:
        die(1, "目标代理数与周期必须 > 0")
    n, w = args.target_agents, args.weeks
    # 四段式占比：预热0% 首发15% 放量60% 维稳25%
    phases = [("预热", 0.0, 2), ("首发", 0.15, 2), ("放量", 0.60, 5), ("维稳", 0.25, 3)]
    if sum(p[2] for p in phases) != w:
        # 按比例缩放到实际周数
        scale = w / sum(p[2] for p in phases)
        phases = [(name, ratio, max(1, round(cnt * scale))) for name, ratio, cnt in phases]
    rows = []
    cum = 0
    for name, ratio, cnt in phases:
        target = round(n * ratio, 0)
        cum += target
        rows.append({"阶段": name, "周数": cnt, "阶段目标代理": target, "累计": round(cum, 0)})
    result = {
        "总目标代理": n,
        "总周数": w,
        "排期": rows,
        "曲线": args.curve,
        "验证点": {
            "预热": "蓄客数 ≥ 目标代理数×3 才进首发",
            "首发": "首批回款 ≥ 总目标10%",
            "放量": "单周新增 ≥ 周目标",
            "维稳": "复购率 ≥30%，不达标停止扩招修动销",
        },
        "口径": "占比为经验值(15/60/25)，须按品类与团队校准；不构成回款承诺",
    }
    out(result, args.json)


def main():
    ap = argparse.ArgumentParser(description="moli-investment-calc calc engine")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("back-solve")
    p.add_argument("--target-gmv", type=float, required=True)
    p.add_argument("--months", type=float, required=True)
    p.add_argument("--agent-price", type=float, required=True)
    p.add_argument("--avg-order", type=float, required=True)
    p.add_argument("--repurchase-months", type=float, required=True)
    p.set_defaults(fn=cmd_back_solve)

    p = sub.add_parser("tier")
    p.add_argument("--tiers", action="append", required=True)
    p.add_argument("--retail", type=float, required=True)
    p.add_argument("--cost", type=float, required=True)
    p.set_defaults(fn=cmd_tier)

    p = sub.add_parser("stack")
    p.add_argument("--cost", type=float, required=True)
    p.add_argument("--retail", type=float, required=True)
    p.add_argument("--agent-price", type=float, required=True)
    p.add_argument("--volume-rebate", required=True)
    p.add_argument("--signup-gift", required=True)
    p.add_argument("--season-discount", required=True)
    p.set_defaults(fn=cmd_stack)

    p = sub.add_parser("rhythm")
    p.add_argument("--target-agents", type=float, required=True)
    p.add_argument("--weeks", type=int, required=True)
    p.add_argument("--curve", default="logistic")
    p.set_defaults(fn=cmd_rhythm)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
