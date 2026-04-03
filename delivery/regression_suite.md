# regression_suite — 回归测试套件

> 更新: 2026-04-02  
> 详细结果: E_regression_tests.md

## 测试矩阵

| 编号 | 模块 | 场景类型 | 输入描述 | 验证规则 | 结果 |
|------|------|---------|---------|---------|------|
| T-1.1 | A 名单 | 口径判定(监管+金融) | 广东 supervised 18 家 | caliber=supervised ∧ includes_financial=1 ∧ confidence≥0.80 | ✅ PASS |
| T-1.2 | A 名单 | 口径判定(identifiable低信度) | 山东 identifiable 7 家 | caliber=identifiable ∧ 0.50≤confidence≤0.65 ∧ source_page=NEWS | ✅ PASS |
| T-2.1 | B 月度 | 多期拆分 | 浙江 2026-01 单月 + 2026-01~02 累计 | 同一 source_url → 2 条记录 ∧ period_type 分别为 single/cumulative | ✅ PASS |
| T-2.2 | B 月度 | 调整同比 | 浙江利润总额 "剔除政策性因素后+8.6%" | yoy_adjusted=true ∧ unit_yoy_note≠空 | ✅ PASS |
| T-2.3 | B 月度 | 百分点消歧 | 全国 DAR 65.4% +0.5pp | value=65.4 ∧ yoy=0.5 ∧ unit=pct ∧ unit_yoy=pp | ✅ PASS |

## 覆盖率
- 口径判定: 2/6 caliber types tested (supervised, identifiable)
- 期间处理: 3/4 period scenarios tested (single, cumulative, annual)
- 指标类型: 4/4 core indicators tested (revenue, profit, tax, DAR)
- 特殊处理: adjusted_yoy, basis_point disambiguation

## 模块C 政策简报测试 (E_policy_regression_tests.md)

| 编号 | 模块 | 场景类型 | 输入描述 | 验证规则 | 结果 |
|------|------|---------|---------|---------|------|
| T-3.1 | C 政策 | 主题误检 | 品牌建设意见 | TOPIC-01排除词命中"品牌建设" | ✅ PASS |
| T-3.2 | C 政策 | 噪声排除 | 学习教育读书班新闻 | TOPIC-06全局噪声词命中3个 | ✅ PASS |
| T-3.3 | C 政策 | 文种分级 | 令第46号违规追责办法 | DOC-01→A级 | ✅ PASS |
| T-3.4 | C 政策 | 文种分级 | 福建五大行动 | DOC-03+LOCAL-01→C级 | ✅ PASS |
| T-3.5 | C 政策 | 文种分级 | 应急管理办法征求意见稿 | DOC-02→B级 | ✅ PASS |
| T-3.6 | C 政策 | 约束词识别 | 46号令正文"不得/禁入" | BIND-01→强制级 | ✅ PASS |

## 累计覆盖统计
- 模块A/B: 5 场景, 5/5 PASS
- 模块C: 6 场景, 6/6 PASS

## 模块D 预算规则测试 (F_budget_regression_tests.md)

| 编号 | 模块 | 场景类型 | 输入描述 | 验证规则 | 结果 |
|------|------|---------|---------|---------|------|
| T-4.1 | D 预算 | 比例提取 | 中央Tier1税后利润收取比例35% | BDG-01→RULE + BDG-02→L2来源 + ratio=35% | ✅ PASS |
| T-4.2 | D 预算 | 比例UNIDENTIFIED | 广东预算中无比例信息 | BTPL-02→UNIDENTIFIED + S4 | ✅ PASS |
| T-4.3 | D 预算 | 截断不推断 | Tier3文本截断 | BDG-03→校验失败 + 不填历史值 | ✅ PASS |
| T-4.4 | D 预算 | Scope消歧 | 预算草案"地方本级" | SCOPE-01/02→local_aggregate | ✅ PASS |
| T-4.5 | D 预算 | 转移支付≠本级 | 广东转移支付0.75亿 | SCOPE-03→TRANSFER≠budget_income | ✅ PASS |
| T-4.6 | D 预算 | 全国scope | 全国国资预算收入 | SCOPE-01→national + 标注合计 | ✅ PASS |
| T-4.7 | D 预算 | Record_type | 中央收入3716.32亿 | BDG-01→BUDGET_FIGURE | ✅ PASS |
| T-4.8 | D 预算 | Record_type | 收取比例30% | BDG-01→RULE | ✅ PASS |
| T-4.9 | D 预算 | 特殊条目 | 兵团体制性支出 | SPEC-01→兵团清单命中 | ✅ PASS |
| T-4.10 | D 预算 | 特殊条目 | 收入总量≠当年收入 | SPEC-02→分别记录 | ✅ PASS |

