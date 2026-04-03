# 字段结构 (field_schema)

> 每类信息的标准化字段定义

---

## 通用字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| region_code | string | Y | 行政区划代码(6位) |
| region_name | string | Y | 地区名称 |
| admin_level | enum | Y | 省级/地级/县级 |
| investor_body | string | Y | 履行出资人职责机构名称 |
| investor_body_type | enum | Y | 国资委/财政局/国资中心/其他 |
| data_year | int | Y | 数据所属年份 |
| source_url | string | N | 数据来源URL |
| source_type | enum | Y | A~F类信息源 |
| collect_date | date | Y | 采集日期 |

---

## 信息源注册字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| source_id | string | Y | 信息源编号（REG-NNN） |
| institution_type | enum | Y | S1~S8 机构类型代码 |
| institution_name | string | Y | 机构全称 |
| admin_level | enum | Y | L1/L2/L3 |
| url | string | Y | 官网首页URL |
| part_coverage | array | Y | 覆盖的Part编号(1~4)及适配度(★★★/★★/★/○) |
| column_mapping | object | N | 栏目名称到Part的映射 |
| verified_date | date | N | 最后一次人工验证日期 |
| access_status | enum | Y | 可访问/需VPN/已失效 |
| notes | string | N | 特殊情况备注 |

---

## Part 1 字段: 监管企业名单

### 1.1 名单级字段（一个地区一条记录）

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| region_code | string | Y | 6位行政区划代码 |
| region_name | string | Y | 地区名称 |
| admin_level | enum(L1/L2/L3) | Y | 行政层级 |
| investor_body | string | Y | 出资人机构全称 |
| investor_body_type | enum(S1~S8) | Y | 机构类型 |
| caliber | enum(①~⑥) | Y | 名单口径编号（参见 part_playbooks C1） |
| caliber_label | string | Y | 口径中文标签（如"监管企业名单"/"出资企业名录"） |
| total_count_claimed | int | N | 官方声明的企业总数（如有） |
| total_count_extracted | int | Y | 实际抽取到的企业数量 |
| list_completeness | enum | Y | 完整/部分/推断/仅数量 |
| page_pattern | enum(LIST-A~F) | Y | 页面模式 |
| source_url | string | Y | 名单页面/文件URL |
| source_type_code | enum(S1~S8) | Y | 信息源机构类型 |
| publish_date | date | Y | 页面发布日期 |
| effective_date | date | N | 数据截至日期 |
| has_dual_category | bool | Y | 是否存在双分类（监管+双管） |
| extraction_method | enum | Y | 导航/搜索/推断/附件 |
| collect_date | date | Y | 采集日期 |
| notes | string | N | 备注 |

### 1.2 企业级字段（每个企业一条记录）

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| region_code | string | Y | 归属地区代码 |
| enterprise_name | string | Y | 企业全称 |
| enterprise_short_name | string | N | 简称 |
| enterprise_tier | enum | Y | 一级企业/二级企业/三级及以下/不明 |
| ownership_level | enum | Y | 省属/市属/县属/区属 |
| supervision_type | enum | Y | 监管企业/双管企业/委托监管/参股企业 |
| is_supervised | bool | Y | 是否纳入监管名单 |
| is_invested | bool | Y | 是否为直接出资企业 |
| industry_category | string | N | 所属行业（如有） |
| functional_type | string | N | 功能分类（商业一类/商业二类/公益类，如有） |
| enterprise_url | string | N | 企业详情页URL（来自名单页的链接） |
| evidence_snippet | string | Y | 原文证据片段（≤200字） |
| source_url | string | Y | 提取该企业信息的具体页面URL |
| caliber | enum(①~⑥) | Y | 继承自名单级 |
| publish_date | date | Y | 继承自名单级 |

### 1.3 示例数据

