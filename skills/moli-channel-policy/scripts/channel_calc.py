#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""channel_calc.py - 渠道政策双向测算引擎。退出码 0/1。"""
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
def cmd_policy(a):
    retail = _num(a.retail_price, "--retail-price 零售价")
    supply = _num(a.supply_price, "--supply-price 供货价(渠道拿货价)")
    rebate = _num(a.rebate_pct, "--rebate-pct 返点比例")
    target = _num(a.task_monthly, "--task-monthly 月任务额")
    m = _num(a.company_margin, "--company-margin 公司毛利率")
    margin = m / 100 if m > 1 else m
    if retail <= 0 or supply <= 0 or supply >= retail: _die("零售价必须大于供货价")
    if not (0 < margin < 1): _die("公司毛利率 0-100%")
    ch_margin = (retail - supply) / retail
    rebate_yuan = supply * (rebate / 100) if rebate else 0
    ch_margin_net = (retail - supply + rebate_yuan) / retail
    company_ok = margin >= 0.25
    channel_ok = ch_margin_net >= 0.25
    out = {"command": "policy",
      "inputs": {"retail": retail, "supply": supply, "rebate_pct": rebate, "company_margin": margin},
      "channel_margin_pct": round(ch_margin * 100, 1), "channel_margin_net_pct": round(ch_margin_net * 100, 1),
      "company_gross_pct": round(margin * 100, 1),
      "task_line_note": "月任务额 %.0f 元：达成返 %.0f%%（%.0f 元/万），未达成不返——任务线是返点的开关" % (target, rebate, target * rebate / 100) if rebate else "未设返点：渠道动力全靠价差",
      "verdict": "PASS" if (company_ok and channel_ok) else "FAIL",
      "verdict_note": ("渠道毛利 %.1f%%（含返点 %.1f%%）、公司毛利 %.1f%%——双向有钱赚，政策成立" % (ch_margin * 100, ch_margin_net * 100, margin * 100)) if (company_ok and channel_ok) else
                      ("打回：%s。修复：%s" % (
                        "渠道毛利 <25% 渠道没动力" if not channel_ok else "公司毛利 <25% 自己没肉",
                        "提零售价锚点 / 降供货成本 / 改返点结构（后置返点代替直接降供货价）")),
      "rules": ["渠道毛利 <25% 没人推你的货", "返点后置（季度返）优于直接降供货价", "区域保护必须写进政策（串货处罚）", "任务线定在渠道能力的 70%（跳一跳够得着）"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="渠道政策双向测算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("policy", help="渠道政策双向测算")
    r.add_argument("--retail-price", required=True); r.add_argument("--supply-price", required=True)
    r.add_argument("--rebate-pct", required=True); r.add_argument("--task-monthly", required=True)
    r.add_argument("--company-margin", required=True)
    r.set_defaults(func=cmd_policy)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()