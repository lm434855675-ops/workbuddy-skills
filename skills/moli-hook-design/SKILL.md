---
name: moli-hook-design
display_name: 引流品设计测算器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治引流品随便送、成本压垮毛利、引来薅羊毛的。能力：引流品选型（券/实物/体验/资料四类）+ 成本红线（≤客单毛利 15%）+ 兑现链路校验。每项过校验才交付。触发词：引流品、钩子设计、引流成本、进店礼、入会礼、拓客礼品、引流方案。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治引流品随便送、成本压垮毛利、引来薅羊毛的。能力：引流品选型（券/实物/体验/资料四类）+ 成本红线（≤客单毛利 15%）+ 兑现链路校验。每项过校验才交付。触发词：引流品、钩子设计、引流成本、进店礼、入会礼、拓客礼品、引流方案。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: lead-magnet selection across four types with a cost redline (<= 15% of gross margin per order) and redemption-path checks, validated before delivery."
display_name_en: "Moli Lead Magnet Cost Checker"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 烘焙店进店礼送什么好？帮我算成本
  - 引流品 12 元一个会不会亏
  - 帮我选一个低成本高转化的引流品
examples_en:
  - "What entry gift should my bakery offer? Check the cost"
  - "Is a 12 RMB hook gift losing money?"
  - "Pick me a low-cost high-conversion lead magnet"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 引流品设计测算器

专治引流品随便送、成本压垮毛利、引来薅羊毛的。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/hook_calc.py check --avg-order 客单 --gross-margin 毛利率 --hook-cost 单份成本 --hook-type 类型`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「引流品」）。
