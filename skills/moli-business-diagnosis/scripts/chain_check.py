#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_check.py — moli-business-diagnosis 五段链完整性检查与断点定位。

用法:
    python3 chain_check.py --scores '{"positioning":5,"value":7,"monetization":6,"growth":4,"moat":6}'
    python3 chain_check.py --scores '{...}' --json

退出码: 0 成功; 1 参数错误; 9 JSON 解析失败。
"""
import argparse
import json
import sys

LINKS = [("positioning", "定位", 5), ("value", "价值", 5), ("monetization", "变现", 5),
         ("growth", "增长", 5), ("moat", "壁垒", 5)]


def main():
    ap = argparse.ArgumentParser(description="five-link chain check")
    ap.add_argument("--scores", required=True, help="JSON 对象, 键为五段英文名, 值 1-10")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        scores = json.loads(args.scores)
    except json.JSONDecodeError as e:
        sys.stderr.write("[9] JSON 解析失败: %s\n" % e)
        sys.exit(9)

    if not isinstance(scores, dict):
        sys.stderr.write("[1] --scores 必须是 JSON 对象\n")
        sys.exit(1)

    missing = [k for k, _, _ in LINKS if k not in scores]
    if missing:
        sys.stderr.write("[1] 缺段: %s\n" % missing)
        sys.exit(1)
    for k, v in scores.items():
        if k not in dict((x[0], x[1]) for x in LINKS):
            sys.stderr.write("[1] 未知段: %s\n" % k)
            sys.exit(1)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or not (1 <= v <= 10):
            sys.stderr.write("[1] %s 分数须 1-10: %r\n" % (k, v))
            sys.exit(1)

    avg = sum(scores[k] for k, _, _ in LINKS) / len(LINKS)
    overall = "模式基本成立" if avg >= 7 else ("模式有硬伤需修复" if avg >= 4 else "模式不成立，需重新定位")
    # 串联链：最上游断点 = 主断点
    main_break = None
    for k, name, threshold in LINKS:
        if scores[k] < threshold:
            main_break = name
            break
    rows = []
    for k, name, threshold in LINKS:
        flag = "断点" if scores[k] < threshold else "通过"
        rows.append({"段": name, "分": scores[k], "状态": flag})

    result = {
        "总评": overall,
        "均分": round(avg, 2),
        "五段链": rows,
        "主断点": main_break or "无单点断点",
        "修复原则": "串联链只修最上游断点" if main_break else "出增长优先级（下一阶段增量在哪）",
        "旁支断点": [r["段"] for r in rows if r["状态"] == "断点" and r["段"] != main_break],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("总评: %s（均分 %.2f）" % (result["总评"], result["均分"]))
        for r in rows:
            print("  %s %s: %s [%s]" % ("🔴" if r["状态"] == "断点" else "🟢", r["段"], r["分"], r["状态"]))
        print("主断点: %s" % result["主断点"])
        if result["旁支断点"]:
            print("旁支断点(当前不动): %s" % "、".join(result["旁支断点"]))
    sys.exit(0)


if __name__ == "__main__":
    main()
