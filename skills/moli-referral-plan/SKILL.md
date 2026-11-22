---
name: moli-referral-plan
display_name: 老顾客转介绍方案生成器
display_name_en: "Moli 老顾客转介绍方案生成器"
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治转介绍全靠人情开口、激励拍脑袋亏钱、介绍完没下文。能力：转介绍激励测算（老客奖励+新客礼双向设计）→ 单新客成本红线校验（≤客单毛利 30%）→ 追踪闭环。每项过校验才交付。触发词：转介绍、老带新、顾客推荐、转介绍激励、介绍有礼、裂变转介绍、口碑推荐。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治转介绍全靠人情开口、激励拍脑袋亏钱、介绍完没下文。能力：转介绍激励测算（老客奖励+新客礼双向设计）→ 单新客成本红线校验（≤客单毛利 30%）→ 追踪闭环。每项过校验才交付。触发词：转介绍、老带新、顾客推荐、转介绍激励、介绍有礼、裂变转介绍、口碑推荐。"
description_en: "MoliGrowth official. 15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队 A distilled free-trial edition, validated before delivery."
category: 商业咨询
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 儿童摄影店想做老带新，帮我设计激励方案算算成本
  - 老顾客转介绍怎么给奖励才不亏？
  - 帮我把转介绍做成常规动作而不是一次性活动
examples_en:
  - "My kids-photography studio wants a referral program - design incentives and check costs"
  - "How to reward referrals without losing money?"
  - "Make referrals a routine motion, not a one-off campaign"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 老顾客转介绍方案生成器

专治转介绍全靠人情开口、激励拍脑袋亏钱、介绍完没下文。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/referral_calc.py`（参数见下方命令）
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「转介绍」）。