## 累计覆盖统计
- 模块A/B: 5 场景, 5/5 PASS
- 模块C: 6 场景, 6/6 PASS
- 模块D: 10 场景, 10/10 PASS
- **合计: 21 场景, 21/21 PASS**

## 模块E 网站展示层测试 (G_site_regression_tests.md)

| 编号 | 模块 | 场景类型 | 输入描述 | 验证规则 | 结果 |
|------|------|---------|---------|---------|------|
| T-5.1 | E 网站 | 字段映射 | 模块A(uev_level=2)+模块D(evidence_strength=S1) | UNIFY-01+EVLINK-02→统一渲染 | ✅ PASS |
| T-5.2 | E 网站 | 字段映射 | 模块A(GD)+模块D(guangdong) | UNIFY-02→识别不一致 | ✅ PASS |
| T-5.3 | E 网站 | 字段映射 | budget_rules含RULE+FIGURE+TRANSFER | API-02→正确拆分至栏目3/4 | ✅ PASS |
| T-5.4 | E 网站 | 证据回链 | BDG-F-001(S1+有URL) | EVLINK-01→4项完整+URL校验 | ✅ PASS |
| T-5.5 | E 网站 | 证据回链 | BDG-P-001(S4+无URL+UNIDENTIFIED) | EVLINK-03→空态处理 | ✅ PASS |
| T-5.6 | E 网站 | 图表组件 | 3指标×2年全国数据 | CHART-01→满足最小集 | ✅ PASS |
| T-5.7 | E 网站 | 图表组件 | 筛选后0条数据 | CHART-02→降级处理 | ✅ PASS |

## 累计覆盖统计
- 模块A/B: 5 场景, 5/5 PASS
- 模块C: 6 场景, 6/6 PASS
- 模块D: 10 场景, 10/10 PASS
- 模块E: 7 场景, 7/7 PASS
- **合计: 28 场景, 28/28 PASS**
---

## 最终全量回归测试 (full_regression.py)

> 执行: 2026-04-02 final round

