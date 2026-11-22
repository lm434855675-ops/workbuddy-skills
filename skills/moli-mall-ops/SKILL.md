---
name: moli-mall-ops
display_name: 微商城运营方案
display_name_en: Moli WeChat Mall Ops Planner
description: 微商城运营方案：把改版、没人点、会员日怎么做这类诉求转成可执行方案，含楼层效率诊断、券保本测算与话术合规检查。触发词：微商城运营、商城运营、会员日、私域商城。
description_zh: 微商城运营方案。把「首页要改版」「分类没人点」「会员日怎么做」这类诉求，转成带责任人、时间点、判定标准的可执行方案。内置楼层效率诊断、漏斗敏感度、券保本测算与话术合规检查，交付自包含 HTML 界面。触发词：微商城运营、商城运营、会员日、私域商城、首页装修。
description_en: A WeChat-mall ops-plan assistant turning vague requests into executable HTML plans with floor-efficiency diagnosis, funnel sensitivity, coupon break-even and compliance checks.
category: 电商运营
version: 1.0.1
author: 文鹏飞
examples_zh:
  - 首页 Banner 点击率只有 3%，楼层顺序怎么排，先动哪一层
  - 会员日发 20 元券、门槛 199，帮我算券面额上限和保本下单转化率
  - 上月 GMV 掉了 18%，帮我定位是流量、转化还是客单掉的那一环
examples_en:
  - "Homepage banner CTR is only 3% - how should the floors be ordered and which one should I change first"
  - "Member day: a 20 CNY coupon with a 199 threshold - calculate the max face value and the break-even order conversion rate"
  - "GMV dropped 18% last month - locate whether it is traffic, conversion or average order value"
---

> 版本：v1.0.1 · 作者：文鹏飞（微商城全案操盘：月 GMV 1000 万、单日峰值 60 万港币、SKU 3000+）

# 微商城运营方案

把"我要做商城运营"这类模糊诉求，转成**带责任人、时间点、判定标准的可执行清单**。
本 skill 只管四件事：**首页装修、分类导航、会员日、数据复盘**。不输出泛泛而谈的方法论。

## 第一步：判断场景，别急着写方案

先用一句话确认用户在哪个场景，再读对应参考资料。**同时命中多个就按优先级串起来做**（合规 > 会员日 > 首页 > 分类 > 复盘）。

| 用户说什么 | 场景 | 读哪个文件 |
|---|---|---|
| 首页要改版 / Banner 没人点 / 楼层怎么排 / 首屏放什么 | 首页装修 | `@references/01-scenarios.md` |
| 分类没人点 / 类目怎么建 / 导航 / 搜索没结果 / 商品分组 | 分类导航 | `@references/01-scenarios.md` |
| 会员日 / 88 会员日 / 会员权益 / 发券 / 储值 / 唤醒沉睡 | 会员日 | `@references/01-scenarios.md` |
| 埋点怎么配 / 坑位怎么统计 / 渠道码 / 归因口径 | 商城侧追踪 | `@references/02-metrics.md` |
| 复盘 / GMV 掉了 / 数据怎么看 / 定目标 | 数据复盘 | `@references/02-metrics.md` |
| 文案能不能这么写 / 短信怎么发 / 裂变玩法合不合规 | 文案合规 | `@references/04-compliance.md` |
| **任何场景的最终交付** | **出 HTML 界面** | **`@references/03-html-output.md`** |

## 第二步：先要基线信息，缺了就问

没有这些数字，写出来的方案是废的。**最多问一轮，用户答不上来的项就写「待补」并给默认假设继续**，不要卡住。

必问（4 项）：

1. **平台与载体** —— 有赞 / 微盟 / 自建小程序？小程序还是 H5？
2. **主营类目 + 客单价 + 毛利率** —— 决定券面额上限、货盘结构、类目树形态
3. **会员与触点** —— 会员数、可触达比例、有没有企微/社群/导购
4. **本次目标 + 周期** —— GMV 数字、时间窗口、可投预算

