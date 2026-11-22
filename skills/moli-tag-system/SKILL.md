---
name: moli-tag-system
display_name: 私域标签体系搭建与分层运营
display_name_en: Moli Private-Domain Tag System Builder
description: "李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整标签体系，精简免费试用版上传，专治私域标签三大死法：标签打了一堆没人用、分层全靠拍脑袋、触达不分人发什么烂什么。四个计算器把体系算出来——四层标签架构→RFM八分法→分层名单导出→客群运营动作匹配，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：私域标签、标签体系、RFM 分层、用户分层、顾客分层、精准触达、用户画像、私域运营、会员分层。"
description_zh: "李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整标签体系，精简免费试用版上传，专治私域标签三大死法：标签打了一堆没人用、分层全靠拍脑袋、触达不分人发什么烂什么。四个计算器把体系算出来——四层标签架构→RFM八分法→分层名单导出→客群运营动作匹配，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：私域标签、标签体系、RFM 分层、用户分层、顾客分层、精准触达、用户画像、私域运营、会员分层。"
description_en: "MoliGrowth official. Built by a private-domain operator with 15 years of experience - 1M+ members managed, 68% repurchase rate, teams acquiring 1,500+ leads daily. Fuses the complete tag system of a mall with 10M monthly GMV and 3,000+ SKUs - a distilled free-trial edition. Fixes the three deadly sins of private-domain tagging: tags nobody uses, gut-feel segmentation, and one-size-fits-all blasts. Four calculators compute the system - four-layer tag architecture, RFM octant segmentation, roster export, and segment-action matching - delivered only after passing validation, producing a plan you can forward straight to your team."
examples_zh:
  - 我有 3 万会员的订单表，帮我按 RFM 分层，每类人给一套运营动作
  - 标签打了几十个但触达还是群发，帮我重新设计标签体系
  - 重要挽留客户越来越多，帮我出一份召回优先级方案
examples_en:
  - "Here is my order sheet for 30K members - segment them by RFM with an action plan per group"
  - "We have dozens of tags but still blast everyone - redesign the tag architecture"
  - "At-risk members keep growing - build me a win-back priority plan"
category: 私域运营
version: 1.0.3
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15年私域实战操盘手——操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队；融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整标签体系。

# 私域标签体系搭建

帮你把「标签打了几十个、触达还是一锅端」变成**一套人人有标签、标签有用途、触达分人发**的体系：四层标签架构、RFM 八分法、可直接执行的分层名单。
与「私域会员体系搭建」的分工：那个管**等级与权益规则**，本技能管**「谁是谁、该发什么」**——标签是体系的神经，没标签的会员体系发不出一条精准触达。

## 第一步：信息收集

| 字段 | 含义 | 必填 |
|---|---|---|
| 会员盘子 | 会员总量、数据在哪（表格/系统） | 必填 |
| 现有标签 | 打了哪些标签、哪些在用 | 选填 |
| 触发现状 | 现在怎么发（群发/分层/1v1） | 必填 |
| 目标 | 精准触达 / 召回 / 提复购 | 必填 |

## 第二步：四层标签架构

读 [references/01-tag-architecture.md](references/01-tag-architecture.md)。原则：**每个标签必须对应一个触达动作**，没有动作的标签不打——打标和维护都有成本。

## 第三步：RFM 八分法（有订单数据就跑）

读 [references/02-rfm-playbook.md](references/02-rfm-playbook.md)，然后跑：

```
python3 scripts/tag_calc.py rfm --file 订单表.json [--out 分层名单.csv]
```

输入 JSON 数组（user/recency_days/frequency/monetary，兼容千分位与万单位）。输出八类客群计数 + 每类运营动作 + **可直接执行的分层名单 CSV**（按客群和金额排序）。

**资源分配铁律**：重要挽留 + 流失 >40% 时，本月全部资源投召回，不投拉新。

## 第四步：渲染交付

整理 spec（blocks ≥ 8），渲染：

```
python3 scripts/build_report.py --spec spec.json --out 标签体系方案.html
```

**禁止跳过渲染直接给文字版。**

## 硬规则

1. **每个标签必须绑定触达动作**（谁用/什么时候用/发什么），无动作的标签不上表
2. **R/F/M 按中位数切分**，不用均值（抗异常值）
3. **分层名单每周重跑**，客群迁移必须盯（价值客户跌入挽留 = 流失预警）
4. 第一版只打「会被用的」标签：RFM 三项 + 渠道来源 + 品类偏好，够了

## 反模式

- ❌ 一次打 50 个标签——维护不动，半年后全是过期数据
- ❌ 用均值切分层——一个万元大单把均值拉爆，分层全失真
- ❌ 标签永不更新——拿三年前的「价格敏感」标签发券，发谁谁烦
- ❌ 分层做完不导名单——方案在 PPT 里，触达还是一锅端

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：多表数据自动清洗合并、标签自动化规则引擎、12 个月客群迁移追踪看板。需要完整版或私域**陪跑顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「标签体系」）。
