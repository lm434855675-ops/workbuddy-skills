---
name: moli-fission-calc
display_name: 裂变活动方案测算器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治裂变补贴烧钱没回报、K 因子低于 1 还在烧、海报做了没人转。能力：K 因子测算（转化/参与）→ 单客成本红线校验 → 方案 PASS/FAIL。每项过校验才交付。触发词：裂变活动、裂变海报、老带新、转介绍活动、K因子、裂变成本、裂变方案。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治裂变补贴烧钱没回报、K 因子低于 1 还在烧、海报做了没人转。能力：K 因子测算（转化/参与）→ 单客成本红线校验 → 方案 PASS/FAIL。每项过校验才交付。触发词：裂变活动、裂变海报、老带新、转介绍活动、K因子、裂变成本、裂变方案。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: computes fission K-factor and cost per new customer against redlines (K >= 1, CPA <= 30% of gross margin), PASS/FAIL before spending."
display_name_en: "Moli Fission Campaign Calculator"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 老带新送 50 元券的裂变活动，帮我算算划不划算
  - K 因子多少才值得做裂变
  - 帮我测一场邀请有礼活动的成本
examples_en:
  - "Evaluate a refer-a-friend campaign with 50 RMB coupons"
  - "What K-factor makes a fission campaign worth running"
  - "Estimate the cost of an invite-rewards campaign"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 裂变活动方案测算器

专治裂变补贴烧钱没回报、K 因子低于 1 还在烧、海报做了没人转。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/fission_calc.py kfactor --invited 人数 --shares 分享人数 --conversions 转化人数 --cost 总补贴 --avg-order 客单 --gross-margin 毛利率`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「裂变活动」）。