选问（有则更准）：近 28 天各楼层曝光/点击/引导 GMV（首页场景必需）、平日日均 GMV（会员日算增量必需）、
近 30 天搜索词 Top 100（分类场景）、历史活动的漏斗五环节实际值。

**首页改版场景没有楼层数据就别硬做诊断** —— 直接说"需要后台的楼层曝光/点击/引导 GMV 才能定楼层顺序"，
先给结构建议和取数清单，拿到数据再跑诊断。

## 第三步：能算的必须用脚本算，不要口算

涉及钱和目标的地方一律走 `scripts/`，口算的让利方案经常是亏的。

### 运营测算 —— `scripts/mall_calc.py`

```bash
# 楼层效率诊断：CTR、坑位 UV 价值、四种判定与建议楼层顺序
python3 scripts/mall_calc.py floor \
    --floor "首屏轮播,52000,6100,420,68000" --floor "限时秒杀,41000,3900,510,79000"

# 漏斗诊断 + 单环节提升的 GMV 敏感度（第三个字段是该环节基准值，可不填）
python3 scripts/mall_calc.py funnel --aov 168 \
    --step "短信触达,50000" --step "进入商城,6000,15%" --step "支付成功,520"

# 券门槛/面额与保本增量占比
python3 scripts/mall_calc.py coupon --aov 168 --gross-margin-rate 45% \
    --face 20 --threshold 199 --redeem-rate 12% --issued 50000

# 会员日全链路：GMV / 成本 / ROI / 保本下单转化率 / 扣基线的增量
python3 scripts/mall_calc.py member --members 126000 --reach-rate 60% \
    --open-rate 12% --order-rate 8% --aov 168 --gross-margin-rate 45% \
    --discount-rate 12% --reach-cost 0.045 --baseline-gmv 38000

# GMV 目标倒推
python3 scripts/mall_calc.py gmv --target 1260000 --uv 90000 --cvr 1.8% --aov 168
```

比率支持 `0.12` / `12%` 两种写法。加 `--json` 输出结构化结果。纯 Python3 标准库。

**三个必须出现在方案里的数字**：券面额上限、保本下单转化率、扣掉平日基线的增量 GMV。

## 第四步：交付物是 HTML 界面，不是 md 文档

**这是本 skill 的硬性交付标准。** 用户要拿到的是一个能直接打开的方案界面 —— 深浅色自适应、清单能勾选、
图表能悬浮看细节、能打印。写完 md 就收工是不合格的交付。

```
读 references/ 定内容 → mall_calc.py 算数 → 写 spec.json → build_report.py 渲染 → 交付 HTML
```

```bash
python3 scripts/build_report.py --schema                                  # 查字段
python3 scripts/build_report.py --spec /tmp/plan.json --check             # 只校验体量，不渲染
python3 scripts/build_report.py --spec /tmp/plan.json --out "方案.html"    # 生成
```

### 体量闸门：内容太少直接拒绝渲染

**渲染器会先算体量再出 HTML，不达标退出码 2 且不写文件。** 这是为了挡住「区块齐全但每个数组都是空的」
空壳方案。触发拒绝的条件：

| 条件 | 默认门槛 |
|---|---|
| 区块数过少 | < 8（`--min-blocks` 可调） |
| 正文字符数过少 | < 1500（`--min-chars` 可调） |
| 某区块的内容数组为空 | 如 `tiles.items` / `table.rows` / `checklist` 全组无条目 → 会渲染成空卡片 |
| `timeline` 动作缺 `criterion` | 判定标准是强制字段，缺一个就拒 |
| 区块类型写错 | 未知类型会被整块丢掉，直接报错并列出可用类型 |
| 全篇没有承载型区块 | 只有 `section`/`callout` 是观点文，不是可执行方案 |

`--allow-thin` 是逃生口，**只用于诊断类快速回答**。**方案交付场景不要用它绕过闸门 —— 报错是在告诉你内容没写够，把内容补上。**

### 通用原则（违反会出错，不是风格建议）

- **输出由脚本一次性渲染，禁止手动追加。** 最终 HTML 由 `build_report.py` 一次性覆写到 `--out`。
  **不要**用 Write/Edit 手动改产出的 HTML —— 要改内容就改 spec.json 后重跑。
