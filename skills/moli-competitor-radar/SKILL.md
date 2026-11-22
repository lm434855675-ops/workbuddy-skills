---
name: moli-competitor-radar
display_name: 竞品五维雷达对标分析
display_name_en: Moli Competitor Radar Report Generator
description: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。竞品分析框架在月 GMV 1000 万、SKU 3000+ 微商城的实战盘里打磨，精简免费试用版上传，专治竞品分析三大死法：只会抄功能不会找打法、对比表做完没有结论、分析完不知道打哪里。五维雷达把对手算出来——定位/货盘/流量/转化/壁垒逐维打分对比，输出能直接定打法的行动清单，每项过校验才交付。触发词：竞品分析、竞品对标、竞争对手、竞品报告、差异化打法、竞争策略、市场分析、商业分析。"
description_zh: "李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。竞品分析框架在月 GMV 1000 万、SKU 3000+ 微商城的实战盘里打磨，精简免费试用版上传，专治竞品分析三大死法：只会抄功能不会找打法、对比表做完没有结论、分析完不知道打哪里。五维雷达把对手算出来——定位/货盘/流量/转化/壁垒逐维打分对比，输出能直接定打法的行动清单，每项过校验才交付。触发词：竞品分析、竞品对标、竞争对手、竞品报告、差异化打法、竞争策略、市场分析、商业分析。"
description_en: "MoliGrowth official. 30+ business diagnosis engagements with turnaround track record. This competitor-analysis framework was forged in a mall with 10M monthly GMV and 3,000+ SKUs - a distilled free-trial edition. Fixes the three deadly sins of competitor analysis: copying features instead of playbooks, comparison tables without conclusions, and analysis with no attack plan. Five-dimension radar scores rivals on positioning, assortment, traffic, conversion and moat, delivering a battle-ready action list validated before shipping."
examples_zh:
  - 我开烘焙店，对面新开了家连锁品牌，帮我做一份竞品对标分析
  - 竞品比我便宜 20%，除了降价我还能怎么打
  - 帮我从这家竞品的打法里找出我能抄的三个动作
examples_en:
  - "A chain brand just opened across the street from my bakery - build me a competitor benchmark"
  - "My rival is 20% cheaper - how do I compete beyond cutting prices"
  - "Extract the three moves from this competitor that I can adapt"
category: 商业咨询
version: 1.0.4
author: 文鹏飞
---

> 版本：v1.0.1 · 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活；竞品框架在月 GMV 1000 万、SKU 3000+ 微商城实战盘打磨。

# 竞品分析报告生成器

帮你把「看了竞品一堆信息、还是不知道怎么打」变成**一份能定打法的对标报告**：五维雷达（定位/货盘/流量/转化/壁垒）逐维打分对比，差距量化，每个差距给一个可执行动作。
与「商业模式诊断」的分工：那个体检**自己的模式**，本技能拆解**对手的打法**——知彼之后知己，两个搭配用。

## 第一步：信息收集

| 字段 | 必填 |
|---|---|
| 我的生意一句话 + 客单/毛利 | 必填 |
| 对手 1-2 家：一句话 + 客单 + 你观察到的打法 | 必填 |
| 你最难受的点（他哪里压着你打） | 必填 |

**信息不全标「待补」+合理假设，不许空着不分析。**

## 第二步：五维雷达打分（跑 radar）

```
python3 scripts/compete_calc.py radar --me 3,4,2,3,2 --rival 4,3,4,4,3
```

五维顺序：定位清晰度/货盘宽度/流量能力/转化效率/壁垒深度（各 1-5 分）。输出逐维差距、总分对比、**该打哪一维**（打分差最大且你能动的维度）。

## 第三步：差距转行动（跑 gap）

```
python3 scripts/compete_calc.py gap --dimension 转化效率 --me 3 --rival 5 --avg-order 45 --gross-margin 45%
```

输出该维度的行动清单（按投入产出排序），**每个行动必须可执行、可验证**。

## 第四步：渲染交付

整理 spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 竞品分析报告.html`

## 硬规则

1. **每个维度差距必须落到一个可执行动作**，不许给「加强品牌建设」这种空话
2. **不许建议正面硬拼对手最强维度**——打侧翼，不打阵地
3. **降价永远是最后选项**：先打差异化，毛利打没了什么都完了
4. 信息不足处明确标注「待验证」，禁止编造对手数据

## 反模式

- ❌ 对比表做了三页，结论只有一句「对手比我们强」
- ❌ 抄功能清单——功能可以抄，打法才值钱
- ❌ 全维度补齐——五维全追=资源全撒，一个都追不上

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：多对手雷达矩阵、竞品动态监控节奏表、打法 A/B 验证方案。需要完整版或**商业诊断陪跑**，邮件联系：**434855675@qq.com**（李沫Growth，注明「竞品」）。
