# 最终 Skill 包说明 (Final Skill Package)

> 版本: v1.0-final | 日期: 2026-04-02
> 主题: 地方国资信息采集与分析

---

## 一、包文件结构

```
guozi_skill_prep/
├── skill_materials.md          ← 核心: 2897行, §1~§17, 全部规则+补丁
├── failure_modes.md            ← 111种失败模式 (通用11+P1-12+P2-14+P3-22+P4-20+X-8+RW-24)
├── field_schema.md             ← 186+字段定义, JSON Schema
├── source_registry.md          ← 15个信息源注册, 适配度矩阵
├── part_playbooks.md           ← 四专题SOP (P1~P4)
├── skill_worklog.md            ← 12步工作日志
│
├── delivery/                   ← 交付物 + 跟踪文件
│   ├── 数据文件 (5个CSV + 1 Word)
│   │   ├── guozi_entity_list_v1_20260402.csv        (32行/21列)
│   │   ├── guozi_monthly_operation_v1_20260402.csv   (15行/28列)
│   │   ├── guozi_policy_v1_20260402.csv              (12行/15列)
│   │   ├── guozi_budget_rules_v1_20260402.csv        (21行/21列)
│   │   ├── guozi_budget_transfer_by_province_v1.csv  (31行/3列)
│   │   └── guozi_policy_briefing_v1_20260402.docx    (6章Word简报)
│   │
│   ├── 说明文档
│   │   ├── A_entity_list_schema.md
│   │   ├── A_coverage_matrix.md
│   │   ├── B_monthly_data_schema.md
│   │   ├── E_site_map.md
│   │   ├── artifact_specs.md
│   │   └── normalization_rules.md
│   │
│   ├── 复盘文档
│   │   ├── C_micro_retro.md          (模块A/B)
│   │   ├── C_policy_micro_retro.md   (模块C)
│   │   ├── D_budget_micro_retro.md   (模块D)
│   │   └── E_site_micro_retro.md     (模块E)
│   │
│   ├── 测试文档
│   │   ├── E_regression_tests.md      (模块A/B, 5场景)
│   │   ├── E_policy_regression_tests.md (模块C, 6场景)
│   │   ├── F_budget_regression_tests.md (模块D, 10场景)
│   │   ├── G_site_regression_tests.md   (模块E, 7场景)
│   │   └── regression_suite.md          (最终全量, 39场景)
│   │
│   ├── 跟踪文件
│   │   ├── delivery_manifest.md
│   │   ├── evidence_index.md
│   │   ├── limitation_log.md    (12项已知限制)
│   │   ├── unresolved_items.md  (7项未解决)
│   │   ├── failure_patterns.md
│   │   ├── live_patch_queue.md
│   │   ├── skill_delta.md
│   │   └── release_notes.md
│   │
│   └── 脚本
│       ├── gen_policy_briefing.py
│       └── gen_budget_summary.py
│
├── site/                       ← 网站展示层 (11个文件)
│   ├── index.html
│   ├── css/main.css
│   ├── js/app.js
│   ├── pages/{entities,operations,policies,budget}.html
│   └── data/{entity_list,monthly_operation,policy_briefing,budget_rules,budget_transfer}.csv
│
└── 校验脚本
    ├── final_check.py           (跨交付物一致性校验)
    └── full_regression.py       (39项完整回归测试)
```

---

## 二、Skill 规则总量

### 原始规则 (§1~§11, 步骤1~5设计阶段)

| 类别 | 数量 | 覆盖 |
|------|------|------|
| 判断规则 (R/JC/JT/NV/AU/VER/PT) | ~45 | 口径/期间/标准化/真实性/时效性 |
| 失败模式 (FM) | 87 | 通用+P1~P4+跨Part |
| 关键词 | ~194 | 4 Part + 通用排除词 |
| 字段定义 | ~186 | 4 Part + 17公共字段 |
| 信息源注册 | 15 | S1~S8 × 3层级 |
| SOP流程 | 4 | P1~P4 (含Phase/回退链) |

### 实战补丁 (§14~§17, 模块A~E交付后追加)

| 补丁 | 来源模块 | 规则数 | 涵盖 |
|------|---------|--------|------|
| PATCH-01~06 (§14) | A+B | 20 | 口径/名称/期间/标准化/URL/缺失 |
| PATCH-07~12 (§15) | C | 23 | 主题词/文种/约束词/地方映射/司库/模板 |
| PATCH-13~17 (§16) | D | 14 | 预算拆分/Scope判定/特殊规定/收取模板/采集策略 |
| PATCH-18~22 (§17) | E | 16 | 统一字段/接口/证据回链/图表/简报映射 |
| **合计** | | **73** | |

### 实战失败模式 (FM-RW-01~24)

| 组别 | 来源 | 数量 |
|------|------|------|
| FM-RW-01~06 | 模块A/B | 6 |
| FM-RW-07~12 | 模块C | 6 |
| FM-RW-13~18 | 模块D | 6 |
| FM-RW-19~24 | 模块E | 6 |
| **合计** | | **24** |

### 总计
- **规则总量**: ~45原始 + 73补丁 = **~118条判断规则**
- **失败模式总量**: 87原始 + 24实战 = **111种失败模式**
- **回归测试总量**: **39场景, 39/39 PASS**

---

## 三、Skill 架构蓝图 (§12)

未来封装为正式 SKILL.md 时推荐:

```
SKILL.md                (~270行, 7类指令: 触发/工作流/决策树/输出/口径/引用/guardrails)
references/
  source-identification-rules.md   (UR-01~02, 信息源路由)
  keyword-lexicon.md               (194个关键词)
  field-dictionary.md              (186+字段, JSON Schema)
  failure-modes.md                 (111种失败模式)
  confidence-rules.md              (UEV 5级体系)
  period-rules.md                  (12个期间正则)
  caliber-guide.md                 (口径全景)
  examples.md                      (10个JSON示例)
  source-registry.md               (15个已验证信息源)
scripts/
  entity-list-extractor.spec.md
  monthly-data-parser.spec.md
  policy-scanner.spec.md
  budget-rule-extractor.spec.md
templates/
  policy-briefing-template.md
  budget-summary-template.md
validation/
  regression-suite.py              (39项自动化测试)
  consistency-check.py             (跨交付物校验)
```

---

## 四、未来迭代清单 (源自 live_patch_queue + unresolved_items)

| 优先级 | 项目 | 预期收益 |
|--------|------|---------|
| HIGH | 补采27省数据 (U-04) | 名单从4省→31省 |
| HIGH | Playwright替代fetch_webpage (L-01) | 解决50%网站抓取失败 |
| HIGH | PDF解析能力 (L-09) | 解决省级预算报告不可读 |
| MEDIUM | 省份编码统一为2字母大写 (UNIFY-02) | 消除跨模块JOIN障碍 |
| MEDIUM | 证据字段名统一 (UNIFY-01) | 消除前端特判 |
| MEDIUM | 补采地级市企业名单 (U-05) | L2层级数据 |
| LOW | 时间序列加深至≥3期 (CHART-01) | 趋势图可用 |
| LOW | 地方政策库深度采集 (L-08) | 政策覆盖率提升 |