**名单级示例**:
```json
{
  "region_code": "110000",
  "region_name": "北京市",
  "admin_level": "L1",
  "investor_body": "北京市人民政府国有资产监督管理委员会",
  "investor_body_type": "S1",
  "caliber": "①",
  "caliber_label": "监管企业名单",
  "total_count_claimed": null,
  "total_count_extracted": 30,
  "list_completeness": "完整",
  "page_pattern": "LIST-F",
  "source_url": "https://gzw.beijing.gov.cn/yggq/jgqy/",
  "source_type_code": "S1",
  "publish_date": "2021-06-17",
  "effective_date": null,
  "has_dual_category": true,
  "extraction_method": "导航",
  "collect_date": "2026-04-02",
  "notes": "共3页约30家监管企业；另有3页约30家双管企业（央企驻京单位）"
}
```

**企业级示例**:
```json
{
  "region_code": "110000",
  "enterprise_name": "首钢集团有限公司",
  "enterprise_short_name": "首钢",
  "enterprise_tier": "一级企业",
  "ownership_level": "市属",
  "supervision_type": "监管企业",
  "is_supervised": true,
  "is_invested": true,
  "industry_category": "钢铁/综合",
  "functional_type": null,
  "enterprise_url": "https://gzw.beijing.gov.cn/yggq/jgqy/201812/t20181220_9792.html",
  "evidence_snippet": "首钢始建于1919年，迄今已有超过100年的历史。已经成为一家跨行业、跨地区、跨所有制、跨国经营的综合性大型企业集团，是世界五百强企业。",
  "source_url": "https://gzw.beijing.gov.cn/yggq/jgqy/",
  "caliber": "①",
  "publish_date": "2021-06-17"
}
```

## Part 2 字段: 月度/年度运行

### 2.1 运行数据集级字段（一期一地区一条记录）

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| region_code | string | Y | 6位行政区划代码 |
| region_name | string | Y | 地区名称 |
| admin_level | enum(L1/L2/L3) | Y | 行政层级 |
| investor_body | string | Y | 出资人机构全称 |
| investor_body_type | enum(S1~S8) | Y | 机构类型 |
| caliber | enum(P2-①~④) | Y | 数据口径编号 |
| caliber_label | string | Y | 口径标签（如"省属企业"/"全口径"） |
| period_year | int | Y | 数据年份 |
| period_start_month | int | Y | 期间起始月（累计型始终=1） |
| period_end_month | int | Y | 期间截止月 |
| period_type | enum | Y | 累计/单月/年度 |
| period_label | string | Y | 期间原文表达（如"1-2月"/"全年"） |
| data_source_label | string | N | 数据来源标签（如"据财务快报统计"） |
| is_preliminary | bool | Y | 是否为快报/初步数据(true) or 决算数据(false) |
| content_format | enum(RUN-A~E) | Y | 内容格式模式 |
| source_url | string | Y | 来源页面URL |
| source_type_code | enum(S1~S8) | Y | 信息源机构类型 |
| original_publisher | string | N | 原始发布者（如为转载则填原发布机构） |
| publish_date | date | Y | 页面发布日期 |
| collect_date | date | Y | 采集日期 |
| indicator_count | int | Y | 本次抽取到的指标数量 |
| has_absolute_values | bool | Y | 是否包含绝对值数据 |
| has_yoy_only | bool | Y | 是否存在"仅有同比无绝对值"的指标 |
| fallback_used | bool | Y | 是否使用了回退链获取 |
| notes | string | N | 特殊说明 |

### 2.2 指标级字段（每个指标一条记录）

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| region_code | string | Y | 归属地区代码 |
| period_label | string | Y | 继承自数据集 |
| indicator_name | string | Y | 指标标准名称（标准化后） |
| indicator_name_raw | string | Y | 指标原文名称（原始表述） |
| indicator_tier | enum(T1/T2/T3/T4) | Y | 指标层级（核心/标准/扩展/地方自定义） |
| value | decimal | N | 绝对值数值（如有） |
| unit | string | N | 数值单位（亿元/万元/%/个百分点） |
| is_approximate | bool | N | 是否为约数（"约XXX亿"） |
| value_type | enum | Y | 流量(累计)/时点(期末) |
| yoy_direction | enum(+/-/0/null) | N | 同比方向 |
| yoy_pct | decimal | N | 同比变化百分比 |
| yoy_bp | decimal | N | 同比变化百分点(资产负债率等百分比指标用) |
| yoy_adjusted | bool | N | 是否为调整后同比（如"剔除政策性因素后"） |
| yoy_adjustment_note | string | N | 调整说明原文 |
| mom_direction | enum(+/-/0/null) | N | 环比方向(如有) |
| mom_pct | decimal | N | 环比变化百分比 |
| evidence_snippet | string | Y | 原文证据片段（≤200字） |
| source_url | string | Y | 具体页面URL |
| caliber | enum(P2-①~④) | Y | 继承自数据集 |
| publish_date | date | Y | 继承自数据集 |

