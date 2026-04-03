---
name: guozi-source-registry
description: "Use when locating provincial SASAC official URLs, verifying province/municipality SASAC domains, updating the official link registry, or collecting provincial SOE lists and国有资本收益管理规则 only from provincial SASAC official websites."
---

# 地方国资官网注册链接 Skill

## 目标

把地方国资相关采集统一收敛到“省级国资委官网注册链接表”，避免使用新闻页、转载页或猜测域名。

## 必用文件

- [delivery/sasac_official_link_registry.md](../../../delivery/sasac_official_link_registry.md)
- [delivery/sasac_website_registry.csv](../../../delivery/sasac_website_registry.csv)

## 权威上游

国务院国资委地方国资委页面：
http://www.sasac.gov.cn/n4422011/n17627531/c17633273/content.html

## 工作流

1. 先读取注册链接表，检查目标省份是否已有 `sasac_url` 和 `enterprise_list_url`。
2. 如果链接失效或疑似错误，到国务院国资委地方国资委页面核对该省锚点链接。
3. 仅在确认正确官网 URL 后访问省级国资委官网。
4. 企业名单、收益管理规则、监管政策，必须继续在该官网同域名下寻找正文或名录页。
5. 每次完成地方国资相关采集后，必须立即同步更新 `site/data/*.csv` 与对应网站页面，不能只改底表不改展示层。
6. 若官网正确但被 WAF/JS challenge 阻断：
   - 保留官方 URL。
   - 在注册链接表中标记 `BLOCKED`。
   - 记录阻断机制和最近测试日期。
   - 不得把新闻页、转载页、第三方页面写成替代来源。

## 已验证 blocked 省份

- 湖北：官方 URL 已确认；浏览器可获 challenge cookie，但同会话访问根路径和候选栏目页仍返回 400。
- 甘肃：官方 URL 已确认；浏览器可获 challenge cookie，但同会话访问根路径和候选栏目页仍返回 400。
- 青海：官方 URL 已确认；浏览器可获 challenge cookie，但同会话访问根路径和候选栏目页仍返回 400。
- 西藏：官方主机当前返回 502，且国务院国资委“地方国资委”页面该行无可点击 href。

以上四省区当前必须继续保留为 `BLOCKED`，不得以省政府新闻页、转载页、门户快讯或第三方页面替代为最终来源。

## 强约束

- 不得凭 `gzw.{province}.gov.cn` 规则猜域名。
- 不得把国务院国资委“地方”新闻转载页当作省级最终来源。
- 不得把省政府新闻频道、门户新闻稿、企业新闻稿写入注册链接表替代 `sasac_url`。
- 只有省级国资委官网或其同域名栏目页，才能作为国企名单和收益管理规则的最终来源。

## 任务完成提示

每次完成地方国资相关任务后，在回复末尾附上首页访问链接，方便用户直接查看最新数据：

> 首页入口：http://localhost:4174/

## 输出要求

每次更新后至少同步以下字段：

- `province`
- `province_code`
- `sasac_url`
- `enterprise_list_url`
- `status`
- `last_tested`
- `notes`

## 状态定义

- `OK`: 官网和目标栏目都可直接进入
- `PARTIAL`: 官网可进入，但目标栏目仍需进一步定位或无法完整展开
- `BLOCKED`: 正确官网 URL 已确认，但当前环境无法通过反爬
- `UNTESTED`: 未测试
