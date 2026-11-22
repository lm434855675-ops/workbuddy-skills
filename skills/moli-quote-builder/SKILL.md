---
name: moli-quote-builder
display_name: 报价方案生成器
display_name_en: "Moli 报价方案生成器"
description: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治报价拍脑袋毛利算不清、一份报价打天下、低价中标亏本干。能力：三档报价单（基础/标准/旗舰锚定）+ 各档毛利率校验 + 锚定逻辑（三档同框顾客多选中间档）。每项过校验才交付。触发词：报价方案、报价单、报价策略、三档报价、怎么报价、价格锚定、报价模板、项目报价。"
description_zh: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治报价拍脑袋毛利算不清、一份报价打天下、低价中标亏本干。能力：三档报价单（基础/标准/旗舰锚定）+ 各档毛利率校验 + 锚定逻辑（三档同框顾客多选中间档）。每项过校验才交付。触发词：报价方案、报价单、报价策略、三档报价、怎么报价、价格锚定、报价模板、项目报价。"
description_en: "MoliGrowth official. 15 年招商与私域操盘，累计招商回款 10 亿+——报价是价值锚点不是成本加成。 A distilled free-trial edition, validated before delivery."
category: 商业咨询
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 我们是做办公家具的，帮我做一份三档报价单
  - 给企业做网站开发怎么报价？帮我算各档毛利
  - 报价单总被砍价，帮我重新设计报价结构
examples_en:
  - "We sell office furniture - build a three-tier quotation"
  - "How should a web dev agency price projects? Check my margins"
  - "My quotes always get bargained down - redesign the structure"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。

# 报价方案生成器

专治报价拍脑袋毛利算不清、一份报价打天下、低价中标亏本干。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：见 scripts/（命令见下）
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「报价方案」）。
