#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
phase_calc.py — moli-fullcase-sop 排期测算引擎（schedule / weekly / gate）。

用法:
    python3 phase_calc.py schedule --months 6 --type recruit
    python3 phase_calc.py weekly --rhythm "周一例会,周三数据,周五复盘"
    python3 phase_calc.py gate --total-weeks 24 --elapsed 10 --remaining-phases 3

退出码: 0 成功; 1 参数错误; 2 测算无解。
"""
import argparse
import json
import sys

TYPES = {"recruit": [("诊断", 0.10), ("方案", 0.20), ("筹备", 0.35), ("上线", 0.25), ("复盘", 0.10)],
         "private": [("诊断", 0.15), ("方案", 0.10), ("筹备", 0.15), ("上线", 0.50), ("复盘", 0.10)],
         "local": [("诊断", 0.10), ("方案", 0.15), ("筹备", 0.30), ("上线", 0.35), ("复盘", 0.10)],
         "launch": [("诊断", 0.15), ("方案", 0.15), ("筹备", 0.25), ("上线", 0.35), ("复盘", 0.10)],
         "model": [("诊断", 0.20), ("方案", 0.30), ("筹备", 0.10), ("上线", 0.30), ("复盘", 0.10)]}


def die(code, msg):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def out(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for k, v in data.items():
            print("%s: %s" % (k, v))


def cmd_schedule(args):
    if args.type not in TYPES:
        die(1, "--type 须为 %s" % sorted(TYPES))
    if args.months <= 0:
        die(1, "周期必须 > 0")
    weeks = args.months * 4.345
    rows = []
    cum_w = 0.0
    for name, ratio in TYPES[args.type]:
        pw = weeks * ratio
        rows.append({"阶段": name, "占比": "%.0f%%" % (ratio * 100),
                     "周数": round(pw, 1),
                     "起(第N周)": round(cum_w, 0) + 1,
                     "止(第N周)": round(cum_w + pw, 0)})
        cum_w += pw
    out({"项目类型": args.type, "总月数": args.months, "总周数": round(weeks, 1),
         "排期": rows, "口径": "阶段占比为该类型经验值，可按项目校准"}, args.json)


def cmd_weekly(args):
    import re
    if not args.rhythm:
        die(1, "--rhythm 不能为空")
    fixed = [x.strip() for x in args.rhythm.split(",") if x.strip()]
    if len(fixed) < 2:
        die(1, "固定周动作至少 2 项（建议例会+数据）")
    days = []
    for item in fixed:
        m = re.match(r"^(周[一二三四五六日天])(.+)$", item)
        if not m:
            die(1, "格式应为 '周一例会,周三数据'，实际: %r" % item)
        days.append({"日": m.group(1), "固定动作": m.group(2)})
    out({"固定周动作": days, "规则": "固定动作进日历，浮动动作让位；例会只过数据与决策"}, args.json)


def cmd_gate(args):
    if args.total_weeks <= 0 or args.elapsed < 0 or args.remaining_phases <= 0:
        die(1, "参数非法")
    if args.elapsed > args.total_weeks:
        die(2, "已耗时(%d)超过总周期(%d)" % (args.elapsed, args.total_weeks))
    remaining_weeks = args.total_weeks - args.elapsed
    per_phase = remaining_weeks / args.remaining_phases
    verdict = "可行" if per_phase >= 2 else "风险：剩余阶段平均不足 2 周，砍范围或申请延期"
    result = {
        "总周期(周)": args.total_weeks,
        "已耗时(周)": args.elapsed,
        "剩余(周)": remaining_weeks,
        "剩余阶段数": args.remaining_phases,
        "每阶段可用周数": round(per_phase, 1),
        "结论": verdict,
    }
    out(result, args.json)
    if per_phase < 2:
        die(2, "剩余周期不足：每阶段仅 %.1f 周 < 2 周" % per_phase)


def main():
    ap = argparse.ArgumentParser(description="moli-fullcase-sop phase calc")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("schedule")
    p.add_argument("--months", type=float, required=True)
    p.add_argument("--type", required=True)
    p.set_defaults(fn=cmd_schedule)

    p = sub.add_parser("weekly")
    p.add_argument("--rhythm", required=True)
    p.set_defaults(fn=cmd_weekly)

    p = sub.add_parser("gate")
    p.add_argument("--total-weeks", type=int, required=True)
    p.add_argument("--elapsed", type=int, required=True)
    p.add_argument("--remaining-phases", type=int, required=True)
    p.set_defaults(fn=cmd_gate)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