- **单一事实源**：区块字段定义以 `scripts/build_report.py --schema` 为准。
- **引用 reference 用相对于 SKILL.md 的路径。**

## 全局硬规则：写方案时不能违背的

| 项 | 要求 |
|---|---|
| 楼层排序 | 依据坑位 UV 价值（引导 GMV / 曝光 UV），不是 CTR，不是"看起来重要" |
| 首屏 | 只放三层：身份入口 → 主 KV → 券/核心玩法 |
| 类目树 | 三级封顶，一级 ≤ 8 个，每组 ≥ 6 个在售 SKU；更深的做成筛选项 |
| 券面额 | ≤ 按门槛成交的单笔毛利 × 0.5 |
| 券门槛 | 客单价 × 1.15 ~ 1.3，并配凑单专区 |
| 让利率 | 必须 < 毛利率；脚本会在 ≥ 毛利率时直接报错退出 |
| 触达顺序 | 订阅消息 → 企微/导购 → 站内 → 短信（按成本，短信永远最后） |
| 短信 | 必须有【签名】+ 退订标识；正文压在 70 字内；避开 21:00–08:00 |
| 微信生态 | 不得把分享/转发/关注设为领奖前置条件（诱导分享，链接会被拦截） |
| 会员日增量 | 必须扣平日基线：活动 GMV − 平日日均 GMV × 活动天数 |
| 活动期改动 | 首页活动版与临时分类都要写明下线/回滚时间 |
| 文案 | 禁广告法极限词；划线价须为真实成交价并留存举证 |

> **时效性声明**：各平台的后台菜单与组件名随版本迭代，本 skill 按能力维度描述，不锁死菜单路径。
> 方案里写到具体路径时，附一句"以当前版本后台为准"。

## 常见反模式：看到就纠正

用户提这些想法时，直接指出问题并给替代方案：

- **"首页整个重做一版"** → 一次只动 2–3 层，否则不知道是哪一层起的作用，下次还是拍脑袋。
- **"Banner 做好看点击率就上来了"** → 点击率取决于利益点是否清晰，先改文案再改视觉。
- **"类目建全一点，用户总能找到"** → 类目越多每个曝光越少；三级封顶，其余做筛选项。
- **"会员日就是全场打折"** → 全场折扣没有身份感还破坏价格体系；会员日要的是"只有会员能拿到"。
- **"先发短信看看效果"** → 短信成本最高、投诉最高，排在订阅消息与企微之后。
- **"给所有会员发同一张券"** → 等于给高价值会员白白打折，至少分三档。
- **"会员日 GMV 涨了 3 倍，成功"** → 扣平日基线后可能只涨 20%，甚至透支了后一周。
- **"邀请 3 人助力得券"** → 微信生态诱导分享，链接会被拦截，整场活动打不开。
- **"数据回头再看"** → 坑位与渠道埋点必须活动前配好，事后补不了。
- **"抄行业转化率基准"** → 品类与私域结构差异太大；用自己近 3 个月的中位数当基准。

## 试试这样问我

可以直接这样问我（也欢迎换成你自己的场景）：

1. 首页 Banner 点击率只有 3%，楼层顺序怎么排，先动哪一层
2. 会员日发 20 元券、门槛 199，帮我算券面额上限和保本下单转化率
3. 上月 GMV 掉了 18%，帮我定位是流量、转化还是客单掉的那一环

## 目录索引

```
微商城运营方案/
├── SKILL.md
├── references/
│   ├── 01-scenarios.md          # 场景路由：首页/分类/会员日的判定要素与流程
│   ├── 02-metrics.md            # 指标体系 + 埋点口径 + 取数节奏
│   ├── 03-html-output.md        # 交付规范：场景→区块配方
│   └── 04-compliance.md         # 词库与结构规则、微信生态红线
└── scripts/
    ├── mall_calc.py             # floor / funnel / coupon / member / gmv 五类测算
    ├── check_copy.py            # 文案合规：极限词 + 短信/裂变/会员储值/Banner 规则
    └── build_report.py          # ★ spec.json → 成品 HTML（含体量闸门）
```
