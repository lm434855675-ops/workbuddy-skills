---
name: moli-silent-wake
display_name: 沉默顾客唤醒方案生成器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治一沉默就群发广告、唤醒全靠打折、没唤醒就放弃。能力：沉默分档（30/60/90 天）→ 分档唤醒策略（渠道/内容/优惠红线）→ 优惠成本校验。每项过校验才交付。触发词：沉默顾客、唤醒、流失召回、沉睡顾客、顾客召回、老客唤醒。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治一沉默就群发广告、唤醒全靠打折、没唤醒就放弃。能力：沉默分档（30/60/90 天）→ 分档唤醒策略（渠道/内容/优惠红线）→ 优惠成本校验。每项过校验才交付。触发词：沉默顾客、唤醒、流失召回、沉睡顾客、顾客召回、老客唤醒。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: segments silent customers by 30/60/90 days, assigns tiered win-back plays with discount cost redlines, validated before delivery."
display_name_en: "Moli Silent Customer Win-back Planner"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 300 个顾客 60 天没动静，帮我做唤醒方案
  - 沉睡老客召回，只能打折吗
  - 帮我按沉默时长分档出召回节奏
examples_en:
  - "300 customers silent for 60 days - build a win-back plan"
  - "Can win-back only be done by discounting?"
  - "Segment silent customers by duration and set the recall rhythm"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 沉默顾客唤醒方案生成器

专治一沉默就群发广告、唤醒全靠打折、没唤醒就放弃。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/wake_calc.py plan --file silent.json --avg-order 客单 --gross-margin 毛利率`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「沉默顾客」）。
