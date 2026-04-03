# skill_delta — 本轮 Skill 变更清单

> 更新: 2026-04-02

## 变更文件

### 1. skill_materials.md
- **位置**: §14 (新增追加段, 约 120 行)
- **内容**: 6 个 PATCH 组, 20 条新规则

| PATCH | 规则 ID | 主题 |
|-------|---------|------|
| PATCH-01 | R4.4 ~ R4.7 | 省份特异口径 + LIST-F 完整度 + identifiable 置信区间 + LIST-B 处理 |
| PATCH-02 | NE-01 ~ NE-04 | 企业名称清洗(去"有限公司"/全称mapping/拼音/别名) |
| PATCH-03 | R6.5 ~ R6.7 | 多期拆分 + 年度/累计边界 + 存量指标期限标注 |
| PATCH-04 | R7.5 ~ R7.7 | 调整同比 + 百分点消歧 + indicator 同义词扩展 |
| PATCH-05 | URL-01 ~ URL-03 | 重试策略 + 备用下载 + 反爬 fallback |
| PATCH-06 | MISS-01 ~ MISS-03 | 替代频率 + 缺失等级 + 指标缺失处理 |

### 2. failure_modes.md
- **位置**: 文件末尾新增 "Real-World Delivery" 段
- **内容**: FM-RW-01 ~ FM-RW-06 (6 条新失败模式)
- **总条目数**: 87 → 93

### 3. skill_worklog.md
- **位置**: Step 8 (新增)
- **内容**: 完整记录本次实战交付过程

### 4. skill_materials.md (模块C追加)
- **位置**: §15 (新增追加段, 约 160 行)
- **内容**: 6 个 PATCH 组, 23 条新规则

| PATCH | 规则 ID | 主题 |
|-------|---------|------|
| PATCH-07 | TOPIC-01 ~ TOPIC-06 | 5大主题关键词库(含include/exclude) + 全局噪声排除 |
| PATCH-08 | DOC-01 ~ DOC-05 | 文种分级A-E(部委令/两办/通知/要点/新闻) |
| PATCH-09 | BIND-01 ~ BIND-04 | 约束性表述4级(强制/应当/鼓励/可选) |
| PATCH-10 | LOCAL-01 ~ LOCAL-03 | 地方文种映射("行动"→C级/证据上限) |
| PATCH-11 | TREAS-01 ~ TREAS-02 | 司库同义词映射(司库≈资金集中管理≈DRP) |
| PATCH-12 | TPL-01 ~ TPL-03 | 时间窗口+简报模板+15字段schema |

### 5. failure_modes.md (模块C追加)
- **位置**: FM-RW-07 ~ FM-RW-12
- **内容**: 6 条新失败模式(主题误检/噪声/文种/约束词/地方表述/司库)
- **总条目数**: 93 → 99

### 6. skill_worklog.md (模块C追加)
- **位置**: Step 9 (新增)
- **内容**: 模块C政策简报完整交付过程

### 7. skill_materials.md (模块D追加)
- **位置**: §16 (新增追加段, 约 140 行)
- **内容**: 5 个 PATCH 组, 14 条新规则

| PATCH | 规则 ID | 主题 |
|-------|---------|------|
| PATCH-13 | BDG-01~03 | record_type二分(BUDGET_FIGURE/RULE/TRANSFER) + 比例规则来源层次 + 分类分档完整性校验 |
| PATCH-14 | SCOPE-01~04 | scope多级编码(national/central/local_aggregate/province/city) + “本级”消歧 + 转移支付≠本级预算 + 全省/本级标注 |
| PATCH-15 | SPEC-01~03 | 特殊预算条目清单(兵团/结转/金融/产权) + 收入总量vs当年收入 + 支出结构标准化 |
| PATCH-16 | BTPL-01~02 | 预算摘要21字段schema + UNIDENTIFIED强制标注 |
| PATCH-17 | BSRC-01~02 | 预算数据源优先级(5级) + 省级PDF处理规则 |

### 8. failure_modes.md (模块D追加)
- **位置**: FM-RW-13 ~ FM-RW-18
- **内容**: 6 条新失败模式(预算数字/规则分离, 比例来源, 分档截断, 本级多义, 转移支付误判, PDF不可解析)
- **总条目数**: 99 → 105

### 9. skill_worklog.md (模块D追加)
- **位置**: Step 10 (新增)
- **内容**: 模块D预算规则完整交付过程

## 变更验证
- 模块A/B 回归测试: 5/5 PASS (见 E_regression_tests.md)
- 模块C 回归测试: 6/6 PASS (见 E_policy_regression_tests.md)
- 模块D 回归测试: 10/10 PASS (见 F_budget_regression_tests.md)
- 无既有规则被修改或删除（仅追加）
- 向后兼容: 所有 PATCH 规则编号独立, 不与 R1~R8 / UR-01~08 / TOPIC~TPL 冲突

### 10. skill_materials.md (模块E追加)
- **位置**: §17 (新增追加段, 约 130 行)
- **内容**: 5 个 PATCH 组, 16 条新规则

| PATCH | 规则 ID | 主题 |
|-------|---------|------|
| PATCH-18 | UNIFY-01~04 | 跨交付物字段统一(证据回链命名/省份编码/record_type枚举/主键规范) |
| PATCH-19 | API-01~03 | 前端接口模板(接口清单/单表多栏目拆分/筛选维度) |
| PATCH-20 | EVLINK-01~03 | 证据回链机制(面板标准/跨模块适配/UNIDENTIFIED处理) |
| PATCH-21 | CHART-01~03 | 图表组件约束(最小字段集/空态处理/底表对齐) |
| PATCH-22 | BRIEF-01~03 | 简报附录映射(三层展示/约束词标色/财政栏目映射) |

### 11. failure_modes.md (模块E追加)
- **位置**: FM-RW-19 ~ FM-RW-24
- **内容**: 6 条新失败模式(证据字段不一致/省份编码/单表拆分/图表空态/摘要丢失/字段不对齐)
- **总条目数**: 105 → 111

### 12. skill_worklog.md (模块E追加)
- **位置**: Step 11 (新增)
- **内容**: 模块E网站展示层完整交付过程

## 变更验证
- 模块A/B 回归测试: 5/5 PASS (见 E_regression_tests.md)
- 模块C 回归测试: 6/6 PASS (见 E_policy_regression_tests.md)
- 模块D 回归测试: 10/10 PASS (见 F_budget_regression_tests.md)
- 模块E 回归测试: 7/7 PASS (见 G_site_regression_tests.md)
- 无既有规则被修改或删除（仅追加）
- 向后兼容: 所有 PATCH 规则编号独立, 不与 R1~R8 / UR-01~08 / TOPIC~BSRC 冲突