### 2.3 指标标准化映射表

| 标准名称 | 原文变体 | 层级 | value_type | 备注 |
|----------|----------|------|------------|------|
| 营业总收入 | 营业收入、营收、主营业务收入 | T1 | 流量 | 浙江用"营业收入"非"营业总收入" |
| 利润总额 | 利润、税前利润 | T1 | 流量 | ≠净利润 |
| 资产总额 | 总资产、资产规模 | T1 | 时点 | "截至X月末" |
| 资产负债率 | 负债率 | T1 | 时点 | 百分比，同比用百分点 |
| 应交税费 | 已交税费、上缴税费、税费总额 | T2 | 流量 | 应交≈已交(近似) |
| 负债总额 | 总负债 | T2 | 时点 | 可由资产总额×资产负债率推算 |
| 成本费用总额 | 成本费用、营业成本 | T2 | 流量 | 较少公开 |
| 工业总产值 | 工业产值 | T3 | 流量 | 仅限有工业企业的地区 |
| 固定资产投资 | 完成投资、投资额 | T3 | 流量 | |
| 研发投入 | R&D投入、研发费用 | T3 | 流量 | |
| 研发投入强度 | 研发强度 | T3 | 时点 | 百分比=研发投入/营收 |
| 净资产收益率 | ROE | T3 | 时点 | |
| 全员劳动生产率 | 劳动生产率 | T3 | 时点 | 万元/人 |
| 战略性新兴产业收入 | 战新产业收入 | T4 | 流量 | 甘肃等地方特色 |

### 2.4 示例数据

**数据集级示例（浙江省）**:
```json
{
  "region_code": "330000",
  "region_name": "浙江省",
  "admin_level": "L1",
  "investor_body": "浙江省人民政府国有资产监督管理委员会",
  "investor_body_type": "S1",
  "caliber": "P2-①",
  "caliber_label": "省属企业",
  "period_year": 2026,
  "period_start_month": 1,
  "period_end_month": 2,
  "period_type": "累计",
  "period_label": "1-2月",
  "data_source_label": "据财务快报统计",
  "is_preliminary": true,
  "content_format": "RUN-A",
  "source_url": "https://gzw.zj.gov.cn/col/col1229430932/art/2026/art_b126dbbfd174410e94c13b41b3e189b4.html",
  "source_type_code": "S1",
  "original_publisher": null,
  "publish_date": "2026-03-18",
  "collect_date": "2026-04-02",
  "indicator_count": 3,
  "has_absolute_values": true,
  "has_yoy_only": false,
  "fallback_used": false,
  "notes": "同一篇含1月单月和1-2月累计两组数据；利润有'剔除政策性因素后'同比"
}
```

**指标级示例**:
```json
[
  {
    "region_code": "330000",
    "period_label": "1-2月",
    "indicator_name": "营业总收入",
    "indicator_name_raw": "营业收入",
    "indicator_tier": "T1",
    "value": 2399.1,
    "unit": "亿元",
    "is_approximate": false,
    "value_type": "流量",
    "yoy_direction": "+",
    "yoy_pct": 2.2,
    "yoy_bp": null,
    "yoy_adjusted": false,
    "evidence_snippet": "据财务快报统计，1-2月份省属企业实现营业收入2,399.1亿元，同比增长2.2%"
  },
  {
    "region_code": "330000",
    "period_label": "1-2月",
    "indicator_name": "利润总额",
    "indicator_name_raw": "利润总额",
    "indicator_tier": "T1",
    "value": 65.9,
    "unit": "亿元",
    "is_approximate": false,
    "value_type": "流量",
    "yoy_direction": "+",
    "yoy_pct": 8.6,
    "yoy_bp": null,
    "yoy_adjusted": true,
    "yoy_adjustment_note": "剔除政策性因素后",
    "evidence_snippet": "实现利润总额65.9亿元，剔除政策性因素后同比增长8.6%"
  },
  {
    "region_code": "330000",
    "period_label": "截至2月底",
    "indicator_name": "资产总额",
    "indicator_name_raw": "资产总额",
    "indicator_tier": "T1",
    "value": 27645.8,
    "unit": "亿元",
    "is_approximate": false,
    "value_type": "时点",
    "yoy_direction": "+",
    "yoy_pct": 9.7,
    "yoy_bp": null,
    "yoy_adjusted": false,
    "evidence_snippet": "截至2月底，省属企业资产总额为27,645.8亿元，同比增长9.7%"
  }
]
```

