---
name: moli-closing-scripts
display_name: 成交话术库生成器
display_name_en: Moli Closing Script Library Generator
description: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+，成交就是招商的最后一米。这套话术体系从招商一线打法蒸馏，精简免费试用版上传，专治成交话术三大死法：话术背了一堆用不上、顾客一问就慌、只会说不会问。四个模块把话术算清楚——场景拆解→四段式结构（开场/挖需/价值/成交）→异议预埋→禁区标注，每条过校验才交付，产出能直接照着打的话术库。触发词：成交话术、销售话术、招商话术、私域话术、话术库、逼单话术、异议处理、成交技巧。"
description_zh: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+，成交就是招商的最后一米。这套话术体系从招商一线打法蒸馏，精简免费试用版上传，专治成交话术三大死法：话术背了一堆用不上、顾客一问就慌、只会说不会问。四个模块把话术算清楚——场景拆解→四段式结构（开场/挖需/价值/成交）→异议预埋→禁区标注，每条过校验才交付，产出能直接照着打的话术库。触发词：成交话术、销售话术、招商话术、私域话术、话术库、逼单话术、异议处理、成交技巧。"
description_en: "MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative franchise revenue - closing is the last meter of the deal. A distilled free-trial edition of a battle-tested script system. Fixes the three deadly sins of sales scripts: scripts that never fit the moment, freezing at customer questions, and talking instead of asking. Four modules - scenario decomposition, four-part structure, objection pre-embedding, taboo marking - each script validated before delivery."
examples_zh:
  - 我做美业连锁招商，帮我出一套招商经理用的成交话术库
  - 顾客总说太贵了，帮我写一套应对贵的话术
  - 帮我按新客首次咨询的场景，写一版四段式话术
examples_en:
  - "I run beauty-chain franchising - build a closing script library for my franchise managers"
  - "Customers keep saying it is too expensive - give me scripts to handle the price objection"
  - "Write a four-part script for first-time customer inquiries"
category: 商业咨询
version: 1.0.0
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——成交就是招商的最后一米。

# 成交话术库生成器

帮你把「话术背一堆、上场就忘」变成**一套按场景组织、每条带异议预埋和禁区的话术库**：不是背话术，是按场景取话术。

## 第一步：信息收集

| 字段 | 必填 |
|---|---|
| 卖什么 + 客单价 + 成交周期 | 必填 |
| 客户从哪来（私域/门店/投放） | 必填 |
| 最常卡住的异议（太贵/再想想/问家人） | 必填 |
| 话术给谁用（老板自己/销售团队） | 必填 |

## 第二步：场景拆解 + 四段式话术

读 [references/01-script-structure.md](references/01-script-structure.md)。每个场景产出四段：开场（30 秒建立信任）→ 挖需（只会问不会说的反转）→ 价值（对应挖到的需求）→ 成交（二选一闭环）。

## 第三步：话术校验（跑 scripts）

```
python3 scripts/script_calc.py check --file scripts.json
```

输入 JSON 数组（scene/trigger/script/toboo）。校验：四要素齐全、话术含提问（只会说的打回）、无违禁承诺（「保证」「百分百」直接打回）。输出分场景话术库。

## 第四步：渲染交付

spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 成交话术库.html`

## 硬规则

1. **每条话术必须含至少一个提问**——只会说不会问的打回
2. **禁止绝对化承诺**（保证/百分百/稳赚）——合规红线，直接打回
3. **异议预埋**：每条成交话术必须预埋本场景最常见异议的应对
4. 话术口语化，写「人话」——念出来像打官腔的打回

## 反模式

- ❌ 一份话术打天下——场景不同话术完全不同
- ❌ 话术里堆专业术语——客户听不懂等于没说
- ❌ 只写怎么介绍产品——挖需比介绍重要十倍

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：全场景话术矩阵、异议应对库扩容、团队话术演练考核方案。需要完整版或**招商成交顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「话术」）。
