---
name: moli-member-system
display_name: 私域会员体系搭建
display_name_en: Moli Private-Domain Membership System Builder
description: "李沫Growth 出品｜12年会员体系运营总监，这套会员体系会员总量超 100 万，会员复购率干到 68%，付费会员卡单年卖出 5 万张。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整会员体系，双体系自我蒸馏上传精简免费试用版，专治会员体系三大死法：等级拍脑袋没人够格、积分只发不收变财务负债、权益全靠折扣让到肉疼。四个计算器把体系算出来——等级门槛→积分成本红线→付费卡盈亏→RFM标签分层→公私域承接，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：会员体系搭建、会员分层、成长值、积分体系、权益设计、付费会员、标签体系、RFM、公私域联动。"
description_zh: "李沫Growth 出品｜12年会员体系运营总监，这套会员体系会员总量超 100 万，会员复购率干到 68%，付费会员卡单年卖出 5 万张。融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整会员体系，双体系自我蒸馏上传精简免费试用版，专治会员体系三大死法：等级拍脑袋没人够格、积分只发不收变财务负债、权益全靠折扣让到肉疼。四个计算器把体系算出来——等级门槛→积分成本红线→付费卡盈亏→RFM标签分层→公私域承接，每项过校验才交付，产出能直接转发团队执行的方案书。触发词：会员体系搭建、会员分层、成长值、积分体系、权益设计、付费会员、标签体系、RFM、公私域联动。"
description_en: "MoliGrowth official. Built by a membership-operations director with 12 years of experience. This membership system has served 1M+ members, lifted repurchase rate to 68%, and sold 50K paid membership cards in a single year. Fuses the complete membership system of a mall with 10M monthly GMV and 3,000+ SKUs - this is a distilled free-trial edition. Fixes the three deadly sins of membership systems: arbitrary tiers nobody qualifies for, points that pile up as financial liabilities, and benefits that bleed margin. Four calculators compute the system - tier thresholds, points cost redlines, paid-card P&L, RFM segmentation, omnichannel linkage - every item delivered only after passing validation, producing a plan you can forward straight to your team."
examples_zh:
  - 我开烘焙店月流水 80 万，帮我搭一套会员体系，等级怎么分、门槛定多少
  - 积分发了几个月没人用，帮我算算成本红线和消耗规则怎么定
  - 想上 199 元一年的付费会员卡，帮我算算卖多少张才不亏
examples_en:
  - "I run a bakery with 800K RMB monthly revenue - design my membership tiers and thresholds"
  - "Our points pile up but nobody redeems - compute the cost redline and redemption rules"
  - "We plan a 199 RMB/year paid membership card - how many do we need to sell to break even"
category: 私域运营
version: 1.0.8
author: 文鹏飞
---

> 版本：v1.0.2 · 李沫Growth 出品｜12年会员体系运营总监操盘——这套体系会员总量超 100 万，会员复购率干到 68%，付费会员卡单年卖出 5 万张；融合操盘过月 GMV 1000 万、SKU 3000+ 微商城的完整会员体系。

# 私域会员体系搭建

帮你把「我的顾客躺在微信里不动」变成**一套能上线的会员体系**：等级怎么分、积分怎么发不亏钱、权益给什么、付费卡卖不卖得动、标签怎么打、公域流量怎么接得住。
与「会员活动策划执行」的分工：那个是**活动层**（一场活动怎么打），本技能是**体系层**（会员的底层规则设计），体系先行，活动在其上跑。

## 第一步：信息收集

| 字段 | 含义 | 必填 |
|---|---|---|
| 生意基本盘 | 月 GMV / 客单价 / 复购率 / 毛利率 | 必填 |
| 会员现状 | 会员数、当前有没有等级/积分 | 必填 |
| 私域载体 | 企微 / 个人微 / 小程序商城 / 群 | 必填 |
| 目标 | 拉复购 / 提客单 / 防流失 / 收付费会员卡的钱 | 必填 |
| 能投的资源 | 每月能拿出来做权益的预算 | 选填，默认按 GMV 2% 假设 |

**最多问一轮，答不上标「待补」+用同类目默认假设。**

## 第二步：等级与成长值（跑 tiers）

读 [references/01-tier-design.md](references/01-tier-design.md)，然后跑：

