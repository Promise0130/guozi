# normalization_rules — 本轮实际使用的规范化规则

> 更新: 2026-04-02

## 指标名称映射(实际触发)

| 原始名 | 标准化名 | 规则 | 触发省份 |
|--------|---------|------|---------|
| 营业收入 | 营业总收入 | R7.1 | 浙江 |
| (暂无更多触发) | — | — | — |

## 调整后同比处理(实际触发)

| 原始表述 | 处理方式 | 规则 | 触发省份 |
|---------|---------|------|---------|
| 剔除政策性因素后同比增长8.6% | 独立记录+yoy_adjusted=true | R7.5 | 浙江 |

## 单位标准化(实际触发)

| 原始 | 标准化 | 规则 |
|------|--------|------|
| 亿元 | 亿元(保持) | R7.2 |
| % | %(保持) | R7.2 |
| 个百分点 | 百分点(yoy单位) | R7.6 |

## 期间拆分(实际触发)

| 原始 | 拆分结果 | 规则 |
|------|---------|------|
| 浙江1月+1-2月同文 | 2条独立记录 | R6.5 |

---

## 模块D 预算规则 规范化规则

### record_type二分(实际触发)

| 原始表述 | 分类结果 | 规则 |
|---------|---------|------|
| “收入预算3716.32亿元” | record_type=BUDGET_FIGURE | BDG-01 |
| “税后利润收取比例为35%” | record_type=RULE | BDG-01 |
| “转移支付0.75亿元” | record_type=TRANSFER | BDG-01 |

### scope多级编码(实际触发)

| 原始表述 | scope编码 | scope_label | 规则 |
|---------|---------|------------|------|
| “全国国有资本经营预算” | national | national_total | SCOPE-01 |
| “中央国有资本经营预算” | central | central_budget | SCOPE-01 |
| 预算草案中“地方本级” | local | local_aggregate | SCOPE-01+02 |
| “中央对广东转移支付” | province | central_to_local | SCOPE-01+03 |

### 比例未识别处理(实际触发)

| 场景 | 处理 | 规则 |
|------|------|------|
| 省级比例不在预算草案 | ratio_value=UNIDENTIFIED, evidence_strength=S4 | BTPL-02 |
| 中央Tier3/4截断 | ratio_value=UNIDENTIFIED, notes含"truncated" | BDG-03+BTPL-02 |

### 特殊条目处理(实际触发)

| 原始表述 | 处理 | 规则 |
|---------|------|------|
| “收入总量3976.23亿=当年3716.32+结转259.91” | budget_income=当年数, notes记录总量 | SPEC-02 |
---

## 模块E 网站展示层 规范化规则

### 跨模块证据字段名映射(实际触发)

| 模块 | URL字段 | 强度字段 | 机构字段 | 前端统一名 | 规则 |
|------|---------|---------|---------|-----------|------|
| A | source_url | uev_level(int) | source_institution | evidence_url / evidence_strength / institution | UNIFY-01 |
| B | source_url | — | source_institution | evidence_url / — / institution | UNIFY-01 |
| C | evidence_url | evidence_strength(str) | issuer | evidence_url / evidence_strength / institution | UNIFY-01 |
| D | evidence_url | evidence_strength(str) | institution | evidence_url / evidence_strength / institution | UNIFY-01 |

### 省份编码标准化(实际触发)

| 模块 | 原始格式 | 标准化格式 | 规则 |
|------|---------|-----------|------|
| A | 全称(浙江省) | province=ZJ | UNIFY-02 |
| B | 全称(浙江省) | province=ZJ | UNIFY-02 |
| D-transfer | 全称(广东省) | province=GD | UNIFY-02 |
| 说明 | 仅1省(浙江)有月度数据, 暂无跨省冲突 | — | — |

### record_type分栏路由(实际触发)

| record_type值 | 路由栏目 | 规则 |
|--------------|---------|------|
| RULE | 栏目3 收益管理规则 | API-02 |
| BUDGET_FIGURE | 栏目4 财政统筹 | API-02 |
| TRANSFER | 栏目4 财政统筹 | API-02 |

### 数值格式化(实际触发)

| 输入 | 输出 | 规则 |
|------|------|------|
| UNIDENTIFIED | 红色"未识别"标签 | CHART-02 |
| 3716.32 | 3,716.32 | 千位分隔(fmtNum) |
| yoy_pct>0 | 绿色↑ | yoyTag() |
| yoy_pct<0 | 红色↓ | yoyTag() |