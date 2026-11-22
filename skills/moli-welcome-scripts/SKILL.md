---
name: moli-welcome-scripts
display_name: 企微欢迎语与承接话术生成器
description: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治欢迎语只说「欢迎关注」、加完好友没人理、承接话术绕三圈。能力：欢迎语四要素校验（身份+钩子+行动+期限）+ 30 秒承接链路输出。每项过校验才交付。触发词：企微欢迎语、欢迎语、承接话术、加微话术、私域承接、新客承接。"
description_zh: "李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏，精简免费试用版上传，专治欢迎语只说「欢迎关注」、加完好友没人理、承接话术绕三圈。能力：欢迎语四要素校验（身份+钩子+行动+期限）+ 30 秒承接链路输出。每项过校验才交付。触发词：企微欢迎语、欢迎语、承接话术、加微话术、私域承接、新客承接。"
description_en: "MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A distilled free-trial edition: validates welcome messages against four elements (identity, hook, action, deadline) and outputs the 30-second follow-up chain, validated before delivery."
display_name_en: "Moli WeCom Welcome & Follow-up Script Generator"
category: 私域运营
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 帮我写一条烘焙店加微后的欢迎语
  - 欢迎语发了没人回，帮我改
  - 加完好友 30 秒内该发什么？
examples_en:
  - "Write the post-add welcome message for my bakery WeChat"
  - "My welcome message gets no replies - fix it"
  - "What should be sent within 30 seconds after adding a friend?"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。

# 企微欢迎语与承接话术生成器

专治欢迎语只说「欢迎关注」、加完好友没人理、承接话术绕三圈。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/welcome_calc.py check --file welcome.json`
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**私域顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「企微欢迎语」）。
