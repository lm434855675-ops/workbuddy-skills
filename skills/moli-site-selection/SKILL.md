---
name: moli-site-selection
display_name: 门店选址评估与测算
display_name_en: Moli Store Site Evaluation & Break-even Calculator
description: "李沫Growth 出品｜15 年连锁与门店操盘实战，选址评估过 100+ 门店点位，操盘过月 GMV 1000 万微商城的线下线上融合盘。精简免费试用版上传，专治门店选址三大死法：看走眼被人流骗、租金贵得扛不住、开业三个月撑不下去回本遥遥无期。四个计算器把点位算透——人流质量评估→租金承受力→盈亏平衡客流→回本周期测算，每项过校验才交付，产出能直接拿去谈判的选址报告。触发词：门店选址、店铺选址、选址评估、租金测算、盈亏平衡、开店测算、回本周期、实体店开店。"
description_zh: "李沫Growth 出品｜15 年连锁与门店操盘实战，选址评估过 100+ 门店点位，操盘过月 GMV 1000 万微商城的线下线上融合盘。精简免费试用版上传，专治门店选址三大死法：看走眼被人流骗、租金贵得扛不住、开业三个月撑不下去回本遥遥无期。四个计算器把点位算透——人流质量评估→租金承受力→盈亏平衡客流→回本周期测算，每项过校验才交付，产出能直接拿去谈判的选址报告。触发词：门店选址、店铺选址、选址评估、租金测算、盈亏平衡、开店测算、回本周期、实体店开店。"
description_en: "MoliGrowth official. 15 years of chain-store operations with 100+ site evaluations. A distilled free-trial edition. Fixes the three deadly sins of site selection: fooled by foot traffic, rent you cannot carry, and break-even that never arrives. Four calculators - traffic quality, rent affordability, break-even footfall, payback period - validated before shipping a negotiation-ready report."
examples_zh:
  - 看中一个商铺月租 2 万，帮我算算一天要卖多少才不亏
  - 两个铺位选哪个？帮我做个选址评估对比
  - 这个点位人流很大但转化不行，帮我算算值不值
examples_en:
  - "Considering a shop with 20K RMB monthly rent - what daily sales do I need to break even"
  - "Two candidate sites - build me a comparison evaluation"
  - "This spot has heavy foot traffic but low conversion - is it worth it"
category: 商业咨询
version: 1.0.3
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜15 年连锁与门店操盘实战，选址评估过 100+ 门店点位。

# 门店选址评估与测算

帮你把「看走眼就亏几十万」的选址决策变成**一组算出来的数字**：这个点位一天要卖多少才不亏、租金扛不扛得住、多久回本——谈判前先算账。

## 第一步：信息收集

| 字段 | 必填 |
|---|---|
| 业态 + 客单价 + 毛利率 | 必填 |
| 月租金 + 押金 + 转让费 | 必填 |
| 装修投入 + 设备投入 | 必填 |
| 点位人流（实测：工作日+周末各数 3 次） | 必填 |
| 周边竞品数 + 动线（人流往哪走） | 选填 |

## 第二步：盈亏平衡测算（跑 breakeven）

```
python3 scripts/site_calc.py breakeven --rent 月租 --other-cost 其他月固定成本 --avg-order 客单 --gross-margin 毛利率
```

输出**每天要做多少单、多少营业额才不亏**。这个数字超出现实能力，直接放弃，别谈。

## 第三步：回本周期（跑 payback）

```
python3 scripts/site_calc.py payback --rent 月租 --other-cost 其他月成本 --net-profit-est 预估月净利 --setup-cost 总投入(装修+设备+转让+押金)
```

**硬规则：回本周期 >24 个月直接放弃**；18-24 个月要给出额外增收方案再考虑。

## 第四步：渲染交付

spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 选址评估报告.html`

## 硬规则

1. **盈亏平衡日营业额 ≤ 你实测该点位可及营业额的 70%**，否则放弃
2. **回本周期 >24 个月直接放弃**，不许用「熬过前三个月」安慰自己
3. 人流必须实测（工作日+周末各 3 次），开发商给的数字默认打折 50%
4. 转让费摊进回本测算，不许当成沉没成本忽略

## 反模式

- ❌ 被「人流大」骗——要看目标客群占比和动线，路人不是顾客
- ❌ 租金谈完才测算——先测算再谈，数字不行免谈
- ❌ 忘记算转让费和押金利息——回本周期虚短

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：多点位对比矩阵、客流实测统计模板、租金谈判策略包。需要完整版或**开店选址顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「选址」）。