## Part 3 字段: 重组/基金/主责主业

### 3A. 重组事件字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| event_id | string | Y | 事件唯一标识(RG-{region}-{seq}) |
| region_code | string | Y | 行政区划代码 |
| region_name | string | Y | 地区名称 |
| restructure_type | enum | Y | RG-01~RG-06 (见类型分类) |
| entity_a | string | Y | 主体企业A(存续/主导方) |
| entity_b | string | Y | 被重组/整合方B |
| entity_new | string | N | 新设企业名称(RG-02/RG-03时填) |
| sector | string | N | 涉及板块(专业化整合时填) |
| is_strategic | bool | Y | 是否战略性重组 |
| is_admin_transfer | bool | Y | 是否行政划转(vs市场化交易) |
| approval_body | string | N | 审批主体(国务院/省政府/市政府) |
| approval_doc | string | N | 批复文件编号 |
| announce_date | date | Y | 公告/发布日期 |
| effective_date | date | N | 生效日期(如有) |
| removed_from_list | bool | N | 被重组方是否从监管名单移出 |
| evidence_level | enum | Y | EV-A1~EV-A5 |
| evidence_snippet | string | Y | 原文引用(≤200字) |
| source_url | string | Y | 来源链接 |
| source_institution | string | Y | 发布机构 |
| confidence | float | Y | 置信度(0~1) |

### 3B. 基金字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| fund_id | string | Y | 基金唯一标识(FD-{region}-{seq}) |
| region_code | string | Y | 行政区划代码 |
| region_name | string | Y | 地区名称 |
| fund_name | string | Y | 基金名称 |
| fund_type | enum | Y | FD-01~FD-05 (见类型分类) |
| fund_size | string | N | 基金规模(含单位) |
| fund_size_value | float | N | 规模数值(统一为亿元) |
| investor_list | array | N | 出资主体列表 |
| manager | string | N | 管理主体/管理人 |
| is_soe_led | enum | Y | true/false/"参与但非主导" |
| is_reform_fund | bool | Y | 是否改革类基金 |
| duration_years | int | N | 存续期(年) |
| investment_focus | string | N | 投资方向/领域 |
| establish_date | date | N | 设立日期 |
| filing_number | string | N | 基金业协会备案号(如有) |
| evidence_level | enum | Y | EV-B1~EV-B5 |
| evidence_snippet | string | Y | 原文引用(≤200字) |
| source_url | string | Y | 来源链接 |
| source_institution | string | Y | 发布机构 |
| confidence | float | Y | 置信度(0~1) |

### 3C. 主责主业字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| mc_id | string | Y | 唯一标识(MC-{region}-{enterprise}-{seq}) |
| region_code | string | Y | 行政区划代码 |
| region_name | string | Y | 地区名称 |
| enterprise_name | string | Y | 企业名称 |
| mc_text | string | Y | 主责主业原文表述 |
| mc_level | enum | Y | MC-L1~MC-L4 (正式性等级) |
| functional_type | enum | N | 商业一类/商业二类/公益类/未分类 |
| is_list | bool | Y | 是否清单化表述 |
| has_adjustment | enum | Y | true/false/"可能" |
| adjustment_direction | string | N | 调整方向描述(新增/退出+领域) |
| source_doc_type | string | Y | 来源文件类型(批复/规划/报告/新闻) |
| source_doc_date | date | Y | 来源文件日期 |
| evidence_level | enum | Y | EV-C1~EV-C5 |
| evidence_snippet | string | Y | 原文引用(≤200字) |
| source_url | string | Y | 来源链接 |
| source_institution | string | Y | 发布机构 |
| confidence | float | Y | 置信度(0~1) |

