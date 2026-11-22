---
name: moli-channel-policy
display_name: 渠道政策设计测算器
display_name_en: "Moli 渠道政策设计测算器"
description: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治分销折扣一拍脑袋渠道没动力、返点层级乱成一锅粥、区域保护没写清打架。能力：分销渠道政策测算（拿货折扣/返点阶梯/任务线）→ 渠道毛利空间校验（渠道有钱赚）+ 公司毛利红线（公司有钱赚）双向校验。每项过校验才交付。触发词：渠道政策、分销政策、代理政策、拿货折扣、返点设计、渠道毛利、经销商政策、分销体系。"
description_zh: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治分销折扣一拍脑袋渠道没动力、返点层级乱成一锅粥、区域保护没写清打架。能力：分销渠道政策测算（拿货折扣/返点阶梯/任务线）→ 渠道毛利空间校验（渠道有钱赚）+ 公司毛利红线（公司有钱赚）双向校验。每项过校验才交付。触发词：渠道政策、分销政策、代理政策、拿货折扣、返点设计、渠道毛利、经销商政策、分销体系。"
description_en: "MoliGrowth official. 15 年招商与私域操盘，累计招商回款 10 亿+ A distilled free-trial edition, validated before delivery."
category: 商业咨询
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 小家电做区域分销，帮我测算拿货折扣和返点怎么设
  - 给代理商的政策总没吸引力，帮我算渠道毛利空间
  - 微商城招分销代理，帮我设计分级政策
examples_en:
  - "Launching regional distribution for small appliances - help me set wholesale discounts and rebates"
  - "Our agent policy lacks appeal - calculate the channel margin space"
  - "Design tiered policies for our mall's distribution agents"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。

# 渠道政策设计测算器

专治分销折扣一拍脑袋渠道没动力、返点层级乱成一锅粥、区域保护没写清打架。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/channel_calc.py`（参数见下方命令）
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「渠道政策」）。
