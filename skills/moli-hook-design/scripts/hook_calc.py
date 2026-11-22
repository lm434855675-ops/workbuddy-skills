#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hook_calc.py — 引流品成本红线与选型引擎。退出码 0/1。"""
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
TYPES = {"券类": "面值按核销率 40% 算真实成本——主力，核销带来二次消费",
         "体验类": "边际成本（人工+耗材）——服务业态最优",
         "资料类": "零边际成本——知识/教育业态最优",
         "实物类": "采购价——谨慎，仅高毛利业态"}
def cmd_check(a):
    ao = _num(a.avg_order, "--avg-order"); m = _num(a.gross_margin, "--gross-margin")
    margin = m / 100 if m > 1 else m
    hc = _num(a.hook_cost, "--hook-cost"); t = str(a.hook_type or "券类").strip()
    if ao <= 0: _die("客单价必须大于 0")
    if not (0 < margin < 1): _die("毛利率 0-100%")
    if hc < 0: _die("成本不能为负")
    red = ao * margin * 0.15
    ok = hc <= red and t in TYPES
    out = {"command": "check",
      "inputs": {"avg_order": ao, "gross_margin": margin, "hook_cost": hc, "type": t},
      "redline_cost": round(red, 2), "type_guide": TYPES.get(t, "未知类型"),
      "verdict": "PASS" if ok else "FAIL",
      "verdict_note": ("成本 %.2f 元 ≤ 红线 %.2f 元（客单毛利 15%%），%s 钩子可投" % (hc, red, t)) if ok else
                      ("打回：成本 %.2f 元超红线 %.2f 元。修复：① 改券类按核销率算真实成本 ② 改零边际（资料/体验）③ 砍配置" % (hc, red)),
      "rules": ["钩子与主业强相关（防薅羊毛）", "兑现链路 ≤2 步", "券类按核销率 40% 算真实成本"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="引流品测算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="引流品成本校验")
    r.add_argument("--avg-order", required=True); r.add_argument("--gross-margin", required=True)
    r.add_argument("--hook-cost", required=True); r.add_argument("--hook-type", default="券类")
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()