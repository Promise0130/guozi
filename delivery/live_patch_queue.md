# live_patch_queue — 待应用补丁队列

> 更新: 2026-04-02

## 已应用 (本轮)
- 模块A/B: 6 组 PATCH (PATCH-01~06, 20规则) → skill_materials.md §14
- 模块C: 6 组 PATCH (PATCH-07~12, 23规则) → skill_materials.md §15
- 模块D: 5 组 PATCH (PATCH-13~17, 14规则) → skill_materials.md §16
- 模块E: 5 组 PATCH (PATCH-18~22, 16规则) → skill_materials.md §17

## 候选补丁 (下轮触发条件)

| # | 触发条件 | 补丁内容 | 优先级 |
|---|---------|---------|--------|
| Q-01 | 成功抓取北京/上海名单 | 验证 LIST-A/LIST-C 模式是否需要调整 | HIGH |
| Q-02 | 地级市采集 ≥5 个城市 | 增加 L2 级别特有的 caliber 判定规则 | MEDIUM |
| Q-03 | 季度数据采集 ≥3 省 | 增加 period_type=quarterly 处理规则 | MEDIUM |
| Q-04 | 央企名单获取成功 | 增加 admin_level=L0 + enterprise_type=央企 规则 | HIGH |
| Q-05 | 遭遇"营业总成本"指标 | 扩展 indicator 同义词表 (R7.7) | LOW |
| Q-06 | 非HTML附件(PDF/Excel)月报 | 增加附件下载+解析规则 | HIGH |
| Q-07 | 省级“国有资本收益收取管理办法”成功获取 | 验证BDG-02层级规则,增加省级比例模板 | HIGH |
| Q-08 | Tier3/4比例文本获取成功 | 补全BDG-03分档数据,更新BDG-R-003/004 | HIGH |
| Q-09 | 省级预算PDF解析成功 | 回填 BDG-P-001~005, 更新BSRC-02规则 | HIGH |
| Q-10 | 跨模块字段统一重构完成 | 落地UNIFY-01~04: 重命名底表字段+补province_code列 | HIGH |
| Q-11 | 采集≥3期时间序列数据 | 解锁折线图, 验证CHART-01趋势图最小字段集 | MEDIUM |

## 队列管理规则
1. 每轮采集后检查触发条件
2. 触发后立即编写 PATCH, 追加至 §14
3. 追加后必须运行回归测试套件
4. PASS 后更新 skill_delta.md 和 regression_suite.md
