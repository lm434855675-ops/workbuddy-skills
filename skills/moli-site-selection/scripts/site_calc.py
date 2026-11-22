#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site_calc.py — 门店选址计算引擎。命令：breakeven(盈亏平衡) / payback(回本周期)。退出码 0/1。"""
import argparse, json, sys

def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg)); sys.exit(code)

def _num(v, field):
    if v is None: _die("缺少参数 %s" % field)
    s = str(v).strip().replace(",", "").replace("，", "").replace("元", "")
    if not s: _die("参数 %s 为空" % field)
    mult = 1.0
    for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3)):
        if s.endswith(suf): mult = m; s = s[:-len(suf)].strip(); break
    try: n = float(s) * mult
    except ValueError: _die("参数 %s 不是合法数字: %r" % (field, v))
    return n

def cmd_breakeven(a):
    rent = _num(a.rent, "--rent 月租")
    other = _num(a.other_cost, "--other-cost 其他月固定成本")
    avg = _num(a.avg_order, "--avg-order 客单价")
    m = str(a.gross_margin).strip()
    margin = float(m[:-1]) / 100 if m.endswith("%") else (float(m) / 100 if float(m) > 1 else float(m))
    if rent < 0 or other < 0: _die("成本不能为负")
    if avg <= 0: _die("客单价必须大于 0")
    if not (0 < margin < 1): _die("毛利率应在 0-100%")
    fixed = rent + other
    daily_fixed = fixed / 30
    daily_gross = daily_fixed / margin
    orders = daily_gross / avg
    out = {
        "command": "breakeven",
        "inputs": {"monthly_rent": rent, "other_monthly_cost": other, "avg_order": avg, "gross_margin": margin},
        "monthly_fixed_cost": round(fixed, 2), "daily_fixed_cost": round(daily_fixed, 2),
        "breakeven_daily_revenue": round(daily_gross, 2),
        "breakeven_daily_orders": round(orders, 1),
        "verdict": "PASS",
        "verdict_note": "每天 %.0f 单 / %.0f 元营业额才保本（月固定成本 %.0f 元）。铁律：该数字 ≤ 你实测该点位可及日营业额的 70%%，否则放弃" % (orders, daily_gross, fixed),
        "rules": ["先测算后谈判，数字不行免谈", "人流必须实测，中介数字打 5 折", "水电/人工计入 other-cost，别只算租金"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def cmd_payback(a):
    rent = _num(a.rent, "--rent 月租")
    other = _num(a.other_cost, "--other-cost 其他月成本")
    profit = _num(a.net_profit_est, "--net-profit-est 预估月净利")
    setup = _num(a.setup_cost, "--setup-cost 总投入")
    if profit <= 0: _die("预估月净利必须大于 0（净利=毛利-租金-人工-水电-其他固定支出）")
    if setup <= 0: _die("总投入必须大于 0")
    months = setup / profit
    ok = months <= 24
    out = {
        "command": "payback",
        "inputs": {"monthly_rent": rent, "other_monthly_cost": other, "monthly_net_profit": profit, "setup_cost": setup},
        "payback_months": round(months, 1),
        "redline": "回本周期 >24 个月直接放弃；18-24 个月需额外增收方案",
        "verdict": "PASS" if ok else "FAIL",
        "verdict_note": ("回本 %.1f 个月，红线内可推进" % months) if ok else
                        ("回本 %.1f 个月超 24 个月红线。修复：① 压 setup（转让费/装修砍价）② 提净利（钧子产品+私域复购）③ 换点位" % months),
        "rules": ["转让费+押金计入 setup", "预估月净利要扣除老板自己工资", "淡旺季取平均，别用最好月份骗自己"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser(description="门店选址计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("breakeven", help="盈亏平衡测算")
    b.add_argument("--rent", required=True); b.add_argument("--other-cost", required=True)
    b.add_argument("--avg-order", required=True); b.add_argument("--gross-margin", required=True)
    b.set_defaults(func=cmd_breakeven)
    p2 = sub.add_parser("payback", help="回本周期测算")
    p2.add_argument("--rent", required=True); p2.add_argument("--other-cost", required=True)
    p2.add_argument("--net-profit-est", required=True); p2.add_argument("--setup-cost", required=True)
    p2.set_defaults(func=cmd_payback)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()