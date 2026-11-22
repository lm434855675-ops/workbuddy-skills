#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文案合规检查：极限词 + 结构性规则（短信 / 裂变 / 会员储值 / Banner）。

用法:
  python3 scripts/check_copy.py --scope banner 文案.txt
  python3 scripts/check_copy.py --scope all 文案.txt

退出码: 0=无命中；1=有必改项；2=无必改但有建议项。
安全边界: 全程不联网，只读调用方传入的本地文件，不调用外部进程。
"""
import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# 极限词：广告法高风险表述。单字「最 / 第一」用组合词判定，避免「最近 / 最后一个」误报。
ABSOLUTE = [
    "顶级", "绝对", "100%", "史上", "独家", "国家级", "吊打", "封神",
    "绝了", "无敌", "销量冠军", "领导者", "极致", "全网最低", "最低价",
    "最便宜", "最划算", "最优质", "最先进", "最好用", "最强", "最高级",
    "第一品牌", "行业第一", "销量第一", "全国第一", "排名第一",
    "最低", "最好", "最佳", "最优", "最高", "最大",
]
SOFT_ABSOLUTE = ["最后.*?小时", "仅剩.*?[件份席]", "限时.*?秒", "抢完.*?为止", "手慢无"]

SCOPES = ("banner", "sms", "member", "share", "all")


def read_text(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def scan_absolute(text):
    """返回 [(行号, 原句, 命中词)]。长词优先并挖掉已命中片段，避免「全网最低价」同时报三个词。"""
    words = sorted(ABSOLUTE, key=len, reverse=True)
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        work = s
        for w in words:
            if w in work:
                out.append((i, s, w))
                work = work.replace(w, "\u0000" * len(w))
        for p in SOFT_ABSOLUTE:
            m = re.search(p, line)
            if m:
                out.append((i, s, m.group(0)))
    return out


def check_sms(text):
    bad, warn = [], []
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if not re.match(r"^【[^】]{1,16}】", s):
            bad.append((i, s, "短信正文必须以【签名】开头"))
        if not re.search(r"退订|回\s*TD", s):
            bad.append((i, s, "缺退订标识，加「回 TD 退订」"))
        body = re.sub(r"^【[^】]{1,16}】", "", s)
        body = re.sub(r"[（(]?回\s*TD\s*退订[）)]?", "", body).strip()
        if len(body) > 70:
            bad.append((i, s, "正文 %d 字，超 70 字上限，需压缩" % len(body)))
    return bad, warn


def check_share(text):
    bad, warn = [], []
    hard = [r"(分享|转发|关注)[^。\n]{0,12}(才能|才可|即可|可)[^。\n]{0,6}(领|得|解锁|获得)",
            r"(分享|转发|关注)[^。\n]{0,10}(领|得|解锁|获得)[^。\n]{0,6}(券|礼|奖|资格)"]
    soft = [r"邀请\s*\d+\s*人[^。\n]{0,8}(领|得|送|获)",
            r"(\d+)\s*人(助力|集赞|砍价)[^。\n]{0,6}(得|领|减)"]
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        for p in hard:
            if re.search(p, s):
                bad.append((i, s, "把分享/转发/关注设为领奖前置，微信判诱导分享，链接会被拦截"))
                break
        for p in soft:
            if re.search(p, s):
                warn.append((i, s, "邀请/助力领奖属高风险玩法，建议改为直接领券或会员日专属价"))
                break
    return bad, warn


def check_member(text):
    bad, warn = [], []
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if "自动续费" in s:
            if not re.search(r"周期|每(月|季|年)", s):
                bad.append((i, s, "自动续费未明示扣费周期"))
            if not re.search(r"取消|关闭", s):
                bad.append((i, s, "自动续费未明示取消路径"))
        if "储值" in s:
            if not re.search(r"有效期|长期有效|不设期限|退款", s):
                warn.append((i, s, "储值未说明有效期与退款规则，易被判不合理限制"))
        if re.search(r"原价|划线价|日常价", s):
            warn.append((i, s, "划线价须为真实成交过的价格，留存后台成交记录举证"))
        if re.search(r"拉人头|人头提成|层级返佣", s):
            bad.append((i, s, "多级分销表述踩传销特征，改为「销售分润」"))
    return bad, warn


def check_banner(text):
    bad, warn = [], []
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if re.search(r"(倒计时|最后|仅剩|名额)", s) and not re.search(r"\d", s):
            warn.append((i, s, "名额/倒计时无具体数字，易被判虚假活动，补真实截止时间与数量"))
    return bad, warn


def run(text, scope):
    bad, warn = [], []
    a = scan_absolute(text)
    for i, s, w in a:
        bad.append((i, s, "极限词「%s」，改为可核对的具体表述（价格/数据/时间）" % w))
    if scope in ("sms", "all"):
        b, w2 = check_sms(text)
        bad += b
        warn += w2
    if scope in ("share", "all"):
        b, w2 = check_share(text)
        bad += b
        warn += w2
    if scope in ("member", "all"):
        b, w2 = check_member(text)
        bad += b
        warn += w2
    if scope in ("banner", "all"):
        b, w2 = check_banner(text)
        bad += b
        warn += w2
    return bad, warn


def selftest():
    cases = [
        ("banner", "全网最低价，仅限今天，手慢无", True),
        ("sms", "【某商城】会员日全场 8 折，回 TD 退订", False),
        ("sms", "会员日全场 8 折", True),
        ("share", "分享给 3 位好友即可领取 20 元券", True),
        ("member", "开通自动续费立减 10 元", True),
        ("banner", "新品上架，尺码表在第 4 屏", False),
    ]
    ok = 0
    for scope, text, expect_bad in cases:
        bad, warn = run(text, scope)
        got = bool(bad)
        flag = "PASS" if got == expect_bad else "FAIL"
        if got == expect_bad:
            ok += 1
        print("[%s] %s | %s | 必改 %d 建议 %d" % (flag, scope, text[:28], len(bad), len(warn)))
    print("selftest: %d/%d" % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_copy.py",
        description="文案合规检查：极限词 + 短信/裂变/会员储值/Banner 结构规则。纯本地，零网络调用。")
    ap.add_argument("file", nargs="?", help="待检查的文案文件（UTF-8 纯文本）")
    ap.add_argument("--scope", default="all", choices=list(SCOPES),
                    help="检查范围，默认 all")
    ap.add_argument("--selftest", action="store_true", help="跑内置自检，退出码 0 表示通过")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        if not args.file:
            print("ERROR: 需要给出待检查文件，例如 check_copy.py --scope banner 文案.txt", file=sys.stderr)
            return 2
        if not os.path.isfile(args.file):
            print("ERROR: 文件不存在: %s" % args.file, file=sys.stderr)
            return 2
        text = read_text(args.file)
        bad, warn = run(text, args.scope)
        for i, s, why in bad:
            print("[必改] L%d 「%s」 → %s" % (i, s[:50], why))
        for i, s, why in warn:
            print("[建议] L%d 「%s」 → %s" % (i, s[:50], why))
        print("\n汇总：必改 %d 条 / 建议 %d 条 / 范围 %s" % (len(bad), len(warn), args.scope))
        if bad:
            return 1
        return 2 if warn else 0
    except (OSError, ValueError, UnicodeError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
