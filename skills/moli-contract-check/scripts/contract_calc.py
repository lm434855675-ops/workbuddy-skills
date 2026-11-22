#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contract_calc.py - 合同八大项初审引擎。退出码 0/1/9。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
ITEMS = ["主体资质", "权责对等", "付款条款", "违约责任", "争议管辖", "知识产权", "保密条款", "终止条款"]
def cmd_check(a):
    try:
        c = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(c, dict):
        _die("输入必须是对象，键=八大项，值={status: 有/无/待补, note: 说明}")
    risks = []
    for k in ITEMS:
        v = c.get(k)
        if not v or not str(v.get("status", "")).strip():
            risks.append({"item": k, "risk": "高", "note": "未约定——合同里没有这一项，等于裸奔"})
        elif str(v["status"]) == "待补":
            risks.append({"item": k, "risk": "中", "note": str(v.get("note", "条款待补充明确"))})
        else:
            risks.append({"item": k, "risk": "低", "note": str(v.get("note", "已约定"))[:60]})
    high = sum(1 for r in risks if r["risk"] == "高")
    out = {"command": "check", "items": risks, "high_risks": high,
      "verdict": "WARN" if high else "PASS",
      "verdict_note": "%d 项未约定（高风险）。补齐前不建议签字" % high if high else "八大项均已约定，可进入法务复核",
      "rules": ["本清单是初审自查，不构成法律意见——重大合同必须律师复核", "付款条款重点：预付比例/验收标准/尾款周期", "违约责任重点：双方对等，只有单方违约金的合同直接打回"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="合同八大项初审引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="八大项初审")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()