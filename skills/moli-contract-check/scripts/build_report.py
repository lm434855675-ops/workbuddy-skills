#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_report.py — moli-member-activity 的 spec.json → 自包含 HTML 渲染器（含体量闸门）。
交付标准同 moli-mall-ops：深浅色自适应、可打印。

用法:
    python3 build_report.py --schema                     # 打印区块字段 schema
    python3 build_report.py --spec plan.json --check     # 只校验体量
    python3 build_report.py --spec plan.json --out 方案.html
    python3 build_report.py --spec plan.json --out 方案.html --allow-thin

退出码: 0 成功; 2 spec 不合规或体量闸门拒绝; 3 写盘失败; 9 JSON 解析失败。
"""
import argparse
import json
import sys

BLOCK_TYPES = {"section", "tiles", "steps", "timeline", "gantt", "checklist",
               "table", "bars", "stack", "callout", "kv", "floorplan", "tree", "funnel"}
CARRY_TYPES = {"tiles", "steps", "timeline", "gantt", "checklist", "table", "bars", "stack", "floorplan", "tree", "funnel"}

SCHEMA = {
    "section": {"fields": ["title", "body"]},
    "tiles": {"fields": ["title", "items[].label,items[].value"]},
    "steps": {"fields": ["title", "items[].text"]},
    "timeline": {"fields": ["title", "items[].time,items[].action,items[].owner,items[].criterion"]},
    "gantt": {"fields": ["title", "items[].phase,items[].start,items[].end"]},
    "checklist": {"fields": ["title", "items[].text"]},
    "table": {"fields": ["title", "head[]", "rows[][]"]},
    "bars": {"fields": ["title", "items[].label,items[].value"]},
    "stack": {"fields": ["title", "items[].label,items[].value"]},
    "callout": {"fields": ["title", "body", "risk?"]},
    "kv": {"fields": ["title", "items[].label,items[].value"]},
    "floorplan": {"fields": ["title", "floors[].name,floors[].note,floors[].fold"]},
    "tree": {"fields": ["title", "nodes[].name,nodes[].children[]"]},
    "funnel": {"fields": ["title", "stages[].label,stages[].value"]},
}


def die(code, msg):
    sys.stderr.write("[%d] %s\n" % (code, msg))
    sys.exit(code)


def count_chars(blocks):
    return sum(_count_value(b) for b in blocks)


def _count_value(v):
    if isinstance(v, str):
        return len(v)
    if isinstance(v, list):
        return sum(_count_value(x) for x in v)
    if isinstance(v, dict):
        return sum(_count_value(x) for x in v.values())
    return len(str(v))


def check_body(spec):
    """结构 + 体量校验，返回错误列表。"""
    errors = []
    blocks = spec.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        return ["blocks 必须是非空数组"]
    if not spec.get("title"):
        errors.append("缺顶层 title")

    has_carry = False
    for i, b in enumerate(blocks):
        if not isinstance(b, dict):
            errors.append("block[%d] 不是对象" % i)
            continue
        bt = b.get("type")
        if bt not in BLOCK_TYPES:
            errors.append("block[%d] 类型非法: %r (可用: %s)" % (i, bt, sorted(BLOCK_TYPES)))
            continue
        if bt in CARRY_TYPES:
            has_carry = True
        # timeline criterion 强制
        if bt == "timeline":
            for it in b.get("items", []):
                if isinstance(it, dict) and not it.get("criterion"):
                    errors.append("block[%d] timeline 动作缺 criterion(判定标准): %r" % (i, it.get("action")))
        # 空内容数组检查
        for key in ("items", "rows", "floors", "nodes", "stages"):
            if key in b and not b[key]:
                errors.append("block[%d] (%s) 的 %s 为空" % (i, bt, key))
        if bt == "table":
            if not b.get("head") or not b.get("rows"):
                errors.append("block[%d] table 缺 head/rows" % i)

    if not has_carry:
        errors.append("全篇没有承载型区块(只有 section/callout 是观点文，不是可执行方案)")

    # 体量闸门
    if len(blocks) < 8:
        errors.append("区块数 %d < 8" % len(blocks))
    chars = count_chars(blocks)
    if chars < 1500:
        errors.append("正文字符数 %d < 1500" % chars)
    return errors


def render_html(spec):
    title = spec.get("title", "运营方案")
    blocks = spec.get("blocks", [])
    parts = ["<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width,initial-scale=1'>",
             "<title>%s</title><style>" % title, _CSS(), "</style></head><body>",
             "<main class='page'><h1>%s</h1>" % title]
    for b in blocks:
        parts.append(_render_block(b))
    parts.append("<div class='brandfoot'>李沫Growth · 合同风险初审清单生成器精简试用版 ｜ 完整版与陪跑顾问服务：434855675@qq.com</div>")
    parts.append("</main><script>%s</script></body></html>" % _JS())
    return "".join(parts)


def _CSS():
    return """
