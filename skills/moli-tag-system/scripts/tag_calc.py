#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tag_calc.py — 私域标签体系计算引擎。
命令：rfm(全量 RFM 八分法 + 分层名单导出)。
输入 JSON 数组，元素含 user/recency_days/frequency/monetary（兼容千分位/万单位）。
退出码: 0 成功; 1 参数错误; 9 文件解析失败。
"""
import argparse
import csv
import json
import statistics
import sys


def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def _num(v, field="数值"):
    if v is None:
        _die("缺少字段 %s" % field)
    s = str(v).strip().replace(",", "").replace("，", "").replace("元", "")
    if not s:
        _die("字段 %s 为空" % field)
    mult = 1.0
    for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3), ("天", 1), ("日", 1)):
        if s.endswith(suf):
            mult = m
            s = s[: -len(suf)].strip()
            break
    try:
        return float(s) * mult
    except ValueError:
        _die("字段 %s 不是合法数字: %r" % (field, v))


SEGMENTS = {
    "重要价值客户": {"cond": (True, True, True), "action": "VIP 专属权益+新品优先，重点防流失"},
    "重要保持客户": {"cond": (False, True, True), "action": "7 天内定向唤醒券+流失预警回访"},
    "重要发展客户": {"cond": (True, False, True), "action": "提频：连带组合、订阅制"},
    "重要挽留客户": {"cond": (False, False, True), "action": "强召回：大额回归券+电话回访"},
    "一般价值客户": {"cond": (True, True, False), "action": "提客单：满减阶梯+组合装"},
    "一般保持客户": {"cond": (False, True, False), "action": "轻触达：pushed 优惠券，不投人工"},
    "一般发展客户": {"cond": (True, False, False), "action": "新客培育：首购后 3 次触达 SOP"},
    "流失客户": {"cond": (False, False, False), "action": "不主动投入，等大促自然回流"},
}


def cmd_rfm(a):
    if not a.file:
        _die("缺少 --file 用户消费记录 JSON")
    try:
        users = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析 %s 失败: %s" % (a.file, e), 9)
    if not isinstance(users, list) or not users:
        _die("输入必须是非空数组，元素含 user/recency_days/frequency/monetary")
    recs = []
    for i, u in enumerate(users):
        uid = str(u.get("user", u.get("uid", "u%d" % (i + 1))))
        try:
            r = _num(u.get("recency_days", u.get("r")), "recency_days")
            f = _num(u.get("frequency", u.get("f")), "frequency")
            m = _num(u.get("monetary", u.get("m")), "monetary")
        except SystemExit:
            _die("users[%d] 缺 recency_days/frequency/monetary 字段" % i)
        recs.append((uid, r, f, m))
    r_med = statistics.median([x[1] for x in recs])
    f_med = statistics.median([x[2] for x in recs])
    m_med = statistics.median([x[3] for x in recs])
    seg_count = {k: 0 for k in SEGMENTS}
    roster = []
    for uid, r, f, m in recs:
        rh, fh, mh = r <= r_med, f >= f_med, m >= m_med
        key = None
        for name, cfg in SEGMENTS.items():
            if cfg["cond"] == (rh, fh, mh):
                key = name
                break
        seg_count[key] += 1
        roster.append({"user": uid, "segment": key, "recency_days": r, "frequency": f, "monetary": m})
    total = len(recs)
    seg_out = [{"segment": k, "count": v, "pct": round(v / total, 4), "action": SEGMENTS[k]["action"]}
               for k, v in sorted(seg_count.items(), key=lambda x: -x[1])]
    # 名单导出
    roster_path = a.out or (a.file.rsplit(".", 1)[0] + "_roster.csv")
    with open(roster_path, "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=["user", "segment", "recency_days", "frequency", "monetary"])
        w.writeheader()
        for row in sorted(roster, key=lambda x: (x["segment"], -x["monetary"])):
            w.writerow(row)
    lost = seg_count["重要挽留客户"] + seg_count["流失客户"]
    out = {
        "command": "rfm",
        "inputs": {"users": total, "r_median_days": r_med, "f_median": f_med, "m_median": m_med},
        "segments": seg_out,
        "roster_csv": roster_path,
        "verdict": "PASS",
        "verdict_note": "按中位数切分；重要挽留+流失合计 %.0f%% 时优先做召回而非拉新（阈值 40%%）" % (100.0 * lost / total),
        "rules": [
            "R/F/M 按中位数切分，比均值抗异常值",
            "分层名单每周重跑一次，客群迁移要盯（价值客户跌入挽留 = 流失预警）",
            "重要挽留+流失 >40%：本月资源全部投召回，不投拉新",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="私域标签体系计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rfm", help="全量 RFM 八分法 + 分层名单导出")
    r.add_argument("--file", required=True, help="用户消费记录 JSON")
    r.add_argument("--out", default=None, help="分层名单 CSV 输出路径（默认输入名_roster.csv）")
    r.set_defaults(func=cmd_rfm)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
