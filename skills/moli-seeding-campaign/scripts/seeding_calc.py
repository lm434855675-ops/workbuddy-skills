#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seeding_calc.py — moli-seeding-campaign 测算引擎（mix / topics / check）。

用法:
    python3 seeding_calc.py mix --budget 100000 --tier "头部,1,80000,5000000,0.02" --tier "腰部,5,15000,600000,0.035" --tier "素人,30,2000,80000,0.05"
    python3 seeding_calc.py topics --topic "成分科普,80,40,90" --topic "空瓶复盘,60,70,95"
    python3 seeding_calc.py check --title "熬夜脸自救指南" --has-hook 1 --has-scene 1 --has-contrast 1 --has-cta 1 --len 850

退出码: 0 成功; 1 参数错误; 2 测算无解。
"""
import argparse
import json
import sys


def die(code, msg):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def out(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for k, v in data.items():
            print("%s: %s" % (k, v))


def cmd_mix(args):
    if args.budget <= 0:
        die(2, "预算必须 > 0")
    tiers = []
    total_unit_cost = 0.0
    est_imp = 0.0
    est_eng = 0.0
    for spec in args.tier:
        parts = [p.strip() for p in spec.split(",")]
        if len(parts) != 5:
            die(1, "--tier 需 5 段: 层级,人数,单价,预估曝光,预估互动率。实际: %r" % spec)
        name, count, unit_cost, imp, eng_rate = parts[0], int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        if count <= 0 or unit_cost < 0:
            die(1, "层级 %s 人数/单价非法" % name)
        if eng_rate < 0 or eng_rate > 1:
            die(2, "层级 %s 互动率须在 0-1" % name)
        cost = count * unit_cost
        total_unit_cost += cost
        tier_imp = count * imp
        tier_eng = tier_imp * eng_rate
        est_imp += tier_imp
        est_eng += tier_eng
        tiers.append({"层级": name, "人数": count, "单价": unit_cost, "小计成本": round(cost, 0),
                      "预估曝光": round(tier_imp, 0), "预估互动": round(tier_eng, 0)})
    if total_unit_cost > args.budget * 1.000001:
        die(2, "组合成本 %.0f 超预算 %.0f（差额 %.0f）" % (total_unit_cost, args.budget, total_unit_cost - args.budget))
    cpe = total_unit_cost / est_eng if est_eng else None
    # 组合结构评分：以 头部:腰部:素人 成本比 2:5:3 为参照的经验模型
    ratio = {"头部": 0.2, "腰部": 0.5, "素人": 0.3}
    struct = 0.0
    detail = {}
    for t in tiers:
        share = t["小计成本"] / total_unit_cost if total_unit_cost else 0
        target = ratio.get(t["层级"], 1.0 / max(len(tiers), 1))
        gap = abs(share - target)
        detail[t["层级"]] = "成本占比%.0f%%(参照%.0f%%)" % (share * 100, target * 100)
        struct += max(0.0, 1 - gap / max(target, 1e-9)) / max(len(tiers), 1)
    result = {
        "层级明细": tiers,
        "总成本": round(total_unit_cost, 0),
        "预算余量": round(args.budget - total_unit_cost, 0),
        "预估总曝光": round(est_imp, 0),
        "预估总互动": round(est_eng, 0),
        "预估CPE": round(cpe, 2) if cpe else "-",
        "结构符合度": "%.0f%%" % (struct * 100),
        "结构说明": detail,
        "口径": "预估均基于输入的层级中位数假设，须用真实达人数据校准；不构成效果承诺",
    }
    out(result, args.json)


def cmd_topics(args):
    rows = []
    for spec in args.topic:
        parts = [p.strip() for p in spec.split(",")]
        if len(parts) != 4:
            die(1, "--topic 需 4 段: 选题,搜索需求,竞争度,产品相关度（各 1-100）。实际: %r" % spec)
        name, demand, comp, rel = parts[0], float(parts[1]), float(parts[2]), float(parts[3])
        for v, n in ((demand, "搜索需求"), (comp, "竞争度"), (rel, "产品相关度")):
            if not (1 <= v <= 100):
                die(1, "%s 的 %s 须在 1-100" % (name, n))
        score = demand * (100 - comp) * rel / 10000.0
        rows.append({"选题": name, "搜索需求": demand, "竞争度": comp, "产品相关度": rel,
                     "优先级分": round(score, 1)})
    rows.sort(key=lambda r: r["优先级分"], reverse=True)
    out({"选题排序": rows, "说明": "分高者优先；搜索需求无后台数据的标'待校准'后重算"}, args.json)


def cmd_check(args):
    hits = []
    if not args.has_hook:
        hits.append("缺首句钩子（痛点/场景/结果三选一）")
    if not args.has_scene:
        hits.append("缺场景锚点（用户在什么处境下用）")
    if not args.has_contrast:
        hits.append("缺对比或结果证据")
    if not args.has_cta:
        hits.append("缺单一 CTA")
    if args.len > 1200:
        hits.append("正文超长(%d>1200)，完读率风险" % args.len)
    if args.len < 300:
        hits.append("正文过短(%d<300)，信息量不足" % args.len)
    if args.title and len(args.title) > 20:
        hits.append("标题超长(%d>20 字)" % len(args.title))
    verdict = "必改" if any(h.startswith("缺") or "超长" in h or "过短" in h for h in hits) else ("建议" if hits else "通过")
    out({"标题": args.title, "结论": verdict, "问题": hits}, args.json)
    sys.exit(0 if verdict == "通过" else (1 if verdict == "必改" else 2))


def main():
    ap = argparse.ArgumentParser(description="moli-seeding-campaign calc engine")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("mix")
    p.add_argument("--budget", type=float, required=True)
    p.add_argument("--tier", action="append", required=True)
    p.set_defaults(fn=cmd_mix)

    p = sub.add_parser("topics")
    p.add_argument("--topic", action="append", required=True)
    p.set_defaults(fn=cmd_topics)

    p = sub.add_parser("check")
    p.add_argument("--title", default="")
    p.add_argument("--has-hook", type=int, default=0)
    p.add_argument("--has-scene", type=int, default=0)
    p.add_argument("--has-contrast", type=int, default=0)
    p.add_argument("--has-cta", type=int, default=0)
    p.add_argument("--len", type=int, default=0)
    p.set_defaults(fn=cmd_check)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
