#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_script.py — moli-viral-script 的 schema 校验 + Markdown 渲染器。

用法:
    python3 render_script.py <input.json> --out <output.md>
    python3 render_script.py - --out <output.md        # 从 stdin 读 JSON

退出码:
    0  成功
    1  参数错误
    2  schema 不合规
    3  写盘失败
    9  JSON 解析失败
"""
import argparse
import json
import sys

SCRIPT_TYPES = {"recruit", "seeding", "ip_persona", "event_invite", "training"}
CAMPAIGN_TYPES = {
    "agent_recruit", "c_end_seeding", "brand_exposure",
    "fan_growth", "event_drain", "training_conversion",
}


def fail(code, msg):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def check_schema(doc):
    """返回错误列表（空 = 通过）。"""
    errors = []
    if not isinstance(doc, dict):
        return ["顶层必须是 JSON 对象"]

    for key in ("title", "duration_sec", "info", "script_type",
                "campaign_types", "structure", "rhythm", "tags"):
        if key not in doc:
            errors.append("缺顶层字段: %s" % key)

    if "title" in doc:
        t = doc["title"]
        if not isinstance(t, str) or not t.strip():
            errors.append("title 必须是非空字符串")
        elif len(t) > 15:
            errors.append("title 超长(>15字): %r" % t)

    if "duration_sec" in doc:
        d = doc["duration_sec"]
        if not isinstance(d, (int, float)) or isinstance(d, bool) or d <= 0:
            errors.append("duration_sec 必须是正数")

    info = doc.get("info")
    if isinstance(info, dict):
        for k in ("purpose", "industry", "audience", "topic"):
            if not info.get(k):
                errors.append("info.%s 缺失" % k)
    else:
        errors.append("info 必须是对象")

    st = doc.get("script_type")
    if st not in SCRIPT_TYPES:
        errors.append("script_type 非法: %r (合法值: %s)" % (st, sorted(SCRIPT_TYPES)))

    cts = doc.get("campaign_types")
    if not isinstance(cts, list) or not cts:
        errors.append("campaign_types 必须是非空数组")
    else:
        bad = [c for c in cts if c not in CAMPAIGN_TYPES]
        if bad:
            errors.append("campaign_types 含非法值: %s" % bad)

    structure = doc.get("structure")
    if isinstance(structure, dict):
        errors.extend(_check_structure(structure, doc.get("script_type"),
                                       doc.get("duration_sec")))
    elif "structure" in doc:
        errors.append("structure 必须是对象")

    rhythm = doc.get("rhythm")
    if isinstance(rhythm, dict):
        wps = rhythm.get("words_per_sec")
        if not isinstance(wps, (int, float)) or isinstance(wps, bool) or not (4 <= wps <= 5):
            errors.append("rhythm.words_per_sec 必须在 [4,5]: %r" % wps)
        pp = rhythm.get("pause_points")
        if not isinstance(pp, list) or not all(isinstance(x, (int, float)) for x in pp):
            errors.append("rhythm.pause_points 必须是数字数组")
        else:
            if pp != sorted(pp):
                errors.append("rhythm.pause_points 必须升序")
            dur = doc.get("duration_sec")
            if isinstance(dur, (int, float)) and any(x <= 0 or x >= dur for x in pp):
                errors.append("rhythm.pause_points 必须落在 (0, duration_sec) 内")
        if not rhythm.get("overall"):
            errors.append("rhythm.overall 缺失")
    elif "rhythm" in doc:
        errors.append("rhythm 必须是对象")

    tags = doc.get("tags")
    if not isinstance(tags, list) or not (2 <= len(tags) <= 5):
        errors.append("tags 必须是 2-5 个字符串的数组")

    return errors


def _check_structure(structure, script_type, duration_sec):
    errors = []
    hook = structure.get("hook")
    segs = structure.get("body", {}).get("segments") if isinstance(structure.get("body"), dict) else None
    cta = structure.get("cta")

    if not isinstance(hook, dict):
        errors.append("structure.hook 缺失或不是对象")
    if not isinstance(cta, dict):
        errors.append("structure.cta 缺失或不是对象")
    if not isinstance(segs, list) or not segs:
        errors.append("structure.body.segments 必须是非空数组")

    if isinstance(hook, dict) and hook.get("index") != 1:
        errors.append("hook.index 必须为 1")
    if isinstance(cta, dict) and cta.get("index") != 99:
        errors.append("cta.index 必须为 99")

    if isinstance(segs, list) and segs:
        limit = 7 if script_type == "training" else 5
        if len(segs) > limit:
            errors.append("segments 超上限: %d > %d (script_type=%s)" % (len(segs), limit, script_type))
        for i, seg in enumerate(segs):
            if not isinstance(seg, dict):
                errors.append("segment[%d] 不是对象" % i)
                continue
            if seg.get("index") != i + 2:
                errors.append("segment[%d].index 应为 %d, 实为 %r" % (i, i + 2, seg.get("index")))

    # 时间轴自洽
    chain = []
    if isinstance(hook, dict):
        chain.append(hook)
    if isinstance(segs, list):
        chain.extend([s for s in segs if isinstance(s, dict)])
    if isinstance(cta, dict):
        chain.append(cta)
    for i, seg in enumerate(chain):
        for f in ("start", "end"):
            v = seg.get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                errors.append("段 index=%r 的 %s 必须是数字" % (seg.get("index"), f))
        s, e = seg.get("start"), seg.get("end")
        if isinstance(s, (int, float)) and isinstance(e, (int, float)) and e <= s:
            errors.append("段 index=%r 的 end 必须大于 start" % seg.get("index"))
        if i > 0:
            prev_end = chain[i - 1].get("end")
            if isinstance(s, (int, float)) and isinstance(prev_end, (int, float)) and abs(s - prev_end) > 1e-9:
                errors.append("时间轴断裂: 段 %r 的 start(%s) != 上一段 end(%s)" % (seg.get("index"), s, prev_end))
        if not seg.get("visual") or not seg.get("dialogue"):
            errors.append("段 index=%r 的 visual/dialogue 不能为空" % seg.get("index"))
        elif len(str(seg.get("visual"))) > 50:
            errors.append("段 index=%r 的 visual 超 50 字" % seg.get("index"))

    if isinstance(cta, dict) and isinstance(duration_sec, (int, float)):
        if abs(cta.get("end", -1) - duration_sec) > 1e-9:
            errors.append("cta.end 必须等于 duration_sec")
    if isinstance(hook, dict) and hook.get("start") != 0:
        errors.append("hook.start 必须为 0")

    return errors


def render_markdown(doc):
    info = doc.get("info", {})
    lines = []
    lines.append("# 爆款脚本：%s" % doc.get("title", "(未命名)"))
    lines.append("")
    lines.append("- 类型：`%s` · 时长：%ss" % (doc.get("script_type"), doc.get("duration_sec")))
    lines.append("- 目的：%s ｜ 行业：%s" % (info.get("purpose"), info.get("industry")))
    lines.append("- 受众：%s ｜ 选题：%s" % (info.get("audience"), info.get("topic")))
    lines.append("- 结构：%s" % doc.get("structure_summary", ""))
    lines.append("- 节奏：%s（语速 %s 字/秒）" % (doc.get("rhythm", {}).get("overall"), doc.get("rhythm", {}).get("words_per_sec")))
    lines.append("- 标签：%s" % "、".join(doc.get("tags", [])))
    lines.append("")
    lines.append("## 分段表")
    lines.append("")
    lines.append("| # | 时间(s) | 画面 | 台词 |")
    lines.append("|---|---------|------|------|")

    chain = []
    structure = doc.get("structure", {})
    hook = structure.get("hook")
    segs = structure.get("body", {}).get("segments", []) if isinstance(structure.get("body"), dict) else []
    cta = structure.get("cta")
    if isinstance(hook, dict):
        chain.append(hook)
    chain.extend([s for s in (segs or []) if isinstance(s, dict)])
    if isinstance(cta, dict):
        chain.append(cta)

    for i, seg in enumerate(chain, 1):
        lines.append("| %d | %s-%s | %s | %s |" % (
            i, seg.get("start"), seg.get("end"),
            str(seg.get("visual", "")).replace("|", "/"),
            str(seg.get("dialogue", "")).replace("|", "/"),
        ))

    lines.append("")
    lines.append("## 口播全文")
    lines.append("")
    for i, seg in enumerate(chain, 1):
        role = "Hook" if seg.get("index") == 1 else ("CTA" if seg.get("index") == 99 else "中段%d" % (i - 1))
        lines.append("**【%s】** %s" % (role, seg.get("dialogue", "")))
        lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("这个技能是通用版：你的行业+数据可定制专属版——把你的产品、话术库、客户数据接进来，就是你的专属智能体。")
    lines.append("李沫Growth 招商与内容脚本 · 专属版智能体定制：434855675@qq.com（邮箱同微信号）")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="moli-viral-script renderer")
    ap.add_argument("input", help="input.json 路径, 或 - 读 stdin")
    ap.add_argument("--out", required=True, help="输出 Markdown 路径")
    args = ap.parse_args()

    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                raw = f.read()
    except OSError as e:
        fail(1, "读不到输入文件: %s" % e)

    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(9, "JSON 解析失败: %s" % e)

    errors = check_schema(doc)
    if errors:
        fail(2, "schema 不合规:\n  - " + "\n  - ".join(errors))

    md = render_markdown(doc)
    try:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
    except OSError as e:
        fail(3, "写盘失败: %s" % e)

    sys.stderr.write("[0] 渲染成功: %s\n" % args.out)
    sys.exit(0)


if __name__ == "__main__":
    main()
