#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compete_calc.py — 竞品五维雷达计算引擎。
命令：radar(五维对比) / gap(差距转行动)。
退出码: 0 成功; 1 参数错误。
"""
import argparse
import json
import sys

DIMS = ["定位清晰度", "货盘宽度", "流量能力", "转化效率", "壁垒深度"]

ACTIONS = {
    "定位清晰度": ["一句话重写定位：卖给谁不卖给谁（对比对手的话术拆解）", "把对手没占住的人群标签占住（详情页+私域话术同步改）"],
    "货盘宽度": ["砍掉与定位无关的 SKU，让招牌产品占比提上去", "对标对手的引流款，上一款不赚钱但拉新的入口产品"],
    "流量能力": ["抄对手的获客渠道并本地化（他投什么平台你就占什么位）", "把公域入口挂满三处：详情页/客服首响/包裹卡"],
    "转化效率": ["检查首单钩子成本是否超毛利 15% 红线并换方案", "上新客 7 天触达排期（参考公私域联动技能）"],
    "壁垒深度": ["把服务做成身份权益（对手抄不走的会员体系）", "沉淀私域数据资产：标签+RFM 分层名单"],
}


def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def _parse_scores(v, field):
    parts = [x.strip() for x in str(v).split(",")]
    if len(parts) != 5:
        _die("%s 需要 5 个分数（逗号分隔，对应：%s）" % (field, "/".join(DIMS)))
    out = []
    for x in parts:
        try:
            n = float(x.replace("分", ""))
        except ValueError:
            _die("%s 含非法分数: %r" % (field, x))
        if not (1 <= n <= 5):
            _die("分数必须 1-5，得到 %r" % x)
        out.append(n)
    return out


def cmd_radar(a):
    me = _parse_scores(a.me, "--me")
    rival = _parse_scores(a.rival, "--rival")
    rows = []
    for i, dim in enumerate(DIMS):
        d = rival[i] - me[i]
        rows.append({"dimension": dim, "me": me[i], "rival": rival[i], "gap": round(d, 1),
                     "verdict": "落后" if d > 0 else ("领先" if d < 0 else "持平")})
    # 打哪个：落后最多、且不选对手壁垒维度（壁垒是长期战，新盘打不动）
    attackable = [r for r in rows if r["gap"] > 0 and r["dimension"] != "壁垒深度"]
    attackable.sort(key=lambda r: -r["gap"])
    out = {
        "command": "radar",
        "inputs": {"me": me, "rival": rival},
        "me_total": sum(me), "rival_total": sum(rival),
        "rows": rows,
        "attack_order": [r["dimension"] for r in attackable],
        "verdict": "PASS",
        "verdict_note": (
            "总分 我 %d vs 对手 %d。打法优先级（落后最多且可动）：%s。壁垒差距不打阵地战，用会员体系换方式建。" % (
                sum(me), sum(rival), " → ".join(r["dimension"] for r in attackable) if attackable else "全维持平或领先，做深壁垒")
        ),
        "rules": [
            "打侧翼不打阵地：不硬拼对手最强维度",
            "降价是最后选项，先打差异化",
            "打分基于观察与推断，标注哪些是实测哪些是估计",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_gap(a):
    dim = a.dimension
    if dim not in DIMS:
        _die("维度必须是：%s" % "/".join(DIMS))
    me = float(a.me)
    rv = float(a.rival)
    if not (1 <= me <= 5 and 1 <= rv <= 5):
        _die("分数必须 1-5")
    if rv <= me:
        _die("该维度你已不落后，换个维度跑")
    avg_order = float(str(a.avg_order).replace(",", "").replace("元", ""))
    margin = str(a.gross_margin).strip()
    if margin.endswith("%"):
        margin = float(margin[:-1]) / 100
    else:
        margin = float(margin)
        if margin > 1:
            margin /= 100
    if not (0 < margin < 1):
        _die("毛利率应在 0-100%")
    acts = ACTIONS[dim]
    out = {
        "command": "gap",
        "inputs": {"dimension": dim, "me": me, "rival": rv, "avg_order": avg_order, "gross_margin": margin},
        "gap_score": round(rv - me, 1),
        "actions": [{"priority": i + 1, "action": t, "verify": "上线 2 周后看对应环节指标变化"} for i, t in enumerate(acts)],
        "verdict": "PASS",
        "verdict_note": "%s 差距 %.1f 分。两个动作二选一先跑，2 周后按指标复评，别同时上——分不清哪招起效" % (dim, rv - me),
        "rules": ["一次只上一个动作，2 周复评", "动作效果回写竞品档案，打法迭代"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="竞品五维雷达计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("radar", help="五维对比")
    r.add_argument("--me", required=True, help="我方 5 维分，逗号分隔")
    r.add_argument("--rival", required=True, help="对手 5 维分，逗号分隔")
    r.set_defaults(func=cmd_radar)
    g = sub.add_parser("gap", help="差距转行动")
    g.add_argument("--dimension", required=True)
    g.add_argument("--me", type=float, required=True)
    g.add_argument("--rival", type=float, required=True)
    g.add_argument("--avg-order", required=True)
    g.add_argument("--gross-margin", required=True)
    g.set_defaults(func=cmd_gap)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
