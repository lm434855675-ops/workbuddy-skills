---
name: moli-followup-sop
display_name: 客户跟进SOP生成器
display_name_en: Moli Customer Follow-up SOP Generator
description: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——成交八成靠跟进，丢单八成死在没跟。这套跟进体系从高客单 1v1 私域打法蒸馏（留学/移民/房产级长周期成交），精简免费试用版上传，专治顾客跟进三大死法：跟两次没反应就放弃、跟进就是问「考虑得怎么样」、全凭记忆没有节奏。三个计算器把跟进算清楚——顾客分级→分级跟进节奏（频率/渠道/内容）→逾期预警，每项过校验才交付，产出能直接照着执行的跟进排期表。触发词：顾客跟进、跟进SOP、顾客分层跟进、丢单挽回、销售跟进、私域跟进、顾客维护、跟进频率。"
description_zh: "李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——成交八成靠跟进，丢单八成死在没跟。这套跟进体系从高客单 1v1 私域打法蒸馏（留学/移民/房产级长周期成交），精简免费试用版上传，专治顾客跟进三大死法：跟两次没反应就放弃、跟进就是问「考虑得怎么样」、全凭记忆没有节奏。三个计算器把跟进算清楚——顾客分级→分级跟进节奏（频率/渠道/内容）→逾期预警，每项过校验才交付，产出能直接照着执行的跟进排期表。触发词：顾客跟进、跟进SOP、顾客分层跟进、丢单挽回、销售跟进、私域跟进、顾客维护、跟进频率。"
description_en: "MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative revenue - most deals close through follow-up, and most are lost by not following up. A distilled free-trial edition of the high-ticket 1v1 follow-up system. Fixes the three deadly sins: giving up after two touches, follow-ups that only ask have you decided, and rhythm kept by memory. Three calculators - lead grading, per-tier cadence, overdue alerts - validated before shipping an executable follow-up schedule."
examples_zh:
  - 我有 200 个咨询过没成交的顾客，帮我做一套分级跟进排期
  - 高客单顾客跟两次就没话说了，帮我设计跟进内容节奏
  - 帮我出一份跟进逾期预警规则，别再凭记忆跟顾客
examples_en:
  - "I have 200 consulted-but-not-closed leads - build me a graded follow-up schedule"
  - "High-ticket clients go silent after two touches - design the content cadence"
  - "Set up overdue alert rules so follow-up never relies on memory"
category: 商业咨询
version: 1.0.0
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——成交八成靠跟进。

# 客户跟进SOP生成器

帮你把「跟两次就放弃、跟进就是催单」变成**按客户分级、有节奏有内容的跟进排期**：谁跟、隔几天、走什么渠道、发什么、发了算数。

## 第一步：信息收集

| 字段 | 必填 |
|---|---|
| 客户量 + 成交周期（几天/几周/几个月） | 必填 |
| 客户来源与当前状态（咨询过/报价过/到过店） | 必填 |
| 载体（企微/个人微/电话） | 必填 |
| 上次流失原因复盘 | 选填 |

## 第二步：客户分级（跑 grade）

```
python3 scripts/followup_calc.py grade --file leads.json
```

输入 JSON 数组（lead/heat 0-100/last_touch_days/status）。按热度分 A/B/C 三级，输出每级的跟进节奏 + 逾期名单。

## 第三步：渲染交付

spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 跟进SOP.html`

## 硬规则

1. **连续跟进必须有内容变化**——同一句「考虑得怎么样」连发两次就是骚扰
2. **A 级 3 天一跟、B 级 7 天、C 级 14 天**，逾期当天预警
3. **每次跟进必须带价值**（案例/资料/优惠/行业信息），纯催单不计入跟进次数
4. C 级客户满 3 轮无反应转入沉默池，等大促批量唤醒

## 反模式

- ❌ 只跟进热客户——冷客户是下个月的热客户
- ❌ 跟进=问进度——每次都要给客户一个「回你」的理由
- ❌ 凭记忆跟客户——排期表之外漏掉的 = 丢单

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：跟进内容素材库、丢单挽回专项 SOP、多载体触达自动化方案。需要完整版或**成交顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「跟进」）。
