# 模块 B：国有企业经营情况月度数据集 — Schema 说明

> 生成日期: 2026-04-02
> 版本: v1.0
> 适用文件: `guozi_monthly_operation_v1_20260402.csv` → 可转为 `.dta`

---

## 1. 字段定义

| # | 字段名 | Stata类型 | 必填 | 说明 |
|---|--------|-----------|------|------|
| 1 | `record_id` | str20 | Y | 唯一标识 `MO-{scope_code}-{period}` |
| 2 | `province` | str20 | Y | 省份名称（"全国"表示全国汇总） |
| 3 | `province_code` | str4 | Y | 省份代码（CN=全国, GD/ZJ/...） |
| 4 | `scope` | str30 | Y | 统计口径(§2) |
| 5 | `scope_code` | str3 | Y | 口径代码(§2) |
| 6 | `period_type` | str10 | Y | `cumulative`=累计, `single_month`=单月, `annual`=全年 |
| 7 | `year` | int | Y | 数据年份 |
| 8 | `month_start` | int | Y | 起始月(含), 累计型通常=1 |
| 9 | `month_end` | int | Y | 截止月(含) |
| 10 | `period_label` | str30 | Y | 原始期间表述(如"1-2月""1-12月") |
| 11 | `indicator_name` | str40 | Y | 指标名称(标准化后) |
| 12 | `indicator_name_raw` | str60 | N | 原始指标名称(来源原文) |
| 13 | `value` | double | N | 数值(统一为亿元; 无绝对值时为缺失) |
| 14 | `unit` | str10 | Y | 单位: `亿元` / `%` / `百分点` |
| 15 | `yoy_pct` | double | N | 同比增长率(%, 如 0.2 表示增长0.2%) |
| 16 | `yoy_direction` | str4 | N | `up`=增长, `down`=下降, `flat`=持平 |
| 17 | `is_cumulative` | byte | Y | 1=累计数据, 0=单月/时点数据 |
| 18 | `is_stock` | byte | Y | 1=时点(存量)数据(如资产总额), 0=流量数据 |
| 19 | `is_preliminary` | byte | Y | 1=财务快报(初步), 0=正式/决算 |
| 20 | `includes_financial` | byte | Y | 1=含金融企业, 0=不含 |
| 21 | `source_institution` | str40 | Y | 发布主体 |
| 22 | `source_title` | str100 | Y | 来源文件标题 |
| 23 | `source_url` | str200 | Y | 来源URL |
| 24 | `publish_date` | str10 | Y | 发布日期 YYYY-MM-DD |
| 25 | `extraction_date` | str10 | Y | 采集日期 |
| 26 | `confidence` | float | Y | 置信度 0.0~1.0 |
| 27 | `uev_level` | byte | Y | 证据等级 1~5 |
| 28 | `notes` | str200 | N | 备注 |

## 2. 统计口径 (`scope` / `scope_code`)

| scope_code | scope | 说明 | 企业范围 |
|-----------|-------|------|---------|
| `A1` | 全国国有及国有控股企业 | 财政部月报标准口径 | 中央企业+36省地方国企+兵团, **不含一级金融** |
| `B1` | 省属监管企业 | 省国资委直接监管企业 | 仅省国资委出资的一级集团 |
| `B2` | 省属企业(含直属) | 省属全口径 | 省级直属+省国资委监管 |
| `C1` | 全省国有及国有控股企业 | 省级全口径 | 含市县国企,通常由财政厅编报 |
| `D1` | 市属监管企业 | 地市国资委口径 | 仅市级一级集团 |
| `X` | 口径不明 | 来源未明确说明 | 需人工判定 |

### ⚠️ 口径警示
- **A1 ≠ B1**: 全国口径(A1)含全部地方国企数千户, 省属监管口径(B1)通常仅10~40户集团
- **A1 不含一级金融企业**: 明确排除
- **B1 vs C1**: 差异可达数倍（省属15家 vs 全省800家）
- **不同口径数据不得直接混合、加总或比较同比增速**

## 3. 标准化指标体系

| 层级 | indicator_name (标准化) | 常见原始名 | 单位 | 流量/存量 |
|------|------------------------|-----------|------|----------|
| T1核心 | 营业总收入 | 营业总收入/营业收入 | 亿元 | 流量 |
| T1核心 | 利润总额 | 利润总额 | 亿元 | 流量 |
| T1核心 | 应交税费 | 应交税费/应交税金 | 亿元 | 流量 |
| T1核心 | 资产负债率 | 资产负债率 | % | 时点 |
| T2常见 | 资产总额 | 资产总额/总资产 | 亿元 | 时点 |
| T2常见 | 净利润 | 净利润 | 亿元 | 流量 |
| T3扩展 | 成本费用利润率 | 成本费用利润率 | % | 流量 |
| T3扩展 | 工业总产值 | 工业总产值 | 亿元 | 流量 |
| T4地方 | (地方特有指标) | varies | varies | varies |

### 指标名称映射规则
| 原始名 | 标准化名 | 备注 |
|--------|---------|------|
| 营业收入 | 营业总收入 | 浙江等省用"营业收入",等价于财政部的"营业总收入" |
| 应交税金 | 应交税费 | 旧称 |
| 总资产 | 资产总额 | 同义 |
| 所有者权益 | 净资产 | 同义(非全资企业中与"国有资本权益"有差异) |

## 4. 期间识别规则

| 原始表述 | period_type | month_start | month_end | is_cumulative |
|---------|-------------|-------------|-----------|---------------|
| 1-2月 | cumulative | 1 | 2 | 1 |
| 1-12月 | annual | 1 | 12 | 1 |
| X月末 | single_month(时点) | X | X | 0 |
| 上半年 | cumulative | 1 | 6 | 1 |
| 前三季度 | cumulative | 1 | 9 | 1 |
| 全年 | annual | 1 | 12 | 1 |

### 特殊规则
- **1月不单独发布**: 最早为1-2月合并发布
- **单月数据**: 浙江同时发布单月(1月)和累计(1-2月), 需分拆为两条记录
- **"X月末"为时点**: 资产负债率等时点指标以"X月末"为截止日

## 5. .dta 转换说明

```stata
* 推荐导入命令
import delimited "guozi_monthly_operation_v1_20260402.csv", encoding(utf-8) clear

* 关键变量类型
destring value yoy_pct confidence, replace force
encode scope_code, gen(scope_code_n)
encode period_type, gen(period_type_n)

* 日期变量
gen publish_dt = date(publish_date, "YMD")
format publish_dt %td
```

## 6. 导出文件名
- CSV: `guozi_monthly_operation_v1_20260402.csv`
- DTA: `guozi_monthly_operation_v1_20260402.dta`
