# WorkBuddy Agent Skills · LiMo Growth

> Author: **文鹏飞 (Wenpeng Fei)**, LiMo Growth · **33 skills** · Updated: 2026-11-22 · [简体中文说明](README.zh-CN.md)

A collection of **33 production-grade agent skills** in the portable `SKILL.md` format, originally authored for the [WorkBuddy](https://codebuddy.cn) agent platform and its skill marketplace — equally usable on Claude Code, CodeBuddy and any other agent platform that supports SKILL.md.

Each skill = one `SKILL.md` (trigger words + workflow + hard rules) plus optional `references/` (domain playbooks), `scripts/` (runnable calculators) and `examples/` (sample data).

> 📝 **Language note**: skill *content* is written in Chinese — it targets China private-domain e-commerce / WeCom (企业微信) scenarios. The structure, workflow format and Python calculators are platform-agnostic and work with any LLM agent; Chinese reading ability is required to use a skill's playbook.

## Skill Catalog

### Content Creation · 内容创作（2）

Spoken-video scripts and AI-text de-flavoring rewriter

| Skill | Version | What it does |
|---|---|---|
| [Humanizer](skills/humanizer/) `humanizer`<br>（中文文案去AI味检测与逐句改写器） | 2.1.1 | Remove AI writing patterns from text. |
| [Moli Viral Spoken Script Generator](skills/moli-viral-script/) `moli-viral-script`<br>（爆款口播脚本生成） | 1.0.6 | A Hook-body-CTA spoken-script generator across five script types (recruiting, seeding, IP persona and more)…. |

### Business Consulting · 商业咨询（14）

Project diagnosis, BP writing, contract/channel/quote/franchise tooling, scripts and SOPs

| Skill | Version | What it does |
|---|---|---|
| [Moli Account Quick Diagnosis](skills/moli-account-diagnosis/) `moli-account-diagnosis`<br>（账号快拆诊断） | 1.0.6 | A quick diagnosis scoring accounts or projects on traffic, conversion, product, ops and org, locating one c…. |
| [Moli 10-Section Business Plan Generator](skills/moli-bp-generator/) `moli-bp-generator`<br>（商业计划书十段生成器） | 1.0.1 | Turns a business into a 10-section investor-grade business plan: positioning, pain point, solution, market,…. |
| [Moli Business Model Diagnosis](skills/moli-business-diagnosis/) `moli-business-diagnosis`<br>（商业模式诊断） | 1.0.7 | A business-model diagnostician running a five-link chain check (positioning, value, monetization, growth, m…. |
| [Moli Channel Policy & Rebate Calculator](skills/moli-channel-policy/) `moli-channel-policy`<br>（渠道政策设计测算器） | 1.0.0 | Designs channel tier pricing, rebates and margin structures with break-even math so every tier has a real i…. |
| [Moli Closing Script Library Generator](skills/moli-closing-scripts/) `moli-closing-scripts`<br>（成交话术库生成器） | 1.0.0 | MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative franchise …. |
| [Moli Competitor Radar Report Generator](skills/moli-competitor-radar/) `moli-competitor-radar`<br>（竞品五维雷达对标分析） | 1.0.4 | MoliGrowth official. 30+ business diagnosis engagements with turnaround track record. This competitor-analy…. |
| [Moli Contract Risk Checklist Generator](skills/moli-contract-check/) `moli-contract-check`<br>（合同风险初审清单生成器） | 1.0.0 | Generates a first-pass contract risk checklist covering deposits, refunds, exclusivity, performance bonds a…. |
| [Moli Customer Follow-up SOP Generator](skills/moli-followup-sop/) `moli-followup-sop`<br>（客户跟进SOP生成器） | 1.0.0 | MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative revenue - …. |
| [Moli Franchise Script Generator](skills/moli-franchise-scripts/) `moli-franchise-scripts`<br>（招商加盟话术生成器） | 1.0.0 | Generates compliant franchise recruitment scripts — needs analysis, profit modeling, objection handling — w…. |
| [Moli Recruitment Launch Calculator](skills/moli-investment-calc/) `moli-investment-calc`<br>（招商起盘测算器） | 1.0.6 | A recruitment-launch calculator covering revenue back-solving, agent tiering with break-even rebates, polic…. |
| [Moli Objection Handling & Closing Scripts](skills/moli-objection-closing/) `moli-objection-closing`<br>（异议处理与逼单话术） | 1.0.0 | MoliGrowth official. 15 years in franchise and private-domain operations with 1B+ RMB cumulative revenue - …. |
| [Moli Quotation Proposal Generator](skills/moli-quote-builder/) `moli-quote-builder`<br>（报价方案生成器） | 1.0.0 | Builds value-anchored quotation proposals with tiered packages, deliverables and comparison anchors instead…. |
| [Moli Customer Referral Plan Generator](skills/moli-referral-plan/) `moli-referral-plan`<br>（老顾客转介绍方案生成器） | 1.0.0 | Designs old-customer referral programs: referrer rewards, trigger moments, follow-up scripts and ROI tracking. |
| [Moli Store Site Evaluation & Break-even Calculator](skills/moli-site-selection/) `moli-site-selection`<br>（门店选址评估与测算） | 1.0.3 | MoliGrowth official. 15 years of chain-store operations with 100+ site evaluations. A distilled free-trial …. |

### Private-Domain Operations · 私域运营（10）

Community, membership, Moments calendar, tagging, fission and win-back across the private-domain funnel

| Skill | Version | What it does |
|---|---|---|
| [Moli Private-domain Content Weekly Planner](skills/moli-content-weekly/) `moli-content-weekly`<br>（私域内容周历生成器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |
| [Moli Fission Campaign Calculator](skills/moli-fission-calc/) `moli-fission-calc`<br>（裂变活动方案测算器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |
| [Moli Group Lifecycle SOP Generator](skills/moli-group-sop/) `moli-group-sop`<br>（社群运营全周期SOP生成器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate, team…. |
| [Moli Lead Magnet Cost Checker](skills/moli-hook-design/) `moli-hook-design`<br>（引流品设计测算器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |
| [Moli Private-Domain Membership System Builder](skills/moli-member-system/) `moli-member-system`<br>（私域会员体系搭建） | 1.0.8 | MoliGrowth official. Built by a membership-operations director with 12 years of experience. This membership…. |
| [Moli Moments Calendar Generator](skills/moli-moments-calendar/) `moli-moments-calendar`<br>（朋友圈运营日历生成器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |
| [Moli Omni-Channel Linkage Plan Generator](skills/moli-omni-linkage/) `moli-omni-linkage`<br>（公私域联动方案生成器） | 1.0.3 | MoliGrowth official. Built by a private-domain operator with 15 years of experience - 1M+ members managed, …. |
| [Moli Silent Customer Win-back Planner](skills/moli-silent-wake/) `moli-silent-wake`<br>（沉默顾客唤醒方案生成器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |
| [Moli Private-Domain Tag System Builder](skills/moli-tag-system/) `moli-tag-system`<br>（私域标签体系搭建与分层运营） | 1.0.3 | MoliGrowth official. Built by a private-domain operator with 15 years of experience - 1M+ members managed, …. |
| [Moli WeCom Welcome & Follow-up Script Generator](skills/moli-welcome-scripts/) `moli-welcome-scripts`<br>（企微欢迎语与承接话术生成器） | 1.0.0 | MoliGrowth official. 15 years in private-domain operations - 1M+ members managed, 68% repurchase rate. A di…. |

### Operations & Team · 运营人力（1）

Full-case coaching SOPs and meeting minutes tracking

| Skill | Version | What it does |
|---|---|---|
| [Moli Full-Case SOP Generator](skills/moli-fullcase-sop/) `moli-fullcase-sop`<br>（全案陪跑SOP生成器） | 1.0.7 | A full-case SOP generator turning projects into executable HTML plans with milestones, department splits, w…. |

### E-commerce Operations · 电商运营（2）

Member campaign planning and WeChat-mall operations

| Skill | Version | What it does |
|---|---|---|
| [Moli WeChat Mall Ops Planner](skills/moli-mall-ops/) `moli-mall-ops`<br>（微商城运营方案） | 1.0.1 | A WeChat-mall ops-plan assistant turning vague requests into executable HTML plans with floor-efficiency di…. |
| [Moli Member Activity Planner](skills/moli-member-activity/) `moli-member-activity`<br>（会员活动策划执行） | 1.1.6 | A member-activity planner with benefit levers, touchpoint matrix and baseline-adjusted increment accounting…. |

### Office Productivity · 办公效率（2）

Meeting action items and the Tencent-Docs html→docx re-layout pipeline

| Skill | Version | What it does |
|---|---|---|
| [Moli Meeting Minutes & Action Tracker](skills/moli-meeting-actions/) `moli-meeting-actions`<br>（会议纪要与行动项追踪） | 1.0.3 | MoliGrowth official. 10 years of team management, chairing 30+ project reviews. A distilled free-trial edit…. |
| [Tencent Docs html→docx Re-layout Pipeline](skills/tencent-docx-html2docx-pipeline/) `tencent-docx-html2docx-pipeline`<br>（腾讯文档 html→docx 重排版管线） | 1.0.0 | Re-layout existing Word docs by driving WorkBuddy's built-in tencent-docx html_to_docx engine directly (mar…. |

### Marketing & Growth · 营销增长（2）

Private-domain conversion funnel and new-product seeding plans

| Skill | Version | What it does |
|---|---|---|
| [Moli Private Domain Conversion Planner](skills/moli-private-conversion/) `moli-private-conversion`<br>（私域转化链路方案） | 1.0.6 | A private-domain conversion planner covering response capacity, tiered scripts and a 14-day follow-up rhyth…. |
| [Moli Product Seeding Campaign Planner](skills/moli-seeding-campaign/) `moli-seeding-campaign`<br>（新品上市种草方案） | 1.0.7 | A product-seeding campaign planner for Xiaohongshu and Douyin with topic matrix, three-tier influencer mix,…. |

## Install & Use

**WorkBuddy / CodeBuddy**: copy a skill folder into `~/.workbuddy/skills/` (Windows: `%USERPROFILE%\.workbuddy\skills\`), restart the app, then invoke it with the trigger phrases in its description.

**Claude Code / other SKILL.md platforms**: copy into the platform's skills directory (e.g. `~/.claude/skills/`), or simply hand the skill folder to any LLM agent as reference material.

**No install needed**: every `SKILL.md` is a self-contained playbook — any model can follow it directly. A machine-readable index is available in [catalog.json](catalog.json).

## Notes

- `tencent-docx-html2docx-pipeline` drives WorkBuddy's built-in tencent-docx plugin; the plugin root varies by installation — see its SKILL.md for how to locate it.
- All machine-specific paths have been removed; data directories in scripts are parameterized via environment variables where applicable.

## Custom Versions

These are the free, generic editions. Plug in **your own products, scripts library and customer data** to get a custom private agent for your business — contact **434855675@qq.com** (also on WeChat).

## License

[MIT](LICENSE) © 2026 文鹏飞 (Wenpeng Fei) · LiMo Growth
