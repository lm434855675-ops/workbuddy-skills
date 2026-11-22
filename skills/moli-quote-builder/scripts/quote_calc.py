#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quote_calc.py - 三档报价测算引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def _num(v, f):
    if v is None: _die("缺少参数 %s" % f)
    s = str(v).strip().replace(",", "").replace("元", "")
    if s.endswith("%"): s = s[:-1].strip()
    for suf in ("天", "日"):
        if s.endswith(suf): s = s[:-len(suf)].strip(); break
    mult = 1.0
    for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3)):
        if s.endswith(suf): mult = m; s = s[:-len(suf)].strip(); break
    try: return float(s) * mult
    except ValueError: _die("参数 %s 不是合法数字: %r" % (f, v))
def cmd_tiers(a):
    cost = _num(a.cost, "--cost 总成本")
    tm = _num(a.target_margin, "--target-margin 目标毛利率")
    tm = tm / 100 if tm > 1 else tm
    if cost <= 0: _die("总成本必须大于 0")
    if not (0 < tm < 1): _die("目标毛利率应在 0-100%")
    std = cost / (1 - tm)
    basic = std * 0.8
    flag = std * 1.35
    mb = (basic - cost) / basic; mf = (flag - cost) / flag
    tiers = [
      {"tier": "基础档", "price": round(basic, 2), "margin_pct": round(mb * 100, 1), "config": "核心交付项，无增值服务", "use": "引流+价格锚点下限"},
      {"tier": "标准档", "price": round(std, 2), "margin_pct": round(tm * 100, 1), "config": "核心交付+标准服务", "use": "主推档（放中间）"},
      {"tier": "旗舰档", "price": round(flag, 2), "margin_pct": round(mf * 100, 1), "config": "全项交付+增值服务+优先权", "use": "价格锚点上限，衬托标准档"},
    ]
    ok = mb > 0
    out = {"command": "tiers", "inputs": {"cost": cost, "target_margin": tm},
      "tiers": tiers, "verdict": "PASS" if ok else "FAIL",
      "verdict_note": ("三档毛利率 %.1f%%/%.1f%%/%.1f%%，均达标。锚定逻辑：三档同框，顾客多数选中间档" % (mb * 100, tm * 100, mf * 100)) if ok else
                      "基础档毛利率 ≤0，报价结构不成立——先压成本或提标准档",
      "rules": ["三档同框，主推放中间", "旗舰档不是用来卖的，是用来衬标准档的", "任何一档毛利率 <0 即结构失败"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="三档报价测算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("tiers", help="三档报价测算")
    r.add_argument("--cost", required=True); r.add_argument("--target-margin", required=True)
    r.set_defaults(func=cmd_tiers)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()