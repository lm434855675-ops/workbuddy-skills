---
name: moli-bp-generator
display_name: 商业计划书十段生成器
display_name_en: "Moli 商业计划书生成器"
description: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 激停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版上传，专治BP写成产品说明书、财务预测拍脑袋、融资额度无依据。能力：BP 十段框架完整性校验（摘要/痛点/方案/市场/模式/竞争/团队/财务/规划/融资）+ 逐段打回重写。每项过校验才交付。触发词：商业计划书、BP、融资计划、路演PPT、商业方案、创业计划、项目计划书、融资BP。"
description_zh: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 激停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版上传，专治BP写成产品说明书、财务预测拍脑袋、融资额度无依据。能力：BP 十段框架完整性校验（摘要/痛点/方案/市场/模式/竞争/团队/财务/规划/融资）+ 逐段打回重写。每项过校验才交付。触发词：商业计划书、BP、融资计划、路演PPT、商业方案、创业计划、项目计划书、融资BP。"
description_en: "MoliGrowth official. 乙方商业咨询 5 年服务企业 100+——BP 不是产品说明书，是给投资人看的风险收益账。 A distilled free-trial edition, validated before delivery."
category: 商业咨询
version: 1.0.1
author: 文鹏飞
examples_zh:
  - 我们是做农产品供应链的创业团队，帮我搭一份 BP 框架
  - BP 的财务预测部分总被投资人挑战，帮我重做
  - 帮我检查这份 BP 缺了哪些关键模块
examples_en:
  - "We are an agri-supply-chain startup - help me structure a BP"
  - "Investors keep challenging our financials - redo that section"
  - "Review my BP and list the missing key modules"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 激停项目重新定位陪跑至复活。

# 商业计划书生成器

专治BP写成产品说明书、财务预测拍脑袋、融资额度无依据。

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

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「商业计划书」）。
