# 模块 A：地方国有企业主体名单表 — Schema 说明

> 生成日期: 2026-04-02
> 版本: v1.0
> 适用文件: `guozi_entity_list.csv` / `.xlsx`

---

## 1. 字段定义

| # | 字段名 | 类型 | 必填 | 说明 |
|---|--------|------|------|------|
| 1 | `entity_id` | string | Y | 唯一标识，格式 `E-{province_code}-{seq:04d}`，如 `E-GD-0001` |
| 2 | `province` | string | Y | 省/自治区/直辖市名称（简称），如"广东""浙江" |
| 3 | `province_code` | string | Y | 省份代码（2位大写字母），如 GD/ZJ/SD/SC |
| 4 | `admin_level` | enum | Y | `L1`=省级, `L2`=地市级, `L3`=县区级 |
| 5 | `city` | string | N | 地级市名称（L1级为空；L2/L3级必填） |
| 6 | `entity_name_full` | string | Y | 企业全称（含"有限公司"等法定后缀） |
| 7 | `entity_name_short` | string | N | 企业简称（如"交通集团"） |
| 8 | `list_caliber` | enum | Y | 名单口径类型（见§2） |
| 9 | `list_caliber_label` | string | Y | 口径说明文字（如"省国资委监管企业"） |
| 10 | `source_institution` | string | Y | 信息来源机构（如"广东省国资委"） |
| 11 | `source_url` | string | Y | 来源页面URL |
| 12 | `source_page_type` | enum | Y | 页面模式(§3) |
| 13 | `extraction_date` | date | Y | 采集日期 YYYY-MM-DD |
| 14 | `list_publish_date` | date | N | 名单公布/更新日期（可考证时填写） |
| 15 | `sector` | string | N | 所属行业/领域（如"能源""交通""金融"） |
| 16 | `includes_financial` | bool | N | 是否含金融类企业 |
| 17 | `completeness` | enum | Y | 完整性判定(§4) |
| 18 | `confidence` | float | Y | 置信度 0.0~1.0 |
| 19 | `uev_level` | int | Y | 统一证据等级 1(最高)~5(最低) |
| 20 | `needs_manual_review` | bool | Y | 是否需要人工复核 |
| 21 | `notes` | string | N | 备注（口径差异、特殊情况等） |

## 2. 名单口径类型 (`list_caliber`)

| 值 | 含义 | 说明 |
|----|------|------|
| `supervised` | 监管企业名单 | 国资委直接监管/出资的一级企业集团（最窄口径） |
| `invested` | 所出资企业名单 | 国资委履行出资人职责的企业（基本等同 supervised） |
| `identifiable` | 公开可识别的国企主体 | 从官网链接、新闻、招聘等间接识别（非正式名单） |
| `budget_scope` | 纳入预算管理范围 | 纳入国有资本经营预算的企业（可能宽于 supervised） |
| `statistical` | 统计口径 | 财政部/统计局"国有及国有控股企业"全口径（最宽） |
| `unknown` | 口径不明 | 来源未明确说明口径类型 |

### ⚠️ 口径警示
- **`supervised` ≠ 全部国有企业**：监管企业通常仅10~40户（一级集团），而同省"国有及国有控股企业"可达数百~数千户
- **`identifiable`** 必然不完整，置信度应降级
- **不同口径数据不得直接混合比较**

## 3. 页面模式 (`source_page_type`)

| 值 | 含义 | 采集可靠性 |
|----|------|-----------|
| `LIST-A` | 独立名单表格页（含企业全称+编号列表） | 最高 |
| `LIST-B` | 无独立名单页，从统计信息/公告间接获取 | 中 |
| `LIST-C` | 政府信息公开目录中的附件(PDF/Excel) | 高（但需下载） |
| `LIST-D` | 年度工作报告中的附表 | 中高 |
| `LIST-E` | 企业改革/布局文件中的企业列表 | 中 |
| `LIST-F` | 首页"监管企业"栏目链接提取 | 中高 |
| `NEWS` | 从新闻/招聘/动态间接识别 | 低 |

## 4. 完整性判定 (`completeness`)

| 值 | 含义 |
|----|------|
| `full_list` | 完整公示名单（官方发布，可作为权威参考） |
| `partial_identified` | 仅识别部分主体（无完整名单来源） |
| `no_public_list` | 该地区未公开明确名单 |
| `needs_verification` | 有名单但日期较旧或来源可信度不足，需人工复核 |

## 5. 文件导出说明

- **CSV**: UTF-8-BOM 编码，逗号分隔，字符串字段用双引号
- **XLSX**: 第一行为表头，冻结首行，列宽自适应
- **推荐文件名**: `guozi_entity_list_v1_20260402.csv`
