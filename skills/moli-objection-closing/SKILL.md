---
name: moli-objection-closing
display_name: 异议处理与逼单话术
display_name_en: Moli Objection Handling & Closing Scripts
description: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——异议处理不是辩赢顾客，是给顾客一个台阶往下走。这套逼单打法从招商一线蒸馏，精简免费试用版上传，专治异议处理三大死法：顾客说贵就慌着降价、逼单太早吓跑人、该逼不逼白白流失。三个计算器把临门一脚算清楚——异议分类应对（太贵/再想想/问家人/对比竞品）→逼单信号评分（该不该逼现在逼）→降价红线（让利换条件的闭环），每条过校验才交付。触发词：异议处理、逼单、顾客说贵、再想想、成交阻力、临门一脚、降价策略、逼单信号。"
description_zh: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——异议处理不是辩赢顾客，是给顾客一个台阶往下走。这套逼单打法从招商一线蒸馏，精简免费试用版上传，专治异议处理三大死法：顾客说贵就慌着降价、逼单太早吓跑人、该逼不逼白白流失。三个计算器把临门一脚算清楚——异议分类应对（太贵/再想想/问家人/对比竞品）→逼单信号评分（该不该逼现在逼）→降价红线（让利换条件的闭环），每条过校验才交付。触发词：异议处理、逼单、顾客说贵、再想想、成交阻力、临门一脚、降价策略、逼单信号。"
description_en: "MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative revenue - objection handling is not about winning the argument but giving the customer a graceful path forward. A distilled free-trial edition of first-line closing tactics. Fixes the three deadly sins: panicking into discounts, closing too early, and letting warm deals die. Three calculators - objection classification, closing-signal scoring, and discount redlines - validated before delivery."
examples_zh:
  - 顾客说太贵了，除了降价还有什么打法
  - 顾客说回去和家里人商量，然后就没影了，怎么逼单
  - 帮我判断这个顾客现在该不该逼单
examples_en:
  - "Customer says it is too expensive - what plays besides discounting"
  - "Client said they would consult family and went silent - how do I close"
  - "Help me judge whether this prospect is ready to be closed now"
category: 商业咨询
version: 1.0.0
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——异议处理是给台阶，逼单是看信号。

# 异议处理与逼单话术

帮你把「客户一犹豫就降价、一逼单就吓跑」变成**按信号出牌的临门一脚**：异议分类应对、逼单时机评分、降价换条件闭环。

## 第一步：异议分类应对

读 [references/01-objection-playbook.md](references/01-objection-playbook.md)。四大异议（太贵/再想想/问家人/对比竞品）每类一个应对框架——**先认同、再重框、后推进**，禁止一上来就降价。

## 第二步：逼单信号评分（跑 signal）

```
python3 scripts/closing_calc.py signal --file signals.json
```

输入 JSON 数组（lead/signals），signals 为该客户已出现的信号列表（问价/问交付/对比竞品/沉默天数/邀约到店）。输出信号强度分 + **该不该逼、怎么逼**。

## 第三步：降价红线（跑 discount）

```
python3 scripts/closing_calc.py discount --price 原价 --cost 成本 --discount-proposal 客户要的折扣 --swap-condition 换什么条件
```

**硬规则：降价必须换条件**（今天定/推荐 2 个同行/发买家秀），纯让利 = 教客户下次继续砍。

## 第四步：渲染交付

spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 异议逼单手册.html`

## 硬规则

1. **降价必须换条件**，无条件的让利直接打回
2. **信号分不足 60 不逼单**——逼太早吓跑人，先补价值
3. **异议应对先认同再重框**，辩赢客户=输掉成交

## 反模式

- ❌ 客户说贵立刻打折——他会知道你的价是虚的
- ❌ 客户一沉默就连环夺命 call——给 48 小时缓冲+一次价值型触达
- ❌ 把「再想想」当拒绝——「再想想」= 有没被回答的顾虑

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：全异议类型应对库、逼单信号自定义权重、团队逼单案例复盘模板。需要完整版或**成交顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「逼单」）。
