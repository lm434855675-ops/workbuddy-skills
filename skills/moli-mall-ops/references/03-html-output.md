# 03 · HTML 交付规范：场景 → 区块配方

## 区块类型（14 种）

`section` `tiles` `steps` `timeline` `gantt` `checklist` `table` `bars` `stack` `callout` `kv` `floorplan` `tree` `funnel`

## 场景配方

### 首页装修

| 区块 | 内容 |
|---|---|
| floorplan | 楼层结构图（带首屏折线，标注 fold） |
| table | 楼层诊断数据（曝光/点击/CTR/UV 价值/判定） |
| steps | 改版流程（取数→诊断→改一版→观察 7 天→固化/回滚） |
| timeline | 改动排期，每个动作带 criterion |
| checklist | 上线前检查项 |
| callout | 风险项（活动版下线时间等） |

### 分类导航

| 区块 | 内容 |
|---|---|
| tree | 三级类目树 |
| table | 一级类目 SKU 数与在售数 |
| steps | 类目重构流程 |
| kv | 搜索词 Top 反哺结论 |

### 会员日

| 区块 | 内容 |
|---|---|
| gantt | 四段式排期（蓄水/预热/爆发/返场） |
| table | 触达矩阵（渠道/成本/到达率/内容） |
| kv | 三个必含数字（券面额上限/保本转化率/增量 GMV） |
| checklist | 权益确认清单 |
| funnel | 漏斗五环节（自动标出最大流失环节） |
| timeline | 每日动作带 owner + criterion |

### 数据复盘

| 区块 | 内容 |
|---|---|
| bars | 关键指标对比 |
| funnel | 漏斗诊断 |
| table | 增量 GMV 拆解 |
| steps | 下周期行动 |

## 硬性约束

1. **timeline 的 criterion 是强制字段**——每个动作必须写"做到什么算完成"（数字或状态）。
2. **owner 必填**：`运营` `采购` `导购` `仓储` `客服` `老板` 六选一。
3. **risk 标注**：涉及平台红线的动作填 `risk`，渲染时标红。
4. **回滚时间**：活动期首页与临时分类必须写下线时间。
5. **数字来自脚本**：券面额上限、保本转化率、ROI、增量 GMV 一律 mall_calc.py 输出，不手填。

## 深浅色与可交互

- 界面深浅色自适应（跟随系统）。
- checklist 可勾选、图表悬浮看细节、支持打印。
- 自包含单文件 HTML，不依赖外网资源。
