#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""referral_calc.py - 转介绍激励测算引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def _num(v, f):
    if v is None: _die("缺少参数 %s" % f)
    s = str(v).strip().replace(",", "").replace("元", "")
    if s.endswith("%"): s = s[:-1].strip()
    mult = 1.0
    for suf, m in (("万", 1e4), ("千", 1e3)):
        if s.endswith(suf): mult = m; s = s[:-len(suf)].strip(); break
    try: return float(s) * mult
    except ValueError: _die("参数 %s 不是合法数字: %r" % (f, v))
def cmd_plan(a):
    ao = _num(a.avg_order, "--avg-order 客单")
    m = _num(a.gross_margin, "--gross-margin 毛利率")
    margin = m / 100 if m > 1 else m
    old_r = _num(a.old_reward, "--old-reward 老客奖励")
    new_r = _num(a.new_reward, "--new-reward 新客礼")
    rate = _num(a.expected_rate, "--expected-rate 预期参与率")
    rate = rate / 100 if rate > 1 else rate
    if not (0 < margin < 1): _die("毛利率 0-100%")
    if rate <= 0 or rate > 1: _die("参与率应 0-100%")
    gross = ao * margin
    cpc = (old_r + new_r) / rate if rate else float("inf")  # 每个参与的老客带来的成本
    cpa = (old_r + new_r)  # 每成交一个新客的激励成本（简化：1 老客带 1 新客成交）
    ok = cpa <= gross * 0.3
    out = {"command": "plan",
      "inputs": {"avg_order": ao, "gross_margin": margin, "old_reward": old_r, "new_reward": new_r, "expected_rate": rate},
      "gross_per_order": round(gross, 2), "incentive_per_conversion": round(cpa, 2),
      "redline": "双向激励合计 ≤ 客单毛利的 30%（即 ≤ %.2f 元）" % (gross * 0.3),
      "verdict": "PASS" if ok else "FAIL",
      "verdict_note": ("双向激励 %.0f 元 ≤ 红线 %.0f 元，闭环成立。参与率预期 %.0f%%，先小范围测 2 周再放量" % (cpa, gross * 0.3, rate * 100)) if ok else
                      ("打回：双向激励 %.0f 元超红线 %.0f 元。修复：① 老客奖励改等值积分/服务 ② 新客礼改首单券（核销率 40%% 算真实成本）③ 提客单而非加激励" % (cpa, gross * 0.3)),
      "rules": ["双向奖励比单向更有效（老客有面子新客有实惠）", "激励兑现挂钩新客真实成交（非注册）", "介绍动作给道具：可转发的专属海报/链接，别让人凭嘴说"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="转介绍激励测算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("plan", help="转介绍方案测算")
    r.add_argument("--avg-order", required=True); r.add_argument("--gross-margin", required=True)
    r.add_argument("--old-reward", required=True); r.add_argument("--new-reward", required=True)
    r.add_argument("--expected-rate", required=True)
    r.set_defaults(func=cmd_plan)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()