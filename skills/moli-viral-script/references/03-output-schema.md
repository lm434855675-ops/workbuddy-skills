# 03 · 输出 Schema（单一事实源）

> 本文件是字段定义的唯一权威。SKILL.md 与 `scripts/render_script.py` 不得与本表冲突。

## 顶层结构

```json
{
  "title": "脚本标题",
  "duration_sec": 90,
  "info": { ... },
  "script_type": "recruit",
  "campaign_types": ["agent_recruit"],
  "structure": { ... },
  "rhythm": { ... },
  "structure_summary": "一句话结构说明",
  "rhythm_evidence": "节奏设计依据",
  "product_conversion": { ... } | null,
  "tags": ["标签1", "标签2"]
}
```

## info 对象（5 字段原样带回）

| 字段 | 类型 | 必填 |
|---|---|---|
| purpose | string | 是 |
| industry | string | 是 |
| audience | string | 是 |
| topic | string | 是 |
| product | string \| null | 否 |

## structure 对象

```
structure.hook          # Hook 段，index 恒为 1
structure.body.segments # 中段数组，index 从 2 起升序
structure.cta           # CTA 段，index 恒为 99
```

### 段对象（hook / segment / ca 同构）

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| index | int | 是 | hook=1；segments 从 2 连续升序；cta=99 |
| start | number | 是 | 秒；hook.start=0；每段 start=上一段 end |
| end | number | 是 | 秒；end>start；cta.end=duration_sec |
| visual | string | 是 | 画面描述，≤50 字 |
| dialogue | string | 是 | 台词，单句 ≤15 字 |
| note | string | 否 | 拍摄/剪辑备注 |

## rhythm 对象

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| overall | string | 是 | 整体节奏描述（如"前快后稳"） |
| pause_points | number[] | 是 | 停顿点（秒），升序，须落在 (0, duration_sec) 内 |
| words_per_sec | number | 是 | 全文语速，4-5 之间 |

## product_conversion 对象（product 为 null 时整体为 null）

| 字段 | 类型 | 必填 |
|---|---|---|
| target | string | 是（转化目标，如"评论区扣 1 领政策表"） |
| trigger | string | 是（转化钩子，如"前 20 名送选品清单"） |

## tags

字符串数组，2-5 个，取自选题库或用户指定。

## 校验规则汇总（render_script.py 实现）

1. 顶层必填字段齐全且类型正确。
2. `script_type` ∈ 五大型谱枚举；`campaign_types` 非空且枚举合法。
3. 时间轴自洽：hook.start=0、段间连续无断裂、cta.index=99、cta.end=duration_sec。
4. segments 数量：`training` ≤7，其余 ≤5。
5. 每段 `dialogue` 存在且非空；`visual` ≤50 字。
6. `rhythm.words_per_sec` ∈ [4, 5]；`pause_points` 升序且在区间内。