| 编号 | 模块 | 场景类型 | 输入描述 | 验证规则 | 结果 |
|------|------|---------|---------|---------|------|
| T-1.1 | A | 口径判定 | 广东supervised 18家+金融标注 | caliber+confidence+fin | ✅ PASS |
| T-1.2 | A | 口径判定 | 山东identifiable 7家+低信度 | 0.50≤conf≤0.65+NEWS | ✅ PASS |
| T-1.3 | A | 编码一致 | province→province_code映射 | GD/ZJ/SD/SC | ✅ PASS |
| T-1.4 | A | L2层级 | L2记录均有city | city非空 | ✅ PASS |
| T-2.1 | B | 多期拆分 | 浙江单月+累计 | period_type | ✅ PASS |
| T-2.2 | B | 调整同比 | 剔除政策性因素+8.6% | 独立记录+yoy填充 | ✅ PASS |
| T-2.3 | B | 百分点消歧 | DAR 65.4% +0.5pp | value+unit+yoy | ✅ PASS |
| T-2.4 | B | 指标标准化 | 营业收入→营业总收入 | name_raw≠name | ✅ PASS |
| T-2.5 | B | 列数完整 | 15行×28列(含修复) | col count | ✅ PASS |
| T-2.6 | B | scope编码 | A1=全国 B1=省属 | scope_code→province | ✅ PASS |
| T-3.1 | C | 主题误检 | 品牌建设意见 | topic=主责主业 | ✅ PASS |
| T-3.2 | C | 噪声排除 | 学习/读书班 | 不在12条中 | ✅ PASS |
| T-3.3 | C | 文种分级 | A级正式文件 | count≥3 | ✅ PASS |
| T-3.4 | C | 文种分级 | C级工作要点 | count≥1 | ✅ PASS |
| T-3.5 | C | 文种分级 | 征求意见稿→B | doc_type_code=B | ✅ PASS |
| T-3.6 | C | 约束词 | 不得/终身问责 | binding_phrases | ✅ PASS |
| T-3.7 | C | 省级标注 | 省级→有province | level+province | ✅ PASS |
| T-4.1 | D | 比例提取 | Tier1=35% | RULE+ratio | ✅ PASS |
| T-4.2 | D | UNIDENTIFIED | 广东省级=S4 | income+strength | ✅ PASS |
| T-4.3 | D | 截断处理 | Tier3→UNIDENTIFIED | 不填历史值 | ✅ PASS |
| T-4.4 | D | Scope消歧 | local→local_aggregate | scope_label | ✅ PASS |
| T-4.5 | D | 转移支付 | TRANSFER scope=province | record_type | ✅ PASS |
| T-4.6 | D | 全国scope | national存在 | count≥2 | ✅ PASS |
| T-4.7 | D | record_type | BUDGET_FIGURE分类 | count≥6 | ✅ PASS |
| T-4.8 | D | record_type | RULE分类 | count≥6 | ✅ PASS |
| T-4.9 | D | 覆盖率 | 31省全覆盖 | len=31 | ✅ PASS |
| T-4.10 | D | 收支配对 | 中央收3716.32+支1476.23 | 金额精确 | ✅ PASS |
| T-5.1 | E | 证据字段 | A有uev_level+D有evidence_strength | 字段存在 | ✅ PASS |
| T-5.2 | E | 省份编码 | GD vs guangdong | 已识别 | ✅ PASS |
| T-5.3 | E | 拆分路由 | RULE→栏目3 FIG/TRANS→栏目4 | 分类正确 | ✅ PASS |
| T-5.4 | E | S1证据 | S1→有URL | http开头 | ✅ PASS |
| T-5.5 | E | UNIDENTIFIED | S4+无URL | 空态处理 | ✅ PASS |
| T-5.6 | E | 图表字段 | 全国收入≥2年 | count≥2 | ✅ PASS |
| T-6.1 | X | URL追溯 | 所有记录http(S4除外) | ≤5空 | ✅ PASS |
| T-6.2 | X | 采集日期 | extraction_date=2026-04-02 | 一致 | ✅ PASS |
| T-6.3 | X | PK唯一 | 4表PK无重复 | unique | ✅ PASS |
| T-6.4 | X | 缺失标记 | UNIDENTIFIED+needs_review | 双机制 | ✅ PASS |
| T-6.5 | X | A→B关联 | ZJ entity+monthly JOIN | 可关联 | ✅ PASS |
| T-6.6 | X | 转移金额 | budget_rules=transfer CSV | 金额一致 | ✅ PASS |

## 最终统计

| 模块 | 测试数 | 通过 |
|------|--------|------|
| A 名单 | 4 | 4/4 |
| B 月度 | 6 | 6/6 |
| C 政策 | 7 | 7/7 |
| D 预算 | 10 | 10/10 |
| E 网站 | 6 | 6/6 |
| X 跨模块 | 6 | 6/6 |
| **合计** | **39** | **39/39 PASS** |

### 数据修复记录
- MO-ZJ-202601-02-profit: 修复CSV列偏移(29列→28列, 多余空列在is_cumulative前)
