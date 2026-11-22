#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
omni_calc.py — 公私域联动计算引擎。
命令：funnel(承接漏斗测算) / hook(钩子成本校验)。
数字输入全走 _num() 安全转换；参数非法 exit 1。

退出码: 0 成功; 1 参数错误。
"""
import argparse
import json
import sys


def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def _num(v, field="数值"):
    if v is None:
        _die("缺少参数 %s" % field)
    s = str(v).strip().replace(",", "").replace("，", "").replace("元", "")
    if not s:
        _die("参数 %s 为空" % field)
    pct = s.endswith("%")
    if pct:
        s = s[:-1].strip()
    mult = 1.0
    for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3), ("天", 1), ("日", 1)):
        if s.endswith(suf):
            mult = m
            s = s[: -len(suf)].strip()
            break
    try:
        n = float(s) * mult
    except ValueError:
        _die("参数 %s 不是合法数字: %r" % (field, v))
    if pct:
        n = n / 100.0
    return n


def _pct(v, field):
    s = str(v).strip()
    n = _num(v, field)
    if not s.endswith("%") and n > 1:
        n = n / 100.0
    if not (0 <= n <= 1):
        _die("参数 %s 应为 0-100%% 之间的比例，得到 %r" % (field, v))
    return n


# 行业基准
BENCH = {"add_rate": 0.10, "first_order_rate": 0.25, "d90_repurchase": 0.30}


def cmd_funnel(a):
    visitors = _num(a.visitors, "--visitors 月进店人数")
    add_rate = _pct(a.add_rate, "--add-rate 加微率")
    fo_rate = _pct(a.first_order_rate, "--first-order-rate 30天首单率")
    avg_order = _num(a.avg_order, "--avg-order 客单价")
    rep = _pct(a.repurchase_rate, "--repurchase-rate 复购率")
    if visitors <= 0 or avg_order <= 0:
        _die("进店人数和客单价必须大于 0")
    added = visitors * add_rate
    first_orders = added * fo_rate
    first_gmv = first_orders * avg_order
    repeat_buyers = first_orders * rep
    repeat_gmv = repeat_buyers * avg_order
    rows = [
        {"stage": "公域进店", "count": round(visitors, 1)},
        {"stage": "加微/企微", "count": round(added, 1), "actual": round(add_rate, 4),
         "benchmark": BENCH["add_rate"],
         "vs_benchmark": "达标" if add_rate >= BENCH["add_rate"] else "低于基准 %.0f%%" % ((BENCH["add_rate"] - add_rate) / BENCH["add_rate"] * 100)},
        {"stage": "30 天首单", "count": round(first_orders, 1), "actual": round(fo_rate, 4),
         "benchmark": BENCH["first_order_rate"],
         "vs_benchmark": "达标" if fo_rate >= BENCH["first_order_rate"] else "低于基准 %.0f%%" % ((BENCH["first_order_rate"] - fo_rate) / BENCH["first_order_rate"] * 100)},
        {"stage": "90 天复购", "count": round(repeat_buyers, 1), "actual": round(rep, 4),
         "benchmark": BENCH["d90_repurchase"],
         "vs_benchmark": "达标" if rep >= BENCH["d90_repurchase"] else "低于基准 %.0f%%" % ((BENCH["d90_repurchase"] - rep) / BENCH["d90_repurchase"] * 100)},
    ]
    broken = [r for r in rows if r.get("vs_benchmark") and r["vs_benchmark"] != "达标"]
    out = {
        "command": "funnel",
        "inputs": {"visitors": visitors, "add_rate": add_rate, "first_order_rate": fo_rate,
                   "avg_order": avg_order, "repurchase_rate": rep},
        "stages": rows,
        "first_order_gmv": round(first_gmv, 2),
        "d90_repeat_gmv": round(repeat_gmv, 2),
        "total_gmv_90d": round(first_gmv + repeat_gmv, 2),
        "broken_stages": [r["stage"] for r in broken],
        "verdict": "PASS" if not broken else "WARN",
        "verdict_note": (
            "漏斗全环达标，90 天总 GMV 预估 %.0f 元" % (first_gmv + repeat_gmv)
            if not broken else
            "断环：%s。修复优先级按漏斗顺序（上游断，下游全断）：%s" % (
                "、".join(r["stage"] for r in broken),
                "；".join("%s：实际 %.0f%% vs 基准 %.0f%%" % (r["stage"], r["actual"] * 100, r["benchmark"] * 100) for r in broken))
        ),
        "rules": [
            "加微率基准 8-15%，低于 8% 先改钩子，别加投放预算",
            "首单率基准 20-35%，低于 20% 查 24h 承接动作是否缺失",
            "复购率基准 30%，低于 30% 停止拉新先做召回",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_hook(a):
    avg_order = _num(a.avg_order, "--avg-order 客单价")
    margin = _pct(a.gross_margin, "--gross-margin 毛利率")
    hook_cost = _num(a.hook_cost, "--hook-cost 钩子单份成本")
    lift = _pct(a.expected_add_rate, "--expected-add-rate 预期加微率")
    if avg_order <= 0:
        _die("客单价必须大于 0")
    if not (0 < margin < 1):
        _die("毛利率应在 0-100% 之间")
    if hook_cost < 0:
        _die("钩子成本不能为负")
    redline = avg_order * margin * 0.15
    unit_margin = avg_order * margin
    ok = hook_cost <= redline
    out = {
        "command": "hook",
        "inputs": {"avg_order": avg_order, "gross_margin": margin, "hook_cost": hook_cost, "expected_add_rate": lift},
        "gross_margin_per_order": round(unit_margin, 2),
        "redline_cost": round(redline, 2),
        "redline_rule": "钩子单份成本 ≤ 客单毛利的 15%%（即 ≤ %.2f 元）" % redline,
        "verdict": "PASS" if ok else "FAIL",
        "verdict_note": (
            "钩子成本 %.2f 元，红线内；预期加微率 %.0f%%（基准 10%%）%s" % (
                hook_cost, lift * 100, "——达标可投" if lift >= 0.10 else "——低于基准，先改钩子设计再加预算")
            if ok else
            "钩子成本 %.2f 元超红线（上限 %.2f 元）。修复优先级：① 换零边际成本钩子（资料包/体验服务/分周发的券）② 降单份成本至 %.2f 元内 ③ 与主业强相关，砍掉通用礼品"
            % (hook_cost, redline, redline)
        ),
        "rules": [
            "钩子三原则：成本 ≤ 客单毛利 15%、即时兑现、与主业强相关",
            "券类钩子按核销率算真实成本（20 元券 × 40% 核销 = 8 元）",
            "禁止送与主业无关的高价值礼品——引来薅党",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="公私域联动计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("funnel", help="承接漏斗测算")
    f.add_argument("--visitors", required=True)
    f.add_argument("--add-rate", required=True)
    f.add_argument("--first-order-rate", required=True)
    f.add_argument("--avg-order", required=True)
    f.add_argument("--repurchase-rate", required=True)
    f.set_defaults(func=cmd_funnel)

    h = sub.add_parser("hook", help="钩子成本校验")
    h.add_argument("--avg-order", required=True)
    h.add_argument("--gross-margin", required=True)
    h.add_argument("--hook-cost", required=True)
    h.add_argument("--expected-add-rate", required=True)
    h.set_defaults(func=cmd_hook)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
