# artifact_specs — 交付物接口规格汇总

> 更新: 2026-04-02

## 数据交付物规格

| 交付物ID | 文件名 | 模块 | 列数 | 行数 | 主键 | 编码 | 供给栏目 |
|---------|--------|------|------|------|------|------|---------|
| API-A | entity_list.csv | A | 21 | 32 | entity_id | UTF-8-BOM | 栏目1 企业主体 |
| API-B | monthly_operation.csv | B | 28 | 15 | record_id | UTF-8-BOM | 栏目2 经营数据 |
| API-C | policy_briefing.csv | C | 15 | 12 | id | UTF-8-BOM | 栏目3 收益规则(政策) |
| API-D1 | budget_rules.csv | D | 21 | 21 | record_id | UTF-8-BOM | 栏目3(RULE)+栏目4(FIGURE/TRANSFER) |
| API-D2 | budget_transfer.csv | D | 3 | 31 | province | UTF-8-BOM | 栏目4 转移支付明细 |

## 证据回链字段对照表

| 模块 | URL字段 | 等级字段 | 机构字段 | 文件字段 | 日期字段 |
|------|---------|---------|---------|---------|---------|
| A | source_url | uev_level (int 1~5) | source_institution | — | extraction_date |
| B | source_url | uev_level (int 1~5) | source_institution | source_title | publish_date |
| C | evidence_url | evidence_strength (str S1~S4) | issuer | title | doc_date |
| D | source_url | evidence_strength (str S1~S4) | — | source_doc | source_date |

**统一标准** (UNIFY-01): evidence_url / evidence_strength / evidence_institution / evidence_date

## 省份编码对照表

| 标准码(UNIFY-02) | 中文 | 模块A | 模块B | 模块D transfer |
|---------|------|-------|-------|---------------|
| GD | 广东 | GD | — | guangdong |
| ZJ | 浙江 | ZJ | ZJ | zhejiang |
| SD | 山东 | SD | — | shandong |
| SC | 四川 | SC | — | sichuan |
| CN | 全国 | — | CN | — |

## Record_type枚举 (UNIFY-03)

| 值 | 含义 | 来源CSV | 目标栏目 |
|----|------|---------|---------|
| ENTITY | 企业主体 | entity_list | 栏目1 |
| DATA | 经营数据 | monthly_operation | 栏目2 |
| POLICY | 政策文件 | policy_briefing | 栏目3 |
| RULE | 比例规则 | budget_rules | 栏目3 |
| BUDGET_FIGURE | 预算数字 | budget_rules | 栏目4 |
| TRANSFER | 转移支付 | budget_rules | 栏目4 |
| UNIDENTIFIED | 未识别 | budget_rules | 栏目4 |

## 筛选维度 (API-03)

| 栏目 | 维度1 | 维度2 | 维度3 |
|------|-------|-------|-------|
| 1 企业主体 | province | list_caliber | admin_level |
| 2 经营数据 | scope_code | indicator_name | province |
| 3 收益规则 | doc_type_code | topic_primary | ratio_type |
| 4 财政统筹 | scope | record_type | — |
