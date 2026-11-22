---
name: tencent-docx-html2docx-pipeline
display_name: 腾讯文档 html→docx 重排版管线
version: 1.0.0
author: 文鹏飞
category: 办公效率
description: 直接驱动 tencent-docx 插件的 html_to_docx 引擎重新生成 Word（含小页边距、致辞/附录单独分页、审门禁全过）的完整命令与坑清单。触发：要重新排版/改边距/加独立一页/重生成已有 docx，或 html_to_docx 报 ModuleNotFoundError: No module named 'click'。
---

# tencent-docx html→docx 直驱管线（重生 Word 文档）

## 适用
对已生成的 docx 做**大幅改版**（精简内容、改页边距、加独立分页章节）时，别用编辑器逐段改——直接改 stage2 HTML 重新转换，路径可控、可校验。

## 关键路径

> 插件根路径因安装方式而异：在 WorkBuddy 插件管理中查看 tencent-docx 插件的安装目录，或在本机 WorkBuddy 数据目录下搜索 `plugins/cache/workbuddy-builtin/tencent-docx`。
- 插件根：`<WorkBuddy 数据目录>\plugins\cache\workbuddy-builtin\tencent-docx\<插件版本>`
- 转换器包：`<插件根>\skills\html-to-docx\scripts`（`html_to_docx` 包 + `requirements.txt`）
- 托管 venv 解释器：`%USERPROFILE%\.venv-html-to-docx\Scripts\python.exe`（**不是** bin/python）
- 审查脚本：`<插件根>\skills\html-review\scripts\review_html.py --html <file> --genre general`（≥80 过门）

## ⚠️ 头号坑：venv 依赖偶发丢失
`ModuleNotFoundError: No module named 'click'` 会**复发**（uv 管的 venv 里没有 pip，setup 脚本的安装步骤曾被 `>/dev/null` 吞掉失败）。
每次转换前无脑跑一遍（幂等、缓存后秒级）：
```bash
UV="$HOME/.local/bin/uv"
PY="$HOME/.venv-html-to-docx/Scripts/python.exe"
"$UV" pip install --python "$PY" --only-binary=:all: -r "<插件根>/skills/html-to-docx/scripts/requirements.txt"
```
venv 没建过则先跑 `<插件根>\scripts\wb\local\setup-html-to-docx.sh`（需可访问外网的代理环境）。

## 转换命令模板
```bash
PYTHONPATH="<插件根>/skills/html-to-docx/scripts" "$PY" -m html_to_docx convert in.html -o out.docx \
  --page-size A4 --margin-top 1.2 --margin-bottom 1.2 --margin-left 1.2 --margin-right 1.2
```
成功 stdout 输出 JSON（含空单元格自动生成的书签 fields，无害）。

## 某章单独一页（分页）的正确姿势
- 转换器**只认顶层 `<section>`**：section[0] 不插分页，section[1..N-1] 前自动插 nextPage 分节符。
- 所以要分页必须有**两个**顶层 section：`<section role="main">正文全部</section><section role="speeches">致辞</section>`。只包一个 section 会当 index=0 → 没有分页！
- 每节边距用 `data-margin-top/bottom/left/right="1.2"`（cm，浮点）防第二页边距被重置。
- CSS `page-break-before` 无效（转换器不解析该 CSS→OOXML）。

## review_html.py 门禁硬规则（不过 80 白干）
- `:root{}` 必须含短名 `--fs-body`、`--color-text`、`--ff-body`（编译令牌的全名 `--typography-fontSize-body` 不算数，两套都写最稳）。
- 所有 color/font-size/margin/padding/font-family 一律 `var(--*)`；`0.5em` 这种裸值会命中 DT-03（em 在单位黑名单）；`border: 1px solid` 和 `cm` 单位不查。
- 表格必须 `<thead>`+`<tbody>` 且表头用 `<th>`。
- 标题不跳级；**h2 后紧跟 h3 中间必须有正文**（TQ-03，加一句引导 `<p>` 即可）；h1 只能 1 个。
- 不用 `<script>`/外部资源/`<span>` 徽章（background+padding 模式）/`<hr>`。

## 转完必校验（python-docx 一段脚本）
- `len(d.sections)` == 预期节数（分页是否生效）
- 每节 `top/bottom/left/right_margin.cm` == 预期边距
- 关键标题/★习俗标注在文本里、`alltext.count("□")` 勾选框数
- 表头 `[c.text for c in d.tables[i].rows[0].cells]`

## 产物落盘
数据一律 `<WorkBuddy 数据目录>\projects\<项目>\`（严禁应用安装目录内、严禁系统盘工作区）；转完 present_files 打开预览 + 聊天里贴核心内容。