### 3. JSON 示例

```json
{
  "restructuring_events": [
    {
      "event_id": "RG-000000-001",
      "region_code": "000000",
      "region_name": "全国(央企)",
      "restructure_type": "RG-01",
      "entity_a": "中国宝武钢铁集团有限公司",
      "entity_b": "中国中钢集团有限公司",
      "entity_new": null,
      "sector": null,
      "is_strategic": true,
      "is_admin_transfer": false,
      "approval_body": "国务院",
      "approval_doc": null,
      "announce_date": "2022-12-21",
      "effective_date": null,
      "removed_from_list": true,
      "evidence_level": "EV-A1",
      "evidence_snippet": "经报国务院批准，中国宝武钢铁集团有限公司与中国中钢集团有限公司实施重组，中国中钢集团有限公司整体划入中国宝武钢铁集团有限公司，不再作为国资委直接监管企业。",
      "source_url": "http://www.sasac.gov.cn/n2588030/n2588924/c26776957/content.html",
      "source_institution": "国务院国资委改革局",
      "confidence": 0.98
    }
  ],
  "funds": [
    {
      "fund_id": "FD-000000-001",
      "region_code": "000000",
      "region_name": "全国(央企)",
      "fund_name": "(政策框架-央企创业投资基金)",
      "fund_type": "FD-03",
      "fund_size": null,
      "fund_size_value": null,
      "investor_list": ["中央企业"],
      "manager": null,
      "is_soe_led": true,
      "is_reform_fund": false,
      "duration_years": 15,
      "investment_focus": "种子期/初创期/成长期硬科技企业",
      "establish_date": null,
      "filing_number": null,
      "evidence_level": "EV-B1",
      "evidence_snippet": "支持中央企业围绕主责主业，聚焦重大战略、重点领域、重要技术，发起设立概念验证基金、种子基金、天使基金等适应科技成果转化及科技创新企业成长所需的创业投资基金",
      "source_url": "http://www.sasac.gov.cn/n2588030/n2588929/c32259172/content.html",
      "source_institution": "国务院国资委资本局",
      "confidence": 0.85
    }
  ],
  "core_business": [
    {
      "mc_id": "MC-000000-CentralSOE-001",
      "region_code": "000000",
      "region_name": "全国(央企)",
      "enterprise_name": "(央企通用要求)",
      "mc_text": "围绕主责主业，聚焦重大战略、重点领域、重要技术",
      "mc_level": "MC-L3",
      "functional_type": "未分类",
      "is_list": false,
      "has_adjustment": false,
      "adjustment_direction": null,
      "source_doc_type": "政策文件",
      "source_doc_date": "2024-12-02",
      "evidence_level": "EV-C3",
      "evidence_snippet": "支持中央企业围绕主责主业，聚焦重大战略、重点领域、重要技术",
      "source_url": "http://www.sasac.gov.cn/n2588030/n2588929/c32259172/content.html",
      "source_institution": "国务院国资委资本局",
      "confidence": 0.70
    }
  ]
}
```

## Part 4 字段: 国资经营预算/资产报告

### §P4A 国有资本经营预算 字段

