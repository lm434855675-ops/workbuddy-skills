#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""group_calc.py — 社群全周期 SOP 排期引擎。退出码 0/1。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
def _num(v, f):
    s = str(v).strip().replace(",", "").replace("人", "")
    try: return float(s)
    except ValueError: _die("参数 %s 不是合法数字: %r" % (f, v))
PLAN = [
 ("D1", "入群欢迎+群规+破冰话题模板", "群规+3 个破冰话题"),
 ("D2-3", "首场干货分享（行业痛点内容）", "互动 ≥10%"),
 ("D4", "顾客案例/买家秀", "点赞回复 ≥5"),
 ("D5", "首个小活动（接龙/投票/抽奖）", "参与 ≥30%"),
 ("D6-7", "首单转化：群专属券（48h 有效）", "核销 ≥15%"),
 ("每周固定", "一干货/一案例/一互动/一优惠（4 条节奏）", "周活跃 ≥25%"),
 ("每月", "1 次主题周（诊断日/团购日/会员日轮换）", "月成交 ≥5% 顾客"),
 ("沉默处理", "连续 14 天活跃 <10%：换群主 IP+改内容结构；30 天仍低 → 并群重开", "—"),
]
def cmd_plan(a):
    members = _num(a.members, "--members 群人数")
    days = int(_num(a.days, "--days"))
    if members <= 0 or days <= 0:
        _die("人数和天数必须大于 0")
    out = {"command": "plan", "inputs": {"members": members, "industry": a.industry, "days": days},
      "groups_advice": "单群 ≤300 人（超了拆分，越大越死）",
      "plan": [{"phase": p, "action": act, "criterion": c} for p, act, c in PLAN[:max(3, min(len(PLAN), days // 5 + 3))]],
      "verdict": "PASS",
      "verdict_note": "按 %d 天排期输出。红包只用于仪式感节点（开奖/满赞），日常发红包=教坏顾客" % days,
      "rules": ["单群 ≤300 人", "每天发言 ≤2 条（广告 ≤1 条）", "每周 1 个群内真人 IP 出镜"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="社群全周期SOP排期引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("plan", help="社群运营排期")
    r.add_argument("--members", required=True); r.add_argument("--industry", required=True); r.add_argument("--days", required=True)
    r.set_defaults(func=cmd_plan)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()