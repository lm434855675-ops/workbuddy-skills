#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mall_calc.py — moli-mall-ops 测算引擎（floor / funnel / coupon / member / gmv）。

用法示例:
    python3 mall_calc.py floor --floor "首屏,52000,6100,420,68000" ...
    python3 mall_calc.py funnel --aov 168 --step "触达,50000" --step "进店,6000,15%"
    python3 mall_calc.py coupon --aov 168 --gross-margin-rate 45% --face 20 --threshold 199 --redeem-rate 12% --issued 50000
    python3 mall_calc.py member --members 126000 --reach-rate 60% --open-rate 12% --order-rate 8% --aov 168 --gross-margin-rate 45% --discount-rate 12% --reach-cost 0.045 --baseline-gmv 38000
    python3 mall_calc.py gmv --target 1260000 --uv 90000 --cvr 1.8% --aov 168

比率支持 0.12 / 12% 两种写法。加 --json 输出结构化结果。
退出码: 0 成功; 2 参数无解(如让利率>=毛利率)。
"""
import argparse
import json
import sys


def parse_rate(s):
    """'12%' -> 0.12 ; '0.12' -> 0.12"""
    if s is None:
        return None
    s = str(s).strip()
    if s.endswith("%"):
        return float(s[:-1]) / 100.0
    v = float(s)
    return v / 100.0 if v > 1 else v


def die(msg):
    sys.stderr.write("[2] %s\n" % msg)
    sys.exit(2)


def out(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for k, v in data.items():
            print("%s: %s" % (k, v))


def cmd_floor(args):
    floors = []
    for spec in args.floor:
        parts = [p.strip() for p in spec.split(",")]
        if len(parts) != 5:
            die("楼层参数需 5 段: 名称,曝光UV,点击UV,引导GMV,备注(可留空)。实际: %r" % spec)
        name, imp, clk, gmv = parts[0], int(parts[1]), int(parts[2]), float(parts[3])
        if imp <= 0:
            die("楼层 %s 曝光 UV 必须 > 0" % name)
        ctr = clk / imp
        uv_value = gmv / imp  # 坑位 UV 价值 = 引导 GMV / 曝光 UV
        floors.append({
            "楼层": name, "曝光UV": imp, "点击UV": clk,
            "CTR": round(ctr * 100, 2), "坑位UV价值": round(uv_value, 2),
            "判定": _floor_verdict(ctr, uv_value),
        })
    ranked = sorted(floors, key=lambda f: f["坑位UV价值"], reverse=True)
    result = {
        "楼层诊断": floors,
        "建议楼层顺序": [f["楼层"] for f in ranked],
        "说明": "排序依据=坑位UV价值(引导GMV/曝光UV)，非CTR",
    }
    out(result, args.json)


def _floor_verdict(ctr, uv_value):
    if ctr < 0.02 and uv_value < 1:
        return "双低-换内容或下架"
    if uv_value < 1:
        return "价值低-下沉或换品"
    if ctr < 0.02:
        return "素材问题-先改文案"
    return "保留-可尝试上移"


def cmd_funnel(args):
    steps = []
    for spec in args.step:
        parts = [p.strip() for p in spec.split(",")]
        name = parts[0]
        val = float(parts[1])
        base = parse_rate(parts[2]) if len(parts) > 2 and parts[2] else None
        steps.append({"环节": name, "数值": val, "基准转化率": base})
    if len(steps) < 2:
        die("漏斗至少 2 个环节")
    rows = []
    worst = None
    worst_gap = -1
    for i in range(1, len(steps)):
        prev = steps[i - 1]["数值"]
        cur = steps[i]["数值"]
        if prev <= 0:
            die("环节 %s 数值必须 > 0" % steps[i - 1]["环节"])
        conv = cur / prev
        row = {"从": steps[i - 1]["环节"], "到": steps[i]["环节"], "转化率": round(conv * 100, 2)}
        base = steps[i]["基准转化率"]
        if base:
            row["与基准差"] = round((conv - base) * 100, 2)
            if base - conv > worst_gap:
                worst_gap = base - conv
                worst = steps[i]["环节"]
        rows.append(row)
    aov = args.aov
    final = steps[-1]["数值"]
    gmv = final * aov
    result = {"漏斗": rows, "末端GMV": round(gmv, 2)}
    if worst:
        result["最大流失环节"] = worst
        result["敏感度"] = "该环节每提升 1 个百分点，GMV +%.0f" % (steps[0]["数值"] * aov * 0.01)
    else:
        result["敏感度"] = "未提供基准转化率，无法定位最大流失环节"
    out(result, args.json)


def cmd_coupon(args):
    aov = args.aov
    gm = parse_rate(args.gross_margin_rate)
    face = args.face
    threshold = args.threshold
    redeem = parse_rate(args.redeem_rate)
    issued = args.issued
    if gm >= 1:
        die("毛利率必须 < 100%")
    unit_margin = threshold * gm
    if face >= unit_margin:
        die("券面额(%.2f) >= 按门槛成交的单笔毛利(%.2f)，必亏" % (face, unit_margin))
    used = issued * redeem
    cost = used * face
    gmv_no_coupon = threshold  # 单笔
    incremental_needed = cost / gm  # 保本所需增量 GMV
    ratio = incremental_needed / (gmv_no_coupon * max(used, 1))
    result = {
        "券面额上限(单笔毛利x0.5)": round(unit_margin * 0.5, 2),
        "当前面额": face,
        "预计核销张数": round(used, 0),
        "让利成本": round(cost, 2),
        "保本增量GMV": round(incremental_needed, 2),
        "增量占核销GMV比例": "%.1f%%" % (ratio * 100),
        "门槛/客单倍数": round(threshold / aov, 2),
    }
    out(result, args.json)


def cmd_member(args):
    members = args.members
    reach = parse_rate(args.reach_rate)
    open_r = parse_rate(args.open_rate)
    order_r = parse_rate(args.order_rate)
    aov = args.aov
    gm = parse_rate(args.gross_margin_rate)
    disc = parse_rate(args.discount_rate)
    reach_cost = parse_rate(args.reach_cost)
    baseline = args.baseline_gmv
    reached = members * reach
    opened = reached * open_r
    orders = opened * order_r
    gmv = orders * aov
    discount_cost = gmv * disc
    total_cost = reached * reach_cost + discount_cost
    roi = (gmv * gm - total_cost) / total_cost if total_cost else 0
    breakeven_cvr = (total_cost / (aov * gm)) / reached if reached else 0
    incremental = gmv - baseline
    result = {
        "触达人数": round(reached, 0),
        "打开人数": round(opened, 0),
        "下单人数": round(orders, 0),
        "活动GMV": round(gmv, 2),
        "让利成本": round(discount_cost, 2),
        "触达成本": round(reached * reach_cost, 2),
        "总成本": round(total_cost, 2),
        "ROI": "%.2f" % roi,
        "保本下单转化率": "%.2f%%" % (breakeven_cvr * 100),
        "增量GMV(扣基线)": round(incremental, 2),
    }
    out(result, args.json)


def cmd_gmv(args):
    target = args.target
    uv = args.uv
    cvr = parse_rate(args.cvr)
    aov = args.aov
    orders = uv * cvr
    gmv = orders * aov
    gap = target - gmv
    result = {
        "当前结构GMV": round(gmv, 2),
        "目标GMV": target,
        "缺口": round(gap, 2),
        "达成路径(三选一)": {
            "UV需提升至": round(target / (cvr * aov), 0) if cvr and aov else "-",
            "转化率需提至": "%.2f%%" % ((target / (uv * aov)) * 100) if uv and aov else "-",
            "客单需提至": round(target / (uv * cvr), 2) if uv and cvr else "-",
        },
    }
    out(result, args.json)


def main():
    ap = argparse.ArgumentParser(description="moli-mall-ops calc engine")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_json(sp):
        """子命令也接受 --json；default=SUPPRESS 保证不覆盖顶层已解析的值。"""
        sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="JSON 输出（写在子命令后也行）")
        return sp

    p = add_json(sub.add_parser("floor"))
    p.add_argument("--floor", action="append", required=True, help="名称,曝光UV,点击UV,引导GMV")
    p.set_defaults(fn=cmd_floor)

    p = add_json(sub.add_parser("funnel"))
    p.add_argument("--aov", type=float, required=True)
    p.add_argument("--step", action="append", required=True, help="环节名,数值[,基准转化率]")
    p.set_defaults(fn=cmd_funnel)

    p = add_json(sub.add_parser("coupon"))
    p.add_argument("--aov", type=float, required=True)
    p.add_argument("--gross-margin-rate", required=True)
    p.add_argument("--face", type=float, required=True)
    p.add_argument("--threshold", type=float, required=True)
    p.add_argument("--redeem-rate", required=True)
    p.add_argument("--issued", type=float, required=True)
    p.set_defaults(fn=cmd_coupon)

    p = add_json(sub.add_parser("member"))
    p.add_argument("--members", type=float, required=True)
    p.add_argument("--reach-rate", required=True)
    p.add_argument("--open-rate", required=True)
    p.add_argument("--order-rate", required=True)
    p.add_argument("--aov", type=float, required=True)
    p.add_argument("--gross-margin-rate", required=True)
    p.add_argument("--discount-rate", required=True)
    p.add_argument("--reach-cost", required=True)
    p.add_argument("--baseline-gmv", type=float, required=True)
    p.set_defaults(fn=cmd_member)

    p = add_json(sub.add_parser("gmv"))
    p.add_argument("--target", type=float, required=True)
    p.add_argument("--uv", type=float, required=True)
    p.add_argument("--cvr", required=True)
    p.add_argument("--aov", type=float, required=True)
    p.set_defaults(fn=cmd_gmv)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