**预算数据集级** (每份预算文件一条记录):

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| budget_id | string | ✓ | 唯一标识: {region}_{year}_{type} |
| region | string | ✓ | 行政区划(省/市/县名) |
| admin_level | enum | ✓ | L1省/L2地市/L3县区/L0中央 |
| budget_year | int | ✓ | 预算年度(如2026) |
| doc_type | enum | ✓ | budget_table/budget_explanation/budget_report/settlement |
| budget_phase | enum | ✓ | draft(草案)/approved(批准)/execution(执行)/settlement(决算) |
| scope | enum | ✓ | own_level(本级)/consolidated(全辖区)/national_total |
| includes_financial | bool | ✓ | 是否含金融企业 |
| total_revenue | float | △ | 收入总额(亿元) |
| total_expenditure | float | △ | 支出总额(亿元) |
| transfer_out | float | △ | 调入一般公共预算金额(亿元) |
| carryover_in | float | | 上年结转收入(亿元) |
| revenue_total_with_carryover | float | | 收入总量(含结转) |
| yoy_revenue | string | | 收入同比(如"增长25.8%") |
| yoy_expenditure | string | | 支出同比 |
| revenue_by_category | array | | 分类收入明细(见下方) |
| expenditure_by_category | array | | 分类支出明细(见下方) |
| budget_scope_enterprises | string | | 纳入预算编制范围的企业描述 |
| profit_collection_ratios | string | | 利润收取比例说明 |
| source_url | string | ✓ | 来源URL |
| source_institution | string | ✓ | 发布机构 |
| publish_date | date | ✓ | 发布日期 |
| evidence_snippet | string | ✓ | 原文依据(200字内) |
| confidence | float | ✓ | 0~1 |

**收入分类明细** (revenue_by_category 元素):

| 字段 | 类型 | 说明 |
|------|------|------|
| category | string | 收入类别(利润收入/股息红利/产权转让/清算/其他) |
| sub_category | string | 子类(如"烟草企业利润收入") |
| amount | float | 金额(亿元) |
| prev_year_amount | float | 上年执行数 |
| yoy_pct | float | 预算数为上年执行数的% |

**支出分类明细** (expenditure_by_category 元素):

| 字段 | 类型 | 说明 |
|------|------|------|
| category | string | 支出类别(历史遗留/资本金注入/公益性补贴/转移支付) |
| amount | float | 金额(亿元) |
| prev_year_amount | float | 上年执行数 |
| yoy_change | string | 同比变化说明 |

**JSON示例 (2026年中央国有资本经营预算)**:
```json
{
  "budget_id": "central_2026_budget",
  "region": "中央",
  "admin_level": "L0",
  "budget_year": 2026,
  "doc_type": "budget_explanation",
  "budget_phase": "draft",
  "scope": "own_level",
  "includes_financial": false,
  "total_revenue": 3716.32,
  "total_expenditure": 1476.23,
  "transfer_out": 2500.00,
  "carryover_in": 259.91,
  "revenue_total_with_carryover": 3976.23,
  "yoy_revenue": "下降4.8%",
  "yoy_expenditure": "增长13.8%",
  "revenue_by_category": [
    {"category": "利润收入", "amount": 3522.33, "prev_year_amount": 3750.77, "yoy_pct": 93.9},
    {"category": "股息红利收入", "amount": 193.99, "prev_year_amount": 150.90, "yoy_pct": 128.6},
    {"category": "产权转让收入", "amount": null, "prev_year_amount": 0.02},
    {"category": "清算收入", "amount": null, "prev_year_amount": 0.87},
    {"category": "其他", "amount": null, "prev_year_amount": 0.18}
  ],
  "expenditure_by_category": [
    {"category": "解决历史遗留问题及改革成本支出", "amount": 39.39, "yoy_change": "下降10.9%"},
    {"category": "国有企业资本金注入", "amount": 766.17, "yoy_change": "增长56.6%"},
    {"category": "国有企业公益性补贴", "amount": 636.89, "yoy_change": "下降11.8%"},
    {"category": "中央对地方转移支付", "amount": 33.78, "yoy_change": "下降0.2%"}
  ],
  "profit_collection_ratios": "第一类35%(烟草石油等资源型);第二类30%(一般竞争型);第三类(军工科研);第四类(政策性)",
  "budget_scope_enterprises": "国资委监管100户+所属144户;教育部141户;...共计多部门",
  "source_url": "http://yss.mof.gov.cn/2026zyczys/202603/t20260324_3985993.htm",
  "source_institution": "财政部预算司",
  "publish_date": "2026-03-24",
  "evidence_snippet": "2026年中央国有资本经营收入预算数为3716.32亿元...支出预算数为1476.23亿元...调出资金预算数为2500亿元",
  "confidence": 0.98
}
```

