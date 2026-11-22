#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""closing_calc.py — 逼单信号与降价红线计算引擎。退出码 0/1/9。"""
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
    try: return float(s) * mult
    except ValueError: _die("参数 %s 不是合法数字: %r" % (field, v))

SIGNALS = {"问价格细节": 20, "问交付售后": 20, "主动对比竞品": 15, "邀约到店": 25, "问优惠": 10, "二次咨询": 10}

def cmd_signal(a):
    if not a.file: _die("缺少 --file 信号 JSON")
    try:
        leads = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(leads, list) or not leads:
        _die("输入必须是非空数组（lead/signals）")
    out_leads = []
    for i, ld in enumerate(leads):
        lead = str(ld.get("lead", "lead%d" % (i + 1)))
        sigs = ld.get("signals", [])
        if not isinstance(sigs, list):
            _die("leads[%d] 的 signals 必须是数组" % i)
        score, unknown = 0, []
        for s in sigs:
            s = str(s).strip()
            if s in SIGNALS: score += SIGNALS[s]
            else: unknown.append(s)
        verdict = ("≥60 可逼单：二选一闭环（基础版 vs 完整版），今天给期限" if score >= 60 else
                   "40-59 先补价值：一次价值型触达（案例/资料），3 天后再评" if score >= 40 else
                   "<40 不逼单：继续培育，逼早了吓跑人")
        out_leads.append({"lead": lead, "signals": sigs, "score": score, "verdict": verdict,
                          "unknown_signals": unknown})
    out = {
        "command": "signal", "leads": out_leads,
        "verdict": "PASS",
        "verdict_note": "≥60 可逼单 / 40-59 先补价值 / <40 继续培育。未识别信号：%s（补充到信号权重表可提精度）" % ("、".join(sorted({u for o in out_leads for u in o["unknown_signals"]}))) if any(o["unknown_signals"] for o in out_leads) else "≥60 可逼单 / 40-59 先补价值 / <40 继续培育",
        "rules": ["逼单=二选一闭环+当天期限", "沉默 48h 给缓冲+一次价值型触达", "信号分是时点的，每次互动后重算"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def cmd_discount(a):
    price = _num(a.price, "--price 原价")
    cost = _num(a.cost, "--cost 单笔成本")
    dp = _num(a.discount_proposal, "--discount-proposal 客户要的折后价")
    swap = str(a.swap_condition or "").strip()
    if price <= 0 or cost < 0: _die("原价必须大于 0，成本不能为负")
    if dp >= price: _die("折后价应低于原价")
    if cost >= price: _die("成本高于原价，这单本身不成立")
    margin_now = (price - cost) / price
    margin_after = (dp - cost) / dp
    giveup = price - dp
    ok = dp > cost and margin_after >= margin_now * 0.6 and bool(swap)
    out = {
        "command": "discount",
        "inputs": {"price": price, "cost": cost, "proposed_price": dp, "swap_condition": swap},
        "margin_now_pct": round(margin_now * 100, 1), "margin_after_pct": round(margin_after * 100, 1),
        "give_up_yuan": round(giveup, 2),
        "redline": "折后毛利率 ≥ 现毛利率的 60%，且必须换条件",
        "verdict": "PASS" if ok else "FAIL",
        "verdict_note": ("让利 %.0f 元换「%s」，毛利率 %.1f%%→%.1f%%（红线内），闭环成立" % (giveup, swap, margin_now * 100, margin_after * 100))
                        if ok else
                        ("打回：%s。修复：① 让利幅度超红线（折后毛利 <现毛利 60%%）② %s" % (
                            "缺交换条件" if not swap else "折后毛利率过低",
                            "" if swap else "降价必须换条件（今天定/转介绍/买家秀）")),
        "rules": ["降价必须换条件", "让利 ≤ 现毛利的 40%", "换来的条件要可验证（截图/名单/发布链接）"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def main():
    ap = argparse.ArgumentParser(description="逼单信号与降价红线计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("signal", help="逼单信号评分")
    s1.add_argument("--file", required=True)
    s1.set_defaults(func=cmd_signal)
    s2 = sub.add_parser("discount", help="降价红线校验")
    s2.add_argument("--price", required=True); s2.add_argument("--cost", required=True)
    s2.add_argument("--discount-proposal", required=True); s2.add_argument("--swap-condition", default="")
    s2.set_defaults(func=cmd_discount)
    a = ap.parse_args(); a.func(a)

if __name__ == "__main__":
    main()