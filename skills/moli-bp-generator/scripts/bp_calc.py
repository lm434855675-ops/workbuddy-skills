#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bp_calc.py - BP 十段完整性校验引擎。退出码 0/1/9。"""
import argparse, json, sys
def _die(m, c=1):
    sys.stderr.write("[%d] %s\n" % (c, m)); sys.exit(c)
SECTIONS = ["执行摘要", "痛点", "解决方案", "市场规模", "商业模式", "竞争分析", "团队", "财务预测", "里程碑规划", "融资计划"]
def cmd_check(a):
    try:
        bp = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析失败: %s" % e, 9)
    if not isinstance(bp, dict):
        _die("输入必须是对象，键=十段名称，值=该段内容文本")
    missing, thin = [], []
    for s in SECTIONS:
        v = str(bp.get(s, "")).strip()
        if not v: missing.append(s)
        elif len(v) < 30: thin.append(s)
    out = {"command": "check", "total_sections": len(SECTIONS), "passed": len(SECTIONS) - len(missing) - len(thin),
      "missing_sections": missing, "thin_sections": thin,
      "verdict": "PASS" if not missing and not thin else "FAIL",
      "verdict_note": ("十段齐全，可直接渲染交付") if not missing and not thin else
                      ("%s%s。不合格段落不入 BP" % ("缺段：" + "、".join(missing) + "。" if missing else "",
                       "内容过薄（<30字）：" + "、".join(thin) if thin else "")),
      "rules": ["十段缺一不可", "财务预测必须与里程碑对应", "融资额度=里程碑资金需求，不是拍数字"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
def main():
    ap = argparse.ArgumentParser(description="BP 十段完整性校验引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("check", help="BP 十段校验")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_check)
    a = ap.parse_args(); a.func(a)
if __name__ == "__main__":
    main()