# 地方国资采集工作区规则

适用于本仓库内所有“地方国资信息采集与分析”任务。

## 官方来源规则

1. 省级/直辖市/兵团国资委官网链接必须先从 [delivery/sasac_official_link_registry.md](../delivery/sasac_official_link_registry.md) 或 [delivery/sasac_website_registry.csv](../delivery/sasac_website_registry.csv) 读取，不得临时凭经验猜测域名。
2. 链接注册表的权威上游是国务院国资委“地方国资委”页面：
   http://www.sasac.gov.cn/n4422011/n17627531/c17633273/content.html
3. 如果某省官网链接访问失败，先回到国务院国资委地方国资委列表核对并更新正确 URL，再重试；不要改用新闻站、政府综合门户新闻页或第三方转载页替代官网链接。
4. 国企名单、收益管理规则、监管制度、政策原文的首选来源必须是对应省级国资委官网及其同域名子栏目。
5. 新闻稿、转载页、国务院国资委“地方”栏目、政府综合门户新闻频道只能作为线索，不能替代省级国资委官网作为最终取数来源。
6. 若正确官网 URL 已确认但仍被 WAF/JS challenge 阻断，应在注册表中保留该官方 URL 并标记阻断原因；不得用非官网新闻页面替换该来源。

## 更新注册表时必须记录

- province / province_code
- sasac_url
- enterprise_list_url
- status
- last_tested
- notes

## 状态解释

- `OK`: 官网和企业名录页可直接访问
- `PARTIAL`: 官网可访问，但名录页仍需进一步定位或有 JS/分页限制
- `BLOCKED`: 正确官网 URL 已确认，但当前抓取环境被 WAF/反爬阻断
- `UNTESTED`: 尚未验证

## 执行顺序

1. 先读注册表
2. 再访问对应国资委官网
3. 如失败，回中央国资委地方国资委列表核对 URL
4. 更新注册表
5. 仅从确认后的官网栏目继续抽取名单或政策
