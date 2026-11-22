#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
member_system_calc.py — 私域会员体系搭建的计算引擎。
四条命令：tiers(等级门槛) / points(积分财务) / paid(付费会员卡) / rfm(RFM分层)。

数字输入全部走 _num() 安全转换：兼容千分位逗号、%、元、万/千/亿单位。
任何参数缺失/非法/除零 → exit 1 并给中文错误，绝不 crash、绝不输出负 ROI 假结果。

用法示例:
  python3 member_system_calc.py tiers --avg-order 45 --annual-frequency 18 --gross-margin 45% --members 3.2万
  python3 member_system_calc.py points --monthly-gmv 80万 --issue-rate 1 --points-value 100 --redeem-rate 55% --gross-margin 45%
  python3 member_system_calc.py paid --card-price 199 --members 3.2万 --take-rate 6% --benefit-cost 80 --renew-rate 35%
  python3 member_system_calc.py rfm --file users.json

退出码: 0 成功; 1 参数错误或校验不通过; 9 文件解析失败。
"""
import argparse
import json
import statistics
import sys


def _num(v, field="数值"):
    """安全数字转换：兼容 '75,600' '45%' '80万' '199元' '0.99'。"""
    if v is None:
        _die("缺少参数 %s" % field)
    s = str(v).strip().replace(",", "").replace("，", "").replace("元", "").replace("块", "")
    if not s:
        _die("参数 %s 为空" % field)
    pct = s.endswith("%")
    if pct:
        s = s[:-1].strip()
    mult = 1.0
    for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3), ("天", 1), ("日", 1)):
        if s.endswith(suf):
            mult = m
            s = s[: -len(suf)].strip()
            break
    try:
        n = float(s) * mult
    except ValueError:
        _die("参数 %s 不是合法数字: %r" % (field, v))
    if pct:
        n = n / 100.0
    return n


def _die(msg, code=1):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def _pct(v, field):
    """百分比参数：接受 '45%' 或 '0.45'，归一为小数，强制 0-100% 范围校验。"""
    s = str(v).strip()
    if s.endswith("%"):
        n = _num(v, field)
    else:
        n = _num(v, field)
        if n > 1:
            n = n / 100.0
    if not (0 <= n <= 1):
        _die("参数 %s 应为 0-100%% 之间的比例，得到 %r" % (field, v))
    return n


# ---------------- tiers：会员等级门槛 ----------------
def cmd_tiers(a):
    avg_order = _num(a.avg_order, "--avg-order 客单价")
    freq = _num(a.annual_frequency, "--annual-frequency 年购买次数")
    margin = _pct(a.gross_margin, "--gross-margin 毛利率")
    members = _num(a.members, "--members 会员规模")
    if avg_order <= 0 or freq <= 0:
        _die("客单价和年购买次数必须大于 0")
    if members <= 0:
        _die("会员规模必须大于 0")
    annual = avg_order * freq
    # 帕累托分层：普通60% / 银30% / 金8% / 黑2%
    ladder = [
        ("普通会员", 0, 60, "入会即得", "新客首单礼+积分累积"),
        ("银卡会员", round(annual), 30, "年消费 ≥ %.0f 元（约 %.0f 单）" % (annual, annual / avg_order), "生日券+积分加速1.2x"),
        ("金卡会员", round(annual * 2.5), 8, "年消费 ≥ %.0f 元（约 %.0f 单）" % (annual * 2.5, annual * 2.5 / avg_order), "专属折扣+免邮+优先客服"),
        ("黑卡会员", round(annual * 6), 2, "年消费 ≥ %.0f 元（约 %.0f 单）" % (annual * 6, annual * 6 / avg_order), "1v1顾问+新品试用心+专属价"),
    ]
    # 高价值层贡献校验：2%的黑卡按帕累托贡献约 25-30% GMV
    top_gmv_share = 0.28
    out = {
        "command": "tiers",
        "inputs": {"avg_order": avg_order, "annual_frequency": freq, "gross_margin": margin, "members": members},
        "annual_spend_per_member": round(annual, 2),
        "annual_member_gmv": round(annual * members, 2),
        "top2pct_gmv_share_assumed": top_gmv_share,
        "ladder": [
            {"tier": t, "threshold_spend": th, "threshold_points": th, "share_pct": sh,
             "rule": rule, "benefits_hint": hint}
            for t, th, sh, rule, hint in ladder
        ],
        "rules": [
            "成长值 = 1 元消费 = 1 成长值（含实付金额，不含运费与券抵扣）",
            "保级周期 12 个月：到期按近 12 个月消费重算，只降一级不清零（降级创伤控制在最小）",
            "等级数 ≤ 4：每多一级，运营成本和用户认知成本同步翻倍",
            "升级当日必须弹权益（即时满足），降级提前 30 天短信预警",
        ],
        "verdict": "PASS" if margin >= 0.2 else "WARN",
        "verdict_note": "毛利率 %.0f%%，%s" % (
            margin * 100,
            "支撑四级体系；高权益集中于黑卡 2% 人群" if margin >= 0.2 else "毛利偏薄，建议先做两级（普通+银卡），金卡黑卡后置",
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


# ---------------- points：积分财务测算 ----------------
def cmd_points(a):
    gmv = _num(a.monthly_gmv, "--monthly-gmv 月GMV")
    issue_rate = _num(a.issue_rate, "--issue-rate 每1元发放积分")  # 1 元 = N 分
    points_value = _num(a.points_value, "--points-value 多少分=1元")
    redeem = _pct(a.redeem_rate, "--redeem-rate 积分消耗率")
    margin = _pct(a.gross_margin, "--gross-margin 毛利率")
    if gmv <= 0 or issue_rate <= 0 or points_value <= 0:
        _die("月GMV、发放率、积分面值都必须大于 0")
    if not (0 < redeem <= 1):
        _die("积分消耗率应在 0-100% 之间")
    if not (0 < margin < 1):
        _die("毛利率应在 0-100% 之间")
    issued_points = gmv * issue_rate            # 每月发放积分
    issued_yuan = issued_points / points_value  # 发放积分对应人民币负债
    redeemed_yuan = issued_yuan * redeem        # 当期实际消耗（真实成本）
    cost_rate = redeemed_yuan / gmv             # 成本率 = 消耗/GMV
    liability = issued_yuan * (1 - redeem)      # 未消耗积分 = 财务负债
    margin_redline = gmv * margin * 0.2         # 红线：积分成本 ≤ 毛利的 20%
    ok = redeemed_yuan <= margin_redline
    out = {
        "command": "points",
        "inputs": {"monthly_gmv": gmv, "issue_rate_per_yuan": issue_rate,
                   "points_per_yuan_value": points_value, "redeem_rate": redeem, "gross_margin": margin},
        "monthly_issued_points": round(issued_points),
        "monthly_issued_liability_yuan": round(issued_yuan, 2),
        "monthly_redeemed_cost_yuan": round(redeemed_yuan, 2),
        "cost_rate_of_gmv": round(cost_rate, 4),
        "unredeemed_liability_yuan": round(liability, 2),
        "redline_cost_yuan": round(margin_redline, 2),
        "redline_rule": "积分核销成本 ≤ 毛利的 20%%（即 ≤ GMV 的 %.1f%%）" % (margin * 20),
        "verdict": "PASS" if ok else "FAIL",
        "verdict_note": (
            "积分成本率 %.2f%%，红线内，方案可上线" % (cost_rate * 100)
            if ok else
            "积分成本率 %.2f%% 超红线（上限 %.2f%%）。修复优先级：① 降发放率至 %.2f 分/元 ② 提消耗门槛（设有效期）③ 缩权益核销面"
            % (cost_rate * 100, margin * 20, issue_rate * margin_redline / max(redeemed_yuan, 1e-9))
        ),
        "rules": [
            "发放口径：仅实付金额计积分，退款同步扣回",
            "积分有效期 12 个月滚动清零（未清零 = 财务负债滚雪球）",
            "消耗场景必须 ≥ 3 个：抵现、兑券、兑品，避免只进不出",
            "防薅：单用户单日获取上限 500 分，退款订单扣回积分",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


# ---------------- paid：付费会员卡测算 ----------------
def cmd_paid(a):
    price = _num(a.card_price, "--card-price 卡价")
    members = _num(a.members, "--members 会员规模")
    take = _pct(a.take_rate, "--take-rate 购买率")
    benefit = _num(a.benefit_cost, "--benefit-cost 单人权益成本")
    renew = _pct(a.renew_rate, "--renew-rate 续费率")
    if price <= 0 or members <= 0:
        _die("卡价和会员规模必须大于 0")
    if benefit < 0:
        _die("单人权益成本不能为负")
    buyers = members * take
    revenue = buyers * price
    cost = buyers * benefit
    profit = revenue - cost
    unit_margin = price - benefit
    ltv2 = unit_margin * (1 + renew)
    # 经济学：权益成本是按人变动成本，只要卡价 > 单人成本，每卖一张赚一张
    ok = unit_margin > 0
    if ok:
        verdict_note = (
            "每张卡毛利 %.0f 元（卡价 %.0f - 权益成本 %.0f），首年利润 %.0f 元；两年 LTV %.0f 元/人。注意：购买率 %.1f%% 是否现实要拿同类目基准（3-15%%）校验"
            % (unit_margin, price, benefit, profit, ltv2, take * 100)
        )
    else:
        verdict_note = (
            "每卖一张亏 %.0f 元（卡价 %.0f < 权益成本 %.0f）。修复优先级：① 提卡价至 %.0f 元以上 ② 砍权益或改按需核销（用才产生成本）③ 缩权益面"
            % (abs(unit_margin), price, benefit, benefit * 1.5)
        )
    out = {
        "command": "paid",
        "inputs": {"card_price": price, "members": members, "take_rate": take,
                   "benefit_cost_per_member": benefit, "renew_rate": renew},
        "buyers": round(buyers),
        "first_year_revenue": round(revenue, 2),
        "first_year_benefit_cost": round(cost, 2),
        "first_year_profit": round(profit, 2),
        "unit_margin_per_card": round(unit_margin, 2),
        "two_year_ltv_per_buyer": round(ltv2, 2),
        "verdict": "PASS" if ok else "FAIL",
        "verdict_note": verdict_note,
        "rules": [
            "权益成本必须按「核销率×单次成本」估，不要按 100% 核销拍",
            "卡价锚点：月均消费 × 6-10%（让用户一眼算出回本）",
            "首版权益 ≤ 5 项：1 个王牌权益 + 4 个零边际成本权益（身份/优先级类）",
            "续费率 < 30% 时优先修续费体验，别急着拉新",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


# ---------------- rfm：RFM 分层 ----------------
def cmd_rfm(a):
    if not a.file:
        _die("缺少 --file 用户消费记录 JSON")
    try:
        users = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:
        _die("解析 %s 失败: %s" % (a.file, e), 9)
    if not isinstance(users, list) or not users:
        _die("users.json 必须是非空数组，元素含 recency_days/frequency/monetary")
    recs = []
    for i, u in enumerate(users):
        try:
            r = float(_num(u.get("recency_days", u.get("r")), "recency_days"))
            f = float(_num(u.get("frequency", u.get("f")), "frequency"))
            m = float(_num(u.get("monetary", u.get("m")), "monetary"))
        except SystemExit:
            _die("users[%d] 缺 recency_days/frequency/monetary 字段" % i)
        recs.append((r, f, m))
    r_med = statistics.median([x[0] for x in recs])
    f_med = statistics.median([x[1] for x in recs])
    m_med = statistics.median([x[2] for x in recs])
    groups = {
        "重要价值客户(R高F高M高)": {"action": "VIP 专属权益+新品优先，重点防流失"},
        "重要保持客户(R低F高M高)": {"action": "唤醒：定向券+流失预警回访，7 天内触达"},
        "重要发展客户(R高F低M高)": {"action": "提频：客单已高，推连带与订阅制"},
        "重要挽留客户(R低F低M高)": {"action": "强召回：大额回归券+电话回访，本月必须动"},
        "一般价值客户(R高F高M低)": {"action": "提客单：满减阶梯+组合装"},
        "一般保持客户(R低F高M低)": {"action": "轻度唤醒： pushed 优惠券，不投入人工"},
        "一般发展客户(R高F低M低)": {"action": "新客培育：首购后 3 次触达 SOP"},
        "流失客户(R低F低M低)": {"action": "不主动投入，等大促自然回流"},
    }
    seg = {k: 0 for k in groups}
    for r, f, m in recs:
        rh, fh, mh = r <= r_med, f >= f_med, m >= m_med
        key = ("重要" if (mh or fh or rh) and (fh or mh) else "一般") if True else ""
        # 标准八分法
        if rh and fh and mh: k = "重要价值客户(R高F高M高)"
        elif (not rh) and fh and mh: k = "重要保持客户(R低F高M高)"
        elif rh and (not fh) and mh: k = "重要发展客户(R高F低M高)"
        elif (not rh) and (not fh) and mh: k = "重要挽留客户(R低F低M高)"
        elif rh and fh and (not mh): k = "一般价值客户(R高F高M低)"
        elif (not rh) and fh and (not mh): k = "一般保持客户(R低F高M低)"
        elif rh and (not fh) and (not mh): k = "一般发展客户(R高F低M低)"
        else: k = "流失客户(R低F低M低)"
        seg[k] += 1
    total = len(recs)
    out = {
        "command": "rfm",
        "inputs": {"users": total, "r_median_days": r_med, "f_median": f_med, "m_median": m_med},
        "segments": [
            {"segment": k, "count": v, "pct": round(v / total, 4), "action": groups[k]["action"]}
            for k, v in sorted(seg.items(), key=lambda x: -x[1])
        ],
        "verdict": "PASS",
        "verdict_note": "按中位数切分；重要挽留+流失合计 %.0f%% 时优先做召回而非拉新" % (
            100.0 * (seg["重要挽留客户(R低F低M高)"] + seg["流失客户(R低F低M低)"]) / total),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="私域会员体系计算引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tiers", help="会员等级门槛测算")
    t.add_argument("--avg-order", required=True)
    t.add_argument("--annual-frequency", required=True)
    t.add_argument("--gross-margin", required=True)
    t.add_argument("--members", required=True)
    t.set_defaults(func=cmd_tiers)

    p = sub.add_parser("points", help="积分财务测算")
    p.add_argument("--monthly-gmv", required=True)
    p.add_argument("--issue-rate", required=True)
    p.add_argument("--points-value", required=True)
    p.add_argument("--redeem-rate", required=True)
    p.add_argument("--gross-margin", required=True)
    p.set_defaults(func=cmd_points)

    d = sub.add_parser("paid", help="付费会员卡盈亏测算")
    d.add_argument("--card-price", required=True)
    d.add_argument("--members", required=True)
    d.add_argument("--take-rate", required=True)
    d.add_argument("--benefit-cost", required=True)
    d.add_argument("--renew-rate", required=True)
    d.set_defaults(func=cmd_paid)

    r = sub.add_parser("rfm", help="RFM 八分法分层")
    r.add_argument("--file", required=True)
    r.set_defaults(func=cmd_rfm)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