### §P4B 国有资产管理情况报告 字段

**报告级** (每份报告一条记录):

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| report_id | string | ✓ | 唯一标识: {region}_{year}_{report_type} |
| region | string | ✓ | 行政区划 |
| admin_level | enum | ✓ | L0中央/L1省/L2地市/L3县区 |
| report_year | int | ✓ | 报告覆盖年度(如2024) |
| report_type | enum | ✓ | comprehensive(综合)/special(专项) |
| special_type | enum | | enterprise/financial/administrative/natural_resource |
| excludes_financial | bool | | 专项报告是否"不含金融企业" |
| doc_version | enum | ✓ | full_text/npc_published/review_opinion/news_summary/audit_ref |
| presenter | string | | 报告人(如"财政部副部长XX") |
| review_session | string | | 审议会议(如"十四届全国人大常委会第十八次会议") |
| covers_enterprise | bool | ✓ | 是否覆盖企业国有资产 |
| enterprise_data | object | | 企业国有资产关键数据(见下方) |
| financial_data | object | | 金融企业国有资产数据 |
| admin_data | object | | 行政事业性国有资产数据 |
| natural_resource_data | object | | 自然资源(资产)数据 |
| problem_statements | array | | 问题表述列表 |
| reform_directions | array | | 整改/改革方向列表 |
| source_url | string | ✓ | 来源URL |
| source_institution | string | ✓ | 发布机构 |
| publish_date | date | ✓ | 发布日期 |
| evidence_snippet | string | ✓ | 原文摘录依据 |
| confidence | float | ✓ | 0~1 |

**企业国有资产数据** (enterprise_data 结构):

| 字段 | 类型 | 说明 |
|------|------|------|
| total_assets | float | 资产总额(万亿元) |
| total_liabilities | float | 负债总额(万亿元) |
| owners_equity | float | 国有资本权益/所有者权益(万亿元) |
| asset_liability_ratio | float | 资产负债率(%) |
| total_revenue | float | 营业总收入(万亿元) |
| total_profit | float | 利润总额(亿元) |
| capital_preservation_rate | float | 国有资本保值增值率(%) |
| enterprise_count | int | 企业户数 |
| scope_description | string | 口径说明(如"不含金融企业") |
| data_cutoff_date | string | 数据截止日期 |

**JSON示例 (2024年度综合报告 - 审议意见)**:
```json
{
  "report_id": "central_2024_comprehensive",
  "region": "全国",
  "admin_level": "L0",
  "report_year": 2024,
  "report_type": "comprehensive",
  "special_type": null,
  "doc_version": "review_opinion",
  "presenter": null,
  "review_session": "十四届全国人大常委会第十八次会议",
  "covers_enterprise": true,
  "enterprise_data": {
    "scope_description": "综合报告企业部分"
  },
  "problem_statements": ["(需从审议意见全文提取)"],
  "reform_directions": ["(需从审议意见全文提取)"],
  "source_url": "http://www.npc.gov.cn/npc/c2/c30834/202602/t20260224_451606.html",
  "source_institution": "全国人大常委会",
  "publish_date": "2026-02-24",
  "evidence_snippet": "十四届全国人大常委会第十八次会议审议了国务院关于2024年度国有资产管理情况的综合报告和财政部副部长郭婷婷受国务院委托作的关于2024年度企业国有资产(不含金融企业)管理情况的专项报告",
  "confidence": 0.85
}
```

---

## v2 统一公共字段 (2026-04-02)

> 统一校验后新增/修订的全局公共字段，解决 7 处跨Part冲突。

### 新增/修订通用字段

| 字段名 | 类型 | 必填 | v2操作 | 说明 |
|--------|------|:---:|--------|------|
| caliber_domain | enum | Y | **新增(C-01)** | 口径所属领域: list/operation/restructuring/fund/core_business/budget/report |
| source_institution | string | Y | **补充到P1/P2** | 发布机构全称(P3/P4已有, P1/P2缺失) |
| confidence | float | Y | **补充到P1/P2** | 0~1置信度(P3/P4已有, P1/P2缺失→now全Part必填) |
| evidence_level | enum(UEV-1~5) | Y | **新增(C-07)** | 统一5级证据等级; 替代P3的EV-A/B/C分立体系 |
| doc_version | enum(LV-1~5) | N | **推广到全Part** | 版本层次(P4已定义→now全Part可用) |