:root{--bg:#f6f7f9;--card:#fff;--tx:#1a1d21;--sub:#5c6470;--line:#e3e6ea;--acc:#c0392b;--ok:#1e8e5f}
@media(prefers-color-scheme:dark){:root{--bg:#14171a;--card:#1d2126;--tx:#e8eaed;--sub:#9aa3ad;--line:#2f353c;--acc:#e05a4b;--ok:#3fb27f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.7 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.page{max-width:960px;margin:0 auto;padding:32px 20px}h1{font-size:26px;border-bottom:3px solid var(--acc);padding-bottom:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:16px 0}
.card h2{font-size:17px;margin:0 0 10px;color:var(--acc)}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{border:1px solid var(--line);padding:7px 10px;text-align:left}th{background:var(--bg)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.tile{background:var(--bg);border-radius:8px;padding:12px}.tile .v{font-size:22px;font-weight:700;color:var(--acc)}
.risk{border-left:4px solid var(--acc)}
li{margin:4px 0}.tag{display:inline-block;background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:1px 8px;font-size:12px;margin:2px}
.funnel-stage{display:flex;align-items:center;margin:6px 0}.funnel-bar{height:26px;background:var(--acc);border-radius:4px;opacity:.85}
.funnel-label{width:120px;font-size:13px}.funnel-val{margin-left:8px;font-size:13px;color:var(--sub)}
@media print{body{background:#fff}.card{break-inside:avoid}}
.brandfoot{margin-top:28px;padding:10px 0 0;border-top:1px solid var(--line);font-size:12px;color:var(--sub)}
"""


def _JS():
    return """
document.querySelectorAll('.checklist input').forEach(function(c){c.addEventListener('change',function(){this.closest('li').style.opacity=this.checked?.55:1})});
"""


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _num(v):
    try:
        s = str(v).strip().replace(",", "").replace("，", "")
        if not s:
            return 0.0
        pct = s.endswith("%")
        if pct:
            s = s[:-1].strip()
        mult = 1.0
        for suf, m in (("亿", 1e8), ("万", 1e4), ("千", 1e3)):
            if s.endswith(suf):
                mult = m
                s = s[:-len(suf)].strip()
                break
        for unit in ("元", "块", "人", "个", "次"):
            if s.endswith(unit):
                s = s[:-len(unit)].strip()
        n = float(s) * mult
        return n / 100.0 if pct else n
    except (ValueError, TypeError):
        return 0.0


def _render_block(b):
    bt = b.get("type")
    title = _esc(b.get("title", ""))
    inner = ""
    if bt == "section":
        inner = "<p>%s</p>" % _esc(b.get("body", ""))
    elif bt == "callout":
        inner = "<p>%s</p>" % _esc(b.get("body", ""))
        cls = "card risk" if b.get("risk") else "card"
        return "<div class='%s'><h2>%s</h2>%s</div>" % (cls, title, inner)
    elif bt in ("tiles", "kv"):
        inner = "<div class='tiles'>" + "".join(
            "<div class='tile'><div>%s</div><div class='v'>%s</div></div>" % (_esc(i.get("label", "")), _esc(i.get("value", "")))
            for i in b.get("items", [])) + "</div>"
    elif bt in ("steps", "checklist"):
        tag = "ol" if bt == "steps" else "ul"
        def _item_text(i):
            # 兼容纯字符串和 {"text": ...} 两种 agent 自然产出
            if isinstance(i, dict):
                return str(i.get("text", ""))
            return str(i)
        items = b.get("items", [])
        if bt == "checklist":
            li = "".join("<li><label><input type=checkbox> %s</label></li>" % _esc(_item_text(i)) for i in items)
        else:
            li = "".join("<li>%s</li>" % _esc(_item_text(i)) for i in items)
        inner = "<%s>%s</%s>" % (tag, li, tag)
    elif bt == "timeline":
        li = "".join("<li><b>%s</b> %s <span class='tag'>%s</span> <span class='tag'>判定:%s</span></li>" % (
            _esc(i.get("time", "")), _esc(i.get("action", "")), _esc(i.get("owner", "")), _esc(i.get("criterion", "")))
            for i in b.get("items", []))
        inner = "<ul>%s</ul>" % li
    elif bt == "gantt":
        li = "".join("<li><b>%s</b> %s → %s</li>" % (_esc(i.get("phase", "")), _esc(i.get("start", "")), _esc(i.get("end", ""))) for i in b.get("items", []))
        inner = "<ul>%s</ul>" % li
    elif bt == "table":
        head = "".join("<th>%s</th>" % _esc(h) for h in b.get("head", []))
        rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _esc(c) for c in r) for r in b.get("rows", []))
        inner = "<table><tr>%s</tr>%s</table>" % (head, rows)
    elif bt in ("bars", "stack"):
        vals = [_num(i.get("value", 0)) for i in b.get("items", [])] or [1]
        mx = max(vals) or 1
        li = "".join("<li>%s <div class='funnel-bar' style='width:%.0f%%;display:inline-block'></div> %s</li>" % (
            _esc(i.get("label", "")), _num(i.get("value", 0)) / mx * 100, _esc(i.get("value", ""))) for i in b.get("items", []))
        inner = "<ul style='list-style:none;padding:0'>%s</ul>" % li
    elif bt == "floorplan":
        li = "".join("<li><b>%s</b> %s %s</li>" % (_esc(f.get("name", "")), _esc(f.get("note", "")),
                     ("<span class='tag'>首屏折线</span>" if f.get("fold") else "")) for f in b.get("floors", []))
        inner = "<ul>%s</ul>" % li
    elif bt == "tree":
        def node(n, depth=0):
            pad = "&nbsp;" * (depth * 4)
            s = "<li>%s%s</li>" % (pad, _esc(n.get("name", "")))
            kids = n.get("children") or []
            if kids:
                s += "<ul>%s</ul>" % "".join(node(k, depth + 1) for k in kids)
            return s
        inner = "<ul>%s</ul>" % "".join(node(n) for n in b.get("nodes", []))
    elif bt == "funnel":
        vals = [_num(s.get("value", 0)) for s in b.get("stages", [])] or [1]
        mx = max(vals) or 1
        worst_idx = vals.index(min(vals)) if len(vals) > 1 else -1
        rows = []
        for idx, s in enumerate(b.get("stages", [])):
            w = _num(s.get("value", 0)) / mx * 100
            mark = " <span class='tag' style='color:var(--acc)'>最大流失</span>" if idx == worst_idx else ""
            rows.append("<div class='funnel-stage'><div class='funnel-label'>%s</div><div class='funnel-bar' style='width:%.0f%%'></div><div class='funnel-val'>%s%s</div></div>" % (
                _esc(s.get("label", "")), w, _esc(s.get("value", "")), mark))
        inner = "".join(rows)
    return "<div class='card'><h2>%s</h2>%s</div>" % (title, inner)


def main():
    ap = argparse.ArgumentParser(description="moli-mall-ops report renderer")
    ap.add_argument("--schema", action="store_true")
    ap.add_argument("--spec")
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--allow-thin", action="store_true")
    ap.add_argument("--min-blocks", type=int, default=8)
    ap.add_argument("--min-chars", type=int, default=1500)
    args = ap.parse_args()

    if args.schema:
        print(json.dumps(SCHEMA, ensure_ascii=False, indent=2))
        sys.exit(0)
    if not args.spec:
        die(2, "缺 --spec")

    try:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        die(9, "JSON 解析失败: %s" % e)
    except OSError as e:
        die(2, "读不到 spec: %s" % e)

    errors = check_body(spec)
    if errors:
        die(2, "spec 不合规:\n  - " + "\n  - ".join(errors))

    # 体量闸门（可调阈值）
    blocks = spec.get("blocks", [])
    if not args.allow_thin:
        gate = []
        if len(blocks) < args.min_blocks:
            gate.append("区块数 %d < %d" % (len(blocks), args.min_blocks))
        chars = count_chars(blocks)
        if chars < args.min_chars:
            gate.append("正文字符数 %d < %d" % (chars, args.min_chars))
        if gate:
            die(2, "体量闸门拒绝:\n  - " + "\n  - ".join(gate) + "\n  (补内容后重跑; 诊断类快速回答才可用 --allow-thin)")

    if args.check:
        sys.stderr.write("[0] 体量校验通过: %d 区块 / %d 字符\n" % (len(blocks), count_chars(blocks)))
        sys.exit(0)
    if not args.out:
        die(2, "缺 --out")

    html = render_html(spec)
    try:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(html)
    except OSError as e:
        die(3, "写盘失败: %s" % e)
    sys.stderr.write("[0] 渲染成功: %s\n" % args.out)
    sys.exit(0)


if __name__ == "__main__":
    main()
