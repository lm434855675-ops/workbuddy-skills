# WorkBuddy 智能体技能库 · 李沫Growth 出品

> 🌐 [English](README.md) | 简体中文

> 作者：**文鹏飞**（李沫Growth） · 技能数 **33** · 最后更新：2026-11-22

这是一套按照 **Agent Skills（SKILL.md）规范**编写的智能体技能与专家包，最初为 [WorkBuddy](https://codebuddy.cn) 智能体平台创作并上架技能市场，同样兼容 Claude Code、CodeBuddy 等任何支持 SKILL.md 技能规范的 Agent 平台。

每个技能 = 一份 `SKILL.md`（触发词 + 工作流 + 硬规则）+ 可选的 `references/`（领域知识库）+ `scripts/`（可执行计算脚本）+ `examples/`（样例数据）。

## 技能目录

### 商业咨询（14 个）

项目诊断、BP、合同/渠道/报价/招商、话术与 SOP 类技能

| 技能 | 版本 | 说明 |
|---|---|---|
| [账号快拆诊断](skills/moli-account-diagnosis/) `moli-account-diagnosis` | 1.0.6 | 李沫Growth 出品｜商业咨询 5 年诊断企业 100+，濒停项目救活 30+，一次诊断只打一个七寸。项目诊断三大死法：全面体检等于没诊断，二十个问题没重… |
| [商业计划书十段生成器](skills/moli-bp-generator/) `moli-bp-generator` | 1.0.1 | 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 激停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版… |
| [商业模式诊断](skills/moli-business-diagnosis/) `moli-business-diagnosis` | 1.0.7 | 李沫Growth 出品｜乙方商业咨询 5 年服务企业 100+，濒停项目重新定位救活 30+。商业模式三大死法：说「什么人都能用」等于没定位、没定价权；先做… |
| [渠道政策设计测算器](skills/moli-channel-policy/) `moli-channel-policy` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治分销折扣一拍脑袋渠道没动力、返点层级… |
| [成交话术库生成器](skills/moli-closing-scripts/) `moli-closing-scripts` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+，成交就是招商的最后一米。这套话术体系从招商一线打法蒸馏，精简免费试用版上传，专治成… |
| [竞品五维雷达对标分析](skills/moli-competitor-radar/) `moli-competitor-radar` | 1.0.4 | 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。竞品分析框架在月 GMV 1000 … |
| [合同风险初审清单生成器](skills/moli-contract-check/) `moli-contract-check` | 1.0.0 | 李沫Growth 出品｜15 年商业操盘手，乙方商业咨询 5 年服务企业 100+，30+ 濒停项目重新定位陪跑至复活。这套打法从实战盘蒸馏，精简免费试用版… |
| [客户跟进SOP生成器](skills/moli-followup-sop/) `moli-followup-sop` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——成交八成靠跟进，丢单八成死在没跟。这套跟进体系从高客单 1v1 私域打法蒸馏（留… |
| [招商加盟话术生成器](skills/moli-franchise-scripts/) `moli-franchise-scripts` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治话术只会夸项目、承诺收益踩法律红线、… |
| [招商起盘测算器](skills/moli-investment-calc/) `moli-investment-calc` | 1.0.6 | 李沫Growth 出品｜15 年招商操盘，累计招商回款 10 亿+：酵素首月 500 万、酱酒 3 个月 1038 万、私护年回款 1000 万。起盘三大死… |
| [异议处理与逼单话术](skills/moli-objection-closing/) `moli-objection-closing` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+——异议处理不是辩赢顾客，是给顾客一个台阶往下走。这套逼单打法从招商一线蒸馏，精简免… |
| [报价方案生成器](skills/moli-quote-builder/) `moli-quote-builder` | 1.0.0 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+。这套打法从实战盘蒸馏，精简免费试用版上传，专治报价拍脑袋毛利算不清、一份报价打天下… |
| [老顾客转介绍方案生成器](skills/moli-referral-plan/) `moli-referral-plan` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [门店选址评估与测算](skills/moli-site-selection/) `moli-site-selection` | 1.0.3 | 李沫Growth 出品｜15 年连锁与门店操盘实战，选址评估过 100+ 门店点位，操盘过月 GMV 1000 万微商城的线下线上融合盘。精简免费试用版上传… |

### 私域运营（10 个）

社群、会员、朋友圈、标签、裂变与唤醒等私域全链路技能

| 技能 | 版本 | 说明 |
|---|---|---|
| [私域内容周历生成器](skills/moli-content-weekly/) `moli-content-weekly` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [裂变活动方案测算器](skills/moli-fission-calc/) `moli-fission-calc` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [社群运营全周期SOP生成器](skills/moli-group-sop/) `moli-group-sop` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [引流品设计测算器](skills/moli-hook-design/) `moli-hook-design` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [私域会员体系搭建](skills/moli-member-system/) `moli-member-system` | 1.0.8 | 李沫Growth 出品｜12年会员体系运营总监，这套会员体系会员总量超 100 万，会员复购率干到 68%，付费会员卡单年卖出 5 万张。融合操盘过月 GM… |
| [朋友圈运营日历生成器](skills/moli-moments-calendar/) `moli-moments-calendar` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [公私域联动方案生成器](skills/moli-omni-linkage/) `moli-omni-linkage` | 1.0.3 | 李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV … |
| [沉默顾客唤醒方案生成器](skills/moli-silent-wake/) `moli-silent-wake` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |
| [私域标签体系搭建与分层运营](skills/moli-tag-system/) `moli-tag-system` | 1.0.3 | 李沫Growth 出品｜15年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。融合操盘过月 GMV … |
| [企微欢迎语与承接话术生成器](skills/moli-welcome-scripts/) `moli-welcome-scripts` | 1.0.0 | 李沫Growth 出品｜15 年私域实战操盘手，操盘会员总量超 100 万，会员复购率干到 68%，日进线 1500+ 的私域直营团队。这套打法从实战盘蒸馏… |

### 营销增长（2 个）

私域转化链路与新品种草方案生成

| 技能 | 版本 | 说明 |
|---|---|---|
| [私域转化链路方案](skills/moli-private-conversion/) `moli-private-conversion` | 1.0.6 | 李沫Growth 出品｜15 年私域直营操盘，带过 200 人直营团队，14 天成交 SOP 日进线 1.2 万+，年度 GMV 1.3 亿。私域转化三大死… |
| [新品上市种草方案](skills/moli-seeding-campaign/) `moli-seeding-campaign` | 1.0.7 | 李沫Growth 出品｜15 年新品上市与内容操盘，操盘种草战役 30+，单战役 C 端订单破万。新品种草三大死法：上来先砸头部达人，预算烧完没复购；素人笔… |

### 内容创作（2 个）

口播脚本与文案去 AI 味改写

| 技能 | 版本 | 说明 |
|---|---|---|
| [中文文案去AI味检测与逐句改写器](skills/humanizer/) `humanizer` | 2.1.1 | 去除文本中的 AI 写作痕迹 |
| [爆款口播脚本生成](skills/moli-viral-script/) `moli-viral-script` | 1.0.6 | 李沫Growth 出品｜15 年招商与私域操盘，累计招商回款 10 亿+，经手口播与招商会脚本 500+ 条。口播脚本三大死法：前 3 秒没钩子，八成观众划… |

### 电商运营（2 个）

会员活动策划与执行

| 技能 | 版本 | 说明 |
|---|---|---|
| [微商城运营方案](skills/moli-mall-ops/) `moli-mall-ops` | 1.0.1 | 微商城运营方案。把「首页要改版」「分类没人点」「会员日怎么做」这类诉求，转成带责任人、时间点、判定标准的可执行方案。内置楼层效率诊断、漏斗敏感度、券保本测算… |
| [会员活动策划执行](skills/moli-member-activity/) `moli-member-activity` | 1.1.6 | 李沫Growth 出品｜15 年私域会员操盘手，实体店会员+线上商城双体系会员总量超 100 万，复购率干到 68%。会员活动三大死法：会员日做成全场打折，… |

### 运营人力（1 个）

全案陪跑 SOP 与会议纪要追踪

| 技能 | 版本 | 说明 |
|---|---|---|
| [全案陪跑SOP生成器](skills/moli-fullcase-sop/) `moli-fullcase-sop` | 1.0.7 | 李沫Growth 出品｜乙方商业咨询 5 年服务企业 100+，濒停项目救活 30+，结项标准只有一个：服务方撤场项目照常跑。把「这个项目怎么陪跑」转成阶段… |

### 办公效率（2 个）

会议行动项与腾讯文档 html→docx 转换管线

| 技能 | 版本 | 说明 |
|---|---|---|
| [会议纪要与行动项追踪](skills/moli-meeting-actions/) `moli-meeting-actions` | 1.0.3 | 李沫Growth 出品｜10 年团队管理实战，主持操盘 30+ 项目例会与跨部门协同。这套会议纪要方法在多项目并行的实战盘里打磨，精简免费试用版上传，专治会… |
| [tencent-docx-html2docx-pipeline](skills/tencent-docx-html2docx-pipeline/) `tencent-docx-html2docx-pipeline` | 1.0.0 | 直接驱动 tencent-docx 插件的 html_to_docx 引擎重新生成 Word（含小页边距、致辞/附录单独分页、审门禁全过）的完整命令与坑清单… |

## 安装使用

**WorkBuddy / CodeBuddy**：把技能文件夹复制到 `~/.workbuddy/skills/`（Windows 为用户目录下 `.workbuddy\skills\`），重启应用后即可用技能描述中的触发词调用。

**Claude Code / 其它 SKILL.md 平台**：复制到对应的 skills 目录（如 `~/.claude/skills/`），或把某个技能文件夹直接作为上下文资料交给智能体阅读执行。

**不装也能用**：每个 `SKILL.md` 都是自足的工作流文档，可以直接让任何大模型按它执行。

机器可读索引见 [catalog.json](catalog.json)。

## 特殊说明

- **tencent-docx-html2docx-pipeline**：面向 WorkBuddy 内置 tencent-docx 插件的重排版管线，插件根路径因安装方式而异，按 SKILL.md 内的定位方法查找。
- **路径可移植性**：所有技能已去除本机专属路径；脚本内的硬编码数据目录均已参数化。

## 定制专属版

这些技能均为通用版。把你的产品、话术库、客户数据接入，即可定制为你自己的专属智能体——
专属版定制与完整版顾问服务请联系：**434855675@qq.com**（邮箱同微信号）。

## License

[MIT](LICENSE) © 2026 文鹏飞（李沫Growth）
