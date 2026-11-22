#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fission_calc.py — 裂变 K 因子测算引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def _num(v, f):
    s = str(v).strip().replace(",", "").replace("人", "").replace("元", "")
    if s.endswith("%"): s = s[:-1].strip()
    for suf in ("天", "日"):
        if s.endswith(suf): s = s[:-len(suf)].strip(); break
    try: return float(s)
    except ValueError: _die("参数 %s 非法: %r" % (f, v))
def cmd_kfactor(a):
    inv = _num(a.invited, "--invited"); sh = _num(a.shares, "--shares")
    conv = _num(a.conversions, "--conversions"); cost = _num(a.cost, "--cost")
    ao = _num(a.avg_order, "--avg-order"); m = _num(a.gross_margin, "--gross-margin")
    margin = m / 100 if m > 1 else m
    if inv <= 0:
        _die("初始参与人数必须大于 0")
    if not (0 < margin < 1):
        _die("毛利率 0-100%")
    k = conv / inv
    cpa = cost / conv if conv > 0 else float("inf")
    gross = ao * margin
    ok = k >= 1 and cpa <= gross * 0.3
    out = {"command": "kfactor",
      "inputs": {"invited": inv, "shares": sh, "conversions": conv, "cost": cost, "avg_order": ao, "gross_margin": margin},
      "k_factor": round(k, 3), "share_rate": round(sh / inv, 3) if inv else 0,
      "cost_per_new_customer": round(cpa, 2), "gross_margin_per_order": round(gross, 2),
      "redline": "K ≥ 1 且 单新客成本 ≤ 客单毛利的 30%",
      "verdict": "PASS" if ok else "FAIL",
      "verdict_note": ("K=%.2f，单新客 %.0f 元 ≤ 红线 %.0f 元——可复制放量" % (k, cpa, gross * 0.3)) if ok else
                      ("打回：K=%.2f%s，单新客 %.0f 元%s。修复：① 降补贴（改阶梯券）② 提分享率（双向奖励）③ 提转化（到店核销）" % (
                          k, "（<1 自循环断裂）" if k < 1 else "", cpa, "超红线" if cpa > gross * 0.3 else "")),
      "rules": ["K<1 的裂变是烧钱游戏，立即停", "补贴改阶梯（邀1人10元/邀3人40元）", "虚拟奖励零成本优先"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="裂变 K 因子测算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("kfactor", help="K 因子测算")
    r.add_argument("--invited", required=True); r.add_argument("--shares", required=True)
    r.add_argument("--conversions", required=True); r.add_argument("--cost", required=True)
    r.add_argument("--avg-order", required=True); r.add_argument("--gross-margin", required=True)
    r.set_defaults(func=cmd_kfactor)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()