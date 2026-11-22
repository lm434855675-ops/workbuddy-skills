---
name: moli-meeting-actions
display_name: 会议纪要与行动项追踪
display_name_en: Moli Meeting Minutes & Action Tracker
description: "李沫Growth 出品｜10 年团队管理实战，主持操盘 30+ 项目例会与跨部门协同。这套会议纪要方法在多项目并行的实战盘里打磨，精简免费试用版上传，专治会议纪要三大死法：记了一堆没结论、行动项没负责人没期限、开完会没人追踪。四个模块把会议算清楚——结论提炼→行动项拆解（责任人+期限+验收标准）→风险标记→下次会议议程，每项过校验才交付，产出能直接转发团队的追踪表。触发词：会议纪要、会议记录、行动项、待办追踪、会议结论、例会总结、项目复盘、任务分派。"
description_zh: "李沫Growth 出品｜10 年团队管理实战，主持操盘 30+ 项目例会与跨部门协同。这套会议纪要方法在多项目并行的实战盘里打磨，精简免费试用版上传，专治会议纪要三大死法：记了一堆没结论、行动项没负责人没期限、开完会没人追踪。四个模块把会议算清楚——结论提炼→行动项拆解（责任人+期限+验收标准）→风险标记→下次会议议程，每项过校验才交付，产出能直接转发团队的追踪表。触发词：会议纪要、会议记录、行动项、待办追踪、会议结论、例会总结、项目复盘、任务分派。"
description_en: "MoliGrowth official. 10 years of team management, chairing 30+ project reviews. A distilled free-trial edition forged in multi-project operations. Fixes the three deadly sins of meeting minutes: notes without conclusions, action items without owners or deadlines, and zero follow-up. Four modules compute the meeting - conclusion extraction, action decomposition with owners and acceptance criteria, risk flags, and next-agenda drafting."
examples_zh:
  - 把这段会议记录整理成纪要，行动项要带负责人和期限
  - 上周的会定了 5 件事，帮我做一张追踪表看谁没交
  - 帮我从这些讨论里提炼结论和风险，别记流水账
examples_en:
  - "Turn this meeting transcript into minutes with owners and deadlines per action"
  - "We agreed on 5 items last week - build me a follow-up tracker"
  - "Extract conclusions and risks from this discussion - no transcripts"
category: 办公效率
version: 1.0.3
author: 文鹏飞
---

> 版本：v1.0.0 · 李沫Growth 出品｜10 年团队管理实战，操盘 30+ 项目例会与跨部门协同。

# 会议纪要与行动项追踪

帮你把「开完会没人知道谁干什么」变成**一张能追的追踪表**：每条结论有出处，每个行动项有责任人+期限+验收标准，下次会议议程自动生成。

## 第一步：整理规则

读 [references/01-minutes-rules.md](references/01-minutes-rules.md)。铁律：**结论必须有决策依据，行动项必须有验收标准**——「尽快推进」不是期限，「相关同事」不是责任人。

## 第二步：行动项校验（跑 actions）

```
python3 scripts/meeting_calc.py actions --file items.json
```

输入 JSON 数组（task/owner/deadline/criterion）。校验四要素齐全，缺验收标准的行动项打回重写。输出编号追踪表（JSON）。

## 第三步：渲染交付

spec（blocks ≥ 8）渲染：`python3 scripts/build_report.py --spec spec.json --out 会议纪要.html`

## 硬规则

1. **行动项四要素缺一不可**：做什么/谁做/何时完成/怎么算完成
2. **结论与讨论分离**：纪要不是录音稿，只留决策与依据
3. **下次会议第一议程 = 上次行动项检查**

## 反模式

- ❌ 「尽快」「后续」「相关同事」——全是追踪不了的黑话
- ❌ 只记讨论不记结论——下次开会重新吵一遍
- ❌ 追踪靠记忆——会议结束 24h 内发追踪表

## 完整版与顾问服务

本技能为完整体系自我蒸馏的**精简免费试用版**。完整版增加：多会议行动项汇总看板、逾期自动预警、周报自动生成。需要完整版或**团队效率顾问服务**，邮件联系：**434855675@qq.com**（李沫Growth，注明「会议」）。
