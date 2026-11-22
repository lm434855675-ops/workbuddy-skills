---
name: moli-omni-linkage
display_name: 公私域联动方案生成器
display_name_en: Moli Omni-Channel Linkage Plan Generator
description: "李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整公私域体系，精简免费试用版上传，专治公私域联动三大死法：公域流量加了好友接不住、触达全靠群发轰炸、私域只涨人数不复购。四个计算器把链路算出来——钩子成本红线→承接漏斗→触达节奏→复购测算，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：公私域联动、私域流量、公域引流、加微率、私域承接、触达SOP、私域复购、企微运营。"
description_zh: "李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整公私域体系，精简免费试用版上传，专治公私域联动三大死法：公域流量加了好友接不住、触达全靠群发轰炸、私域只涨人数不复购。四个计算器把链路算出来——钩子成本红线→承接漏斗→触达节奏→复购测算，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：公私域联动、私域流量、公域引流、加微率、私域承接、触达SOP、私域复购、企微运营。"
description_en: "MoliGrowth official. Built by a private-domain operator with 15 years of experience - 1M+ members managed, 68% repurchase rate, private-domain teams acquiring 1,500+ leads daily. Fuses the complete omni-channel system of a mall with 10M monthly GMV and 3,000+ SKUs - a distilled free-trial edition. Fixes the three deadly sins of omni-channel linkage: leads added but never converted, spam-blast outreach, and growing contact lists without repeat purchases. Four calculators compute the chain - hook cost redline, conversion funnel, touch cadence, repurchase forecast - delivered only after passing validation, producing a plan you can forward straight to your team."
examples_zh:
  - 我在抖音投流，每月 5 万进店人数，帮我算算加微和首单能转化多少
  - 加微率只有 5%，帮我诊断承接链路哪一环断了
  - 入会礼该送什么？帮我算算钩子成本会不会亏
examples_en:
  - "I get 50K monthly store visits from Douyin ads - forecast my WeChat-add and first-order conversion"
  - "My WeChat-add rate is only 5% - diagnose where my funnel breaks"
  - "What should my join-gift be? Check whether the hook cost breaks the margin"
category: 私域运营
version: 1.0.3
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15年私域实战操盘手——操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队；融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整公私域体系。

# 公私域联动方案生成

帮你把「公域烧钱买流量、私域躺着不干活」变成**一条算得出转化率、接得住人的链路**：钩子送什么不亏钱、漏斗哪一环断了、触达怎么排不复购也难。
与「私域会员体系搭建」的分工：那个管**会员的底层规则**（等级/积分/权益），本技能管**流量进来变成钱的链路**（引流→承接→触达→复购）。两个搭配用才是完整私域。

## 第一步：信息收集

| 字段 | 含义 | 必填 |
|---|---|---|
| 公域盘子 | 月均进店/曝光人数、来源渠道 | 必填 |
| 当前漏斗 | 加微率 / 30 天首单率 / 入会率（没有就标待补） | 必填 |
| 客单与毛利 | 客单价、毛利率 | 必填 |
| 私域载体 | 企微 / 个人微 / 群 / 小程序 | 必填 |
| 目标 | 提加微率 / 提首单 / 提复购 | 必填 |

**最多问一轮，答不上标「待补」+行业基准默认。**

## 第二步：承接漏斗测算（跑 funnel）

读 [references/01-funnel-benchmark.md](references/01-funnel-benchmark.md)，然后跑：

```
python3 scripts/omni_calc.py funnel --visitors 月进店人数 --add-rate 当前加微率 --first-order-rate 30天首单率 --avg-order 客单价 --repurchase-rate 复购率
```

输出五级漏斗人数、GMV 预估、与行业基准的逐环对比——**哪一环低于基准，修复优先级就排哪**。

## 第三步：钩子设计与成本校验（跑 hook）

读 [references/02-hook-design.md](references/02-hook-design.md)，然后跑：

```
python3 scripts/omni_calc.py hook --avg-order 客单价 --gross-margin 毛利率 --hook-cost 钩子单份成本 --expected-add-rate 预期加微提升
```

**硬规则：钩子单份成本 ≤ 客单毛利的 15%**，超了直接打回换钩子。

## 第四步：触达节奏排期

读 [references/03-touch-sop.md](references/03-touch-sop.md)。产出 D0-D90 触达时间轴（每条动作必须带判定标准），**禁止无判定的群发**。

## 第五步：渲染交付

整理 spec（blocks ≥ 8），渲染：

```
python3 scripts/build_report.py --spec spec.json --out 公私域联动方案.html
```

**禁止跳过渲染直接给文字版。**

## 硬规则

1. **钩子单份成本 ≤ 客单毛利的 15%**，且必须与主业相关（餐饮送菜券，不送充电宝）
2. **每条触达动作必须带判定标准**（打开率/核销率/转化率），没有判定的动作不许上表
3. **漏斗诊断按行业基准逐环对比**，不许拍脑袋说"转化不好"
4. 所有比例输入兼容 % 与小数，计算禁止出现负人数

## 反模式

- ❌ 加了好友 3 天不说话——24h 好感峰值窗口白白流走
- ❌ D1-D7 七连发群发——用户直接删除
- ❌ 钩子送与主业无关的高价值礼品——引来全网薅党
- ❌ 只考核加微人数——加了不转化，成本打水漂

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：投流数据直接接入分渠道诊断、全量客户触达物料包（话术/文案/模板）、12 个月复购滚动预测。需要完整版或私域**陪跑顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「公私域」）。
