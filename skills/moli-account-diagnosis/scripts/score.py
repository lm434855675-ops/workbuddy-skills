#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score.py — moli-account-diagnosis 五维加权评分卡。

用法:
    python3 score.py --scores '{"traffic":5,"conversion":7,"product":6,"ops":4,"org":6}'
    python3 score.py --scores '{...}' --json

退出码: 0 成功; 1 参数错误; 9 JSON 解析失败。
"""
import argparse
import json
import sys

WEIGHTS = {"traffic": 0.25, "conversion": 0.25, "product": 0.20, "ops": 0.15, "org": 0.15}
NAMES = {"traffic": "流量结构", "conversion": "转化链路", "product": "产品货盘", "ops": "运营能力", "org": "组织执行"}


def light(score):
    if score >= 7:
        return "绿灯"
    if score >= 4:
        return "黄灯"
    return "红灯"


def main():
    ap = argparse.ArgumentParser(description="five-dimension weighted scorer")
    ap.add_argument("--scores", required=True, help='JSON 对象, 键为五维英文名, 值 1-10')
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

    missing = [k for k in WEIGHTS if k not in scores]
    if missing:
        sys.stderr.write("[1] 缺维度: %s\n" % missing)
        sys.exit(1)
    for k, v in scores.items():
        if k not in WEIGHTS:
            sys.stderr.write("[1] 未知维度: %s (合法: %s)\n" % (k, sorted(WEIGHTS)))
            sys.exit(1)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or not (1 <= v <= 10):
            sys.stderr.write("[1] %s 分数必须是 1-10: %r\n" % (k, v))
            sys.exit(1)

    total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    overall_light = light(total)
    result = {
        "总分": round(total, 2),
        "总评灯": overall_light,
        "分维": [
            {"维度": NAMES[k], "键": k, "得分": scores[k], "权重": WEIGHTS[k],
             "加权": round(scores[k] * WEIGHTS[k], 2), "灯": light(scores[k])}
            for k in WEIGHTS
        ],
        "红灯维度": [NAMES[k] for k in WEIGHTS if scores[k] < 4],
        "说明": "绿灯>=7, 黄灯4-6, 红灯<4; 总分=加权和",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("总分: %.2f [%s]" % (result["总分"], result["总评灯"]))
        for d in result["分维"]:
            print("  %s %s: %s (权重%.2f 加权%.2f)" % (d["灯"], d["维度"], d["得分"], d["权重"], d["加权"]))
        if result["红灯维度"]:
            print("红灯维度: %s" % "、".join(result["红灯维度"]))
        else:
            print("无红灯维度")
    sys.exit(0)


if __name__ == "__main__":
    main()