### P1补充字段（v2新增）

P1名单级和企业级需追加:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| confidence | float | Y | P1的置信度计算: LIST-A完整=0.90; LIST-B推断=0.55; LIST-E仅数量=0.35 |
| evidence_level | enum | Y | UEV-1(含文号名单) / UEV-2(官网栏目) / UEV-4(推断/拼凑) |
| source_institution | string | Y | 如"北京市人民政府国有资产监督管理委员会" |
| caliber_domain | enum | Y | 固定为 "list" |

### P2补充字段（v2新增）

P2数据集级需追加:

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| confidence | float | Y | RUN-A=0.90; RUN-B=0.70; RUN-D=0.55; RUN-E=0.30 |
| evidence_level | enum | Y | UEV-2(官方统计) / UEV-3(新闻通稿) / UEV-4(工作报告摘录) |
| source_institution | string | Y | P2原有original_publisher可选→now合并, 取原始发布者 |
| caliber_domain | enum | Y | 固定为 "operation" |

### P3字段映射（v2修订）

| v1字段 | v2统一字段 | 处理 |
|--------|-----------|------|
| announce_date(P3A) | publish_date | **重命名(C-02)**: 统一日期字段名 |
| evidence_level: EV-A1~A5 | evidence_level: UEV-1~5 | **映射(C-07)**: EV-A1→UEV-1, EV-A2→UEV-1, EV-A3→UEV-3, EV-A4→UEV-4, EV-A5→UEV-5 |
| evidence_level: EV-B1~B5 | evidence_level: UEV-1~5 | **映射**: EV-B1→UEV-2, EV-B2→UEV-1, EV-B3→UEV-3, EV-B4→UEV-2, EV-B5→UEV-3 |
| evidence_level: EV-C1~C5 | evidence_level: UEV-1~5 | **映射**: EV-C1→UEV-1, EV-C2→UEV-1, EV-C3→UEV-3, EV-C4→UEV-3, EV-C5→UEV-5 |
| (无变化) | caliber_domain | **新增**: P3A="restructuring", P3B="fund", P3C="core_business" |

### P4字段映射（v2修订）

| v1字段 | v2统一字段 | 处理 |
|--------|-----------|------|
| doc_version(P4B) | doc_version(全Part) | 无变化, 但现在允许P4A也使用 |
| (无变化) | evidence_level | **新增**: P4A BUD-T1/T2=UEV-1, BUD-T3/T4=UEV-2, 报告摘要=UEV-4 |
| (无变化) | caliber_domain | **新增**: P4A="budget", P4B="report" |

### v2 统一输出骨架 JSON Schema

```json
{
  "$schema": "guozi_output_v2",
  "$comment": "所有Part的输出遵循此骨架, data字段按Part扩展",
  "required_blocks": ["_meta", "_quality", "_source", "data"],
  "_meta": {
    "task_id": "string (region_part_timestamp)",
    "region_code": "string (6位)",
    "region_name": "string",
    "admin_level": "enum(L1/L2/L3)",
    "part": "enum(P1/P2/P3A/P3B/P3C/P4A/P4B)",
    "collect_date": "date"
  },
  "_quality": {
    "confidence": "float 0~1",
    "evidence_level": "enum(UEV-1~5)",
    "completeness": "enum(完整/部分/推断/仅数量)",
    "fallback_used": "bool",
    "warnings": "array[string]"
  },
  "_source": {
    "source_url": "string",
    "source_type_code": "enum(S1~S8)",
    "source_institution": "string",
    "publish_date": "date",
    "doc_version": "enum(LV-1~5) optional",
    "is_repost": "bool",
    "evidence_snippet": "string ≤200字"
  },
  "data": {
    "caliber_domain": "enum(list/operation/restructuring/fund/core_business/budget/report)",
    "caliber_label": "string (口径中文标签)",
    "$part_specific_fields": "..."
  }
}
```