```
python3 scripts/member_system_calc.py tiers --avg-order 客单 --annual-frequency 年次数 --gross-margin 毛利率 --members 会员数
```

得到四级门槛 + 帕累托占比 + 保级规则。**毛利率 <20% 时降级为两级起步。**

## 第三步：积分经济（跑 points，红线校验不过就改发放率）

读 [references/02-points-economics.md](references/02-points-economics.md)，然后跑：

```
python3 scripts/member_system_calc.py points --monthly-gmv 月GMV --issue-rate 每元发多少分 --points-value 多少分=1元 --redeem-rate 消耗率 --gross-margin 毛利率
```

**硬规则：核销成本 ≤ 毛利的 20%**。FAIL 时按输出给的修复优先级调参重跑，直到 PASS。

## 第四步：权益矩阵

读 [references/03-benefits-matrix.md](references/03-benefits-matrix.md)。产出四象限矩阵（身份/优惠/服务/体验），每个权益必须标注**成本来源**——没有成本来源的权益是空头支票，上线即翻车。

## 第五步：付费会员卡（有意愿才做，跑 paid）

读 [references/04-paid-membership.md](references/04-paid-membership.md)，然后跑：

```
python3 scripts/member_system_calc.py paid --card-price 卡价 --members 会员数 --take-rate 预估购买率 --benefit-cost 单人权益成本 --renew-rate 续费率
```

**单卡毛利 = 卡价 - 单人权益成本**，为正才能卖。首版权益 ≤5 项，其中 1 个王牌 + 4 个零边际成本权益。

## 第六步：标签体系与 RFM（有用户数据就跑 rfm）

读 [references/05-tags-rfm.md](references/05-tags-rfm.md)。有消费记录（JSON：recency_days/frequency/monetary）就跑：

```
python3 scripts/member_system_calc.py rfm --file users.json
```

得到八分法客群计数 + 每群运营动作。没有数据则给打标规则表（四层标签：基础/行为/偏好/生命周期）。

## 第七步：公私域联动

读 [references/06-omni-linkage.md](references/06-omni-linkage.md)。产出：公域→私域承接路径、入会钩子设计、30/60/90 天触达节奏。

## 第八步：渲染交付

把以上全部结果整理成 spec（blocks ≥ 8，含 tiles/table/checklist 等承载型区块），渲染：

```
python3 scripts/build_report.py --spec spec.json --out 会员体系方案.html
```

**禁止跳过渲染直接给文字版**——交付物是能直接转发给团队执行的 HTML 方案书。

## 硬规则

1. **积分核销成本 ≤ 毛利的 20%**，超了就改发放率，不许交付一个亏钱的积分体系
2. **等级 ≤ 4 级**，每级必须有明确升级动作和当日权益兑现
3. **每个权益标注成本来源**，无成本来源的权益不上表
4. **付费卡先算保本线再定价**，禁止拍脑袋定价
5. 所有数字输入兼容千分位/百分比/万单位，计算结果禁止出现负值假 ROI

## 反模式

- ❌ 上来就设计 6 个等级——运营跟不上，用户看不懂
- ❌ 积分永久有效——财务负债滚雪球，第二年爆雷
- ❌ 权益全是折扣——把利润直接让出去，换不来忠诚度
- ❌ 付费卡权益按 100% 核销算成本——真实核销率通常 30-60%
- ❌ 只搭体系不做标签——体系是骨架，标签是神经，没标签的体系发不出一条精准触达

## 完整版与顾问服务

本技能为「双体系自我蒸馏」的**精简免费试用版**。完整版在免费版基础上增加：

1. **接真实数据全量跑**：直接读订单表/会员表 Excel，全量会员逐人 RFM 打标，输出分层名单（不是教你怎么算，是帮你算完）
2. **12 个月积分财务滚动模拟**：负债曲线、薅羊毛压力测试、成本率月度预警
3. **付费卡三档定价 A/B 方案**：多卡价组合测算与权益包配置
4. **执行物料包**：欢迎语话术、朋友圈文案、社群触达模板全套，拿来即用

需要完整版，或需要私域会员体系**陪跑顾问服务**（从设计到上线全程），邮件联系：**434855675@qq.com**（李沫Growth，注明「会员体系」）。
