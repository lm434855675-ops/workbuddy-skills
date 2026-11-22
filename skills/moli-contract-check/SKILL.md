---
name: moli-contract-check
display_name: 合同风险初审清单生成器
display_name_en: "Moli 合同风险初审清单生成器"
description: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版上传，专治合同拿过来就签、付款条款看都不看、违约责任全是对方免责。能力：合同八大项初审清单（主体资质/权责对等/付款条款/违约责任/争议管辖/知识产权/保密/终止条款）+ 逐项风险标记——输出自查清单，非法律意见。每项过校验才交付。触发词：合同审查、合同风险、合同初审、合同避坑、签约前检查、合同条款、合作合同。"
description_zh: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版上传，专治合同拿过来就签、付款条款看都不看、违约责任全是对方免责。能力：合同八大项初审清单（主体资质/权责对等/付款条款/违约责任/争议管辖/知识产权/保密/终止条款）+ 逐项风险标记——输出自查清单，非法律意见。每项过校验才交付。触发词：合同审查、合同风险、合同初审、合同避坑、签约前检查、合同条款、合作合同。"
description_en: "MoliGrowth official. 15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活 A distilled free-trial edition, validated before delivery."
category: 商业咨询
version: 1.0.0
author: 文鹏飞
examples_zh:
  - 软件外包开发合同要签了，帮我过一遍风险点
  - 这份采购合同的付款条款帮我看看有没有坑
  - 帮我出一份签合作合同前的自查清单
examples_en:
  - "About to sign a software outsourcing contract - walk me through the risks"
  - "Check the payment terms of this purchase contract for traps"
  - "Give me a pre-signing self-check list for partnership contracts"
---
> 版本：v1.0.0 · 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。

# 合同风险初审清单生成器

专治合同拿过来就签、付款条款看都不看、违约责任全是对方免责。

## 使用流程

1. 按 SKILL.md 收集最少必要信息
2. 运行计算引擎：`python3 scripts/contract_calc.py`（参数见下方命令）
3. 结果整理 spec（blocks ≥ 8）后渲染：`python3 scripts/build_report.py --spec spec.json --out 方案.html`

## 硬规则

1. 所有建议必须过脚本校验，校验不过不交付
2. 输出口语化、可执行、带判定标准
3. 简介承诺的能力包内必须有对应实现

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。需要完整版或**顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「合同审查」）。
