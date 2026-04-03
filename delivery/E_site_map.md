# E_site_map — 网站结构与字段映射

> 日期: 2026-04-02
> 版本: v1.0
> 根目录: site/

## 站点地图

```
site/
├── index.html                    # 首页总览
├── css/main.css                  # 全局样式
├── js/app.js                     # 数据加载+渲染核心(CSV解析/证据回链/图表)
├── data/
│   ├── entity_list.csv           # 模块A 32条×21字段
│   ├── monthly_operation.csv     # 模块B 15条×28字段
│   ├── policy_briefing.csv       # 模块C 12条×15字段
│   ├── budget_rules.csv          # 模块D 21条×21字段
│   └── budget_transfer.csv       # 模块D 31条×3字段
└── pages/
    ├── entities.html             # 栏目1: 国资企业主体
    ├── operations.html           # 栏目2: 企业经营数据分析
    ├── policies.html             # 栏目3: 收益管理规则动态
    └── budget.html               # 栏目4: 财政统筹结果
```

## 页面→底表→字段映射

### 栏目1: 国资企业主体 (entities.html → entity_list.csv)

| 页面元素 | 底表字段 | 类型 | 说明 |
|---------|---------|------|------|
| 企业名称 | entity_name_full | string | 主显示字段 |
| 省份 | province | string | 筛选维度 |
| 层级 | admin_level | enum | L1/L2/L3 |
| 口径 | list_caliber + list_caliber_label | enum+string | 筛选维度 |
| 行业 | sector | string | — |
| 置信度 | confidence | float | 数值显示 |
| 证据等级 | uev_level | int | 转换为S1~S4 badge |
| 来源回链 | source_url + source_institution + extraction_date | string | 证据面板 |

### 栏目2: 企业经营数据 (operations.html → monthly_operation.csv)

| 页面元素 | 底表字段 | 类型 | 说明 |
|---------|---------|------|------|
| 期间 | year + period_label | int+string | 组合显示 |
| 省份 | province | string | 筛选维度 |
| 口径 | scope + scope_code | string+string | 筛选维度 |
| 指标 | indicator_name | string | 筛选维度 |
| 数值 | value + unit | double+string | 格式化显示 |
| 同比 | yoy_pct + yoy_direction | double+string | 涨跌色 |
| 证据等级 | uev_level | int | S1~S4 badge |
| 来源回链 | source_url + source_institution + source_title + publish_date | string | 证据面板 |
| 图表: 柱状图 | indicator_name ∈ {营业总收入,利润总额,应交税费} × value × year | — | Canvas绘制 |
| KPI卡片 | value(最新全国累计) + yoy_pct | — | 4项核心指标 |

### 栏目3: 收益管理规则 (policies.html → policy_briefing.csv + budget_rules.csv[RULE])

| 页面元素 | 底表 | 底表字段 | 类型 | 说明 |
|---------|------|---------|------|------|
| 政策名称 | C | title | string | — |
| 发文机构 | C | issuer | string | — |
| 日期 | C | doc_date | date | — |
| 文种 | C | doc_type + doc_type_code | string+enum | A~E级 |
| 主题 | C | topic_primary | string | — |
| 政策证据 | C | evidence_url + evidence_strength | string+string | 证据面板 |
| 规则说明 | D | rule_description_zh | string | RULE类记录 |
| 比例 | D | ratio_value | string | 35%/30%/UNIDENTIFIED |
| 比例类型 | D | ratio_type | enum | net_profit_collection/transfer_to_gpb |
| 范围 | D | scope_label | string | central_soe/province_level/ALL |
| 规则证据 | D | source_url + evidence_strength + source_doc | string | 证据面板 |

### 栏目4: 财政统筹结果 (budget.html → budget_rules.csv[BUDGET_FIGURE/TRANSFER] + budget_transfer.csv)

| 页面元素 | 底表 | 底表字段 | 类型 | 说明 |
|---------|------|---------|------|------|
| 范围 | D | scope_label | string | national_total/central_budget/local_aggregate/province_level |
| 收入 | D | budget_income | decimal | 亿元 |
| 支出 | D | budget_expenditure | decimal | 亿元 |
| 调入公共预算 | D | budget_transfer_to_gpb | decimal | 亿元 |
| 同比 | D | yoy | string | — |
| 预算证据 | D | source_url + evidence_strength + source_doc | string | 证据面板 |
| 省份(转移) | Dt | province | string | 31省 |
| 2025执行数 | Dt | 2025_execution_100M_CNY | decimal | 亿元 |
| 2026预算数 | Dt | 2026_budget_100M_CNY | decimal | 亿元 |
| 图表: 横条图 | Dt | province × 2026_budget_100M_CNY TOP10 | — | Canvas绘制 |

## 证据回链机制

每条数据行通过以下字段实现证据回溯:

| 模块 | URL字段 | 等级字段 | 机构字段 | 文件字段 |
|------|---------|---------|---------|---------|
| A | source_url | uev_level(int 1~5) | source_institution | — |
| B | source_url | uev_level(int 1~5) | source_institution | source_title |
| C | evidence_url | evidence_strength(string S1~S4) | issuer | title |
| D | source_url | evidence_strength(string S1~S4) | — | source_doc |

前端通过 `evidenceLink(row)` 函数自动适配不同模块的字段名差异，统一渲染证据面板。

## 前端接口约定

| 接口 | 路径 | 返回格式 | 记录数 | 主键 |
|------|------|---------|--------|------|
| 企业主体 | data/entity_list.csv | CSV(21列) | 32 | entity_id |
| 经营数据 | data/monthly_operation.csv | CSV(28列) | 15 | record_id |
| 政策简报 | data/policy_briefing.csv | CSV(15列) | 12 | id |
| 预算规则 | data/budget_rules.csv | CSV(21列) | 21 | record_id |
| 转移支付 | data/budget_transfer.csv | CSV(3列) | 31 | province |

所有CSV均为UTF-8编码，逗号分隔，字符串字段双引号包裹。
前端通过 `DataStore.loadAll()` 统一加载并缓存。
