---
name: moli-moments-calendar
display_name: 朋友圈运营日历生成器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治天天发广告被屏蔽、想发什么发什么、三天打鱼两天晒网。能力：30 天朋友圈内容日历（六类内容配比+黄金时段+禁发清单），按行业定制。每项过校验才交付。触发词：朋友圈运营、朋友圈日历、朋友圈文案、发圈、朋友圈内容、朋友圈广告。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治天天发广告被屏蔽、想发什么发什么、三天打鱼两天晒网。能力：30 天朋友圈内容日历（六类内容配比+黄金时段+禁发清单），按行业定制。每项过校验才交付。触发词：朋友圈运营、朋友圈日历、朋友圈文案、发圈、朋友圈内容、朋友圈广告。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: 30-day WeChat Moments content calendar with six-type mix, golden time slots, and hard-ad caps, customized per industry. Validated before delivery."
display_name_en: "Moli Moments Calendar Generator"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 我是做烘焙的，帮我排 30 天朋友圈日历
  - 朋友圈发什么没人屏蔽？给我一套配比
  - 帮我排一版招商型朋友圈
examples_en:
  - "Build a 30-day WeChat Moments calendar for my bakery"
  - "What Moments content avoids being muted? Give me the mix"
  - "Design a franchise-recruiting Moments plan"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 朋友圈运营日历生成器

专治天天发广告被屏蔽、想发什么发什么、三天打鱼两天晒网。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/moments_calc.py calendar --industry 行业 --days 30`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「朋友圈运营」）。
