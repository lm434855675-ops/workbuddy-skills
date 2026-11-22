---
name: moli-content-weekly
display_name: 私域内容周历生成器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治内容全靠灵感、想到啥发啥、一周发满 7 天广告。能力：一周内容周历（六类轮换+行业定制+广告占比 ≤20%）输出排期表。每项过校验才交付。触发词：内容周历、私域内容、内容排期、朋友圈周历、内容规划、社群内容。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治内容全靠灵感、想到啥发啥、一周发满 7 天广告。能力：一周内容周历（六类轮换+行业定制+广告占比 ≤20%）输出排期表。每项过校验才交付。触发词：内容周历、私域内容、内容排期、朋友圈周历、内容规划、社群内容。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: builds a weekly content calendar across Moments, groups and 1v1 with six-type rotation and hard-ad cap <= 20%, validated before delivery."
display_name_en: "Moli Private-domain Content Weekly Planner"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 帮我排一周的私域内容：朋友圈+社群+1v1
  - 私域里一周该发什么内容？
  - 给我一版美业的内容周历
examples_en:
  - "Plan a week of private-domain content: Moments, group, 1v1"
  - "What should I post weekly in my private domain?"
  - "Give me a content calendar for the beauty industry"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 私域内容周历生成器

专治内容全靠灵感、想到啥发啥、一周发满 7 天广告。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/weekly_calc.py week --industry 行业 --channels 朋友圈,社群,1v1`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「内容周历」）。
