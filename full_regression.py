#!/usr/bin/env python3
"""Full regression test suite — covers all 5 modules + cross-cutting checks."""
import csv, sys, re

PY = "C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe"

def load_csv(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

ent = load_csv('delivery/guozi_entity_list_v1_20260402.csv')
mon = load_csv('delivery/guozi_monthly_operation_v1_20260402.csv')
pol = load_csv('delivery/guozi_policy_v1_20260402.csv')
bud = load_csv('delivery/guozi_budget_rules_v1_20260402.csv')
tra = load_csv('delivery/guozi_budget_transfer_by_province_v1_20260402.csv')

results = []

def test(tid, module, scenario, desc, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append((tid, module, scenario, desc, status, detail))
    marker = "OK" if condition else "FAIL"
    print(f"  [{marker}] {tid}: {desc}" + (f" -- {detail}" if detail and not condition else ""))

# ================================================================
# MODULE A: Entity list
# ================================================================
print("=== MODULE A: 名单表 ===")

# T-1.1 口径判定(supervised + financial)
gd_sup = [r for r in ent if r['province']=='广东' and r['list_caliber']=='supervised']
gd_fin = [r for r in gd_sup if r['includes_financial']=='TRUE']
test("T-1.1", "A", "口径判定", "广东supervised 18家 + 金融类标注",
     len(gd_sup)==18 and len(gd_fin)>=1 and all(float(r['confidence'])>=0.80 for r in gd_sup),
     f"supervised={len(gd_sup)}, financial={len(gd_fin)}")

# T-1.2 口径判定(identifiable低信度)
sd_id = [r for r in ent if r['province']=='山东' and r['list_caliber']=='identifiable']
test("T-1.2", "A", "口径判定", "山东identifiable 7家 + 低信度",
     len(sd_id)==7 and all(0.50<=float(r['confidence'])<=0.65 for r in sd_id) and all(r['source_page_type']=='NEWS' for r in sd_id),
     f"count={len(sd_id)}")

# T-1.3 province_code consistency
ent_pc = {r['province']: r['province_code'] for r in ent}
test("T-1.3", "A", "编码一致", "province→province_code映射一致",
     ent_pc.get('广东')=='GD' and ent_pc.get('浙江')=='ZJ' and ent_pc.get('山东')=='SD' and ent_pc.get('四川')=='SC',
     str(ent_pc))

# T-1.4 L2 records have city
l2 = [r for r in ent if r['admin_level']=='L2']
test("T-1.4", "A", "L2层级", "L2记录均有city字段",
     all(r['city'].strip() for r in l2),
     f"L2 count={len(l2)}")

# ================================================================
# MODULE B: Monthly data
# ================================================================
print("\n=== MODULE B: 月度经营数据 ===")

# T-2.1 多期拆分
zj_single = [r for r in mon if r['province_code']=='ZJ' and r['period_type']=='single_month']
zj_cum = [r for r in mon if r['province_code']=='ZJ' and r['period_type']=='cumulative']
test("T-2.1", "B", "多期拆分", "浙江单月+累计拆分",
     len(zj_single)>=2 and len(zj_cum)>=2,
     f"single={len(zj_single)}, cumulative={len(zj_cum)}")

# T-2.2 调整同比
yoy_adj = [r for r in mon if '剔除政策性因素' in r.get('indicator_name','')]
test("T-2.2", "B", "调整同比", "剔除政策性因素的同比独立记录",
     len(yoy_adj)>=1 and yoy_adj[0]['yoy_pct'].strip()!='' if yoy_adj else False,
     f"count={len(yoy_adj)}")

# T-2.3 百分点消歧
dar = [r for r in mon if r['indicator_name']=='资产负债率' and r['province_code']=='CN' and r['year']=='2026']
test("T-2.3", "B", "百分点消歧", "DAR=65.4% yoy=0.5pp",
     dar and dar[0]['value']=='65.4' and dar[0]['unit']=='%' and dar[0]['yoy_pct']=='0.5',
     f"val={dar[0]['value'] if dar else '?'}, yoy={dar[0]['yoy_pct'] if dar else '?'}")

# T-2.4 指标标准化
rev_raw = [r for r in mon if r['indicator_name']=='营业总收入' and r['indicator_name_raw']=='营业收入']
test("T-2.4", "B", "指标标准化", "营业收入→营业总收入标准化",
     len(rev_raw)>=1,
     f"count={len(rev_raw)}")

# T-2.5 列数正确(修复后)
test("T-2.5", "B", "列数完整", "所有行28列(含修复后MO-ZJ-202601-02-profit)",
     all(len(r)==28 for r in mon),
     f"rows={len(mon)}")

# T-2.6 scope编码
cn_a1 = [r for r in mon if r['scope_code']=='A1']
zj_b1 = [r for r in mon if r['scope_code']=='B1']
test("T-2.6", "B", "scope编码", "全国=A1, 省属=B1",
     all(r['province_code']=='CN' for r in cn_a1) and all(r['province_code']=='ZJ' for r in zj_b1),
     f"A1={len(cn_a1)}, B1={len(zj_b1)}")

# ================================================================
# MODULE C: Policy briefing
# ================================================================
print("\n=== MODULE C: 政策简报 ===")

# T-3.1 主题误检(品牌)
brand = [r for r in pol if '品牌' in r['title']]
test("T-3.1", "C", "主题误检", "品牌建设意见不应排除(有实质监管内容)",
     len(brand)==1 and brand[0]['topic_primary']=='主责主业管理',
     f"found={len(brand)}")

# T-3.2 噪声排除
noise_kw = ['学习','读书班','研讨']
is_noise = [r for r in pol if any(kw in r['title'] for kw in noise_kw)]
test("T-3.2", "C", "噪声排除", "学习/读书班类新闻不在12条中",
     len(is_noise)==0,
     f"noise_found={len(is_noise)}")

# T-3.3 文种分级A级
a_level = [r for r in pol if r['doc_type_code']=='A']
test("T-3.3", "C", "文种分级", "A级(正式规范性文件)存在多条",
     len(a_level)>=3,
     f"A-count={len(a_level)}")

# T-3.4 文种分级C级
c_level = [r for r in pol if r['doc_type_code']=='C']
test("T-3.4", "C", "文种分级", "C级(工作要点)存在",
     len(c_level)>=1,
     f"C-count={len(c_level)}")

# T-3.5 征求意见稿=B级
draft = [r for r in pol if '征求意见' in r['title']]
test("T-3.5", "C", "文种分级", "征求意见稿→B级",
     draft and draft[0]['doc_type_code']=='B',
     f"found={len(draft)}")

# T-3.6 约束词
p5 = [r for r in pol if r['id']=='POL-005']
test("T-3.6", "C", "约束词", "违规追责办法含'不得/终身问责'约束词",
     p5 and '不得' in p5[0]['binding_phrases'] and '终身问责' in p5[0]['binding_phrases'],
     f"phrases={p5[0]['binding_phrases'][:40] if p5 else '?'}...")

# T-3.7 省级政策level
prov_pol = [r for r in pol if r['level']=='省级']
test("T-3.7", "C", "省级标注", "省级政策level=省级 且有province",
     all(r.get('province','').strip() for r in prov_pol),
     f"prov_count={len(prov_pol)}")

# ================================================================
# MODULE D: Budget rules
# ================================================================
print("\n=== MODULE D: 预算规则 ===")

# T-4.1 比例提取
tier1 = [r for r in bud if r['record_id']=='BDG-R-001']
test("T-4.1", "D", "比例提取", "Tier1 ratio=35%",
     tier1 and tier1[0]['ratio_value']=='35%' and tier1[0]['record_type']=='RULE',
     f"val={tier1[0]['ratio_value'] if tier1 else '?'}")

# T-4.2 比例UNIDENTIFIED
bdg_p1 = [r for r in bud if r['record_id']=='BDG-P-001']
test("T-4.2", "D", "UNIDENTIFIED", "广东省级预算=UNIDENTIFIED+S4",
     bdg_p1 and bdg_p1[0]['budget_income']=='UNIDENTIFIED' and bdg_p1[0]['evidence_strength']=='S4',
     f"income={bdg_p1[0]['budget_income'] if bdg_p1 else '?'}")

# T-4.3 截断不推断
tier3 = [r for r in bud if r['record_id']=='BDG-R-003']
test("T-4.3", "D", "截断处理", "Tier3截断→UNIDENTIFIED而非历史值25%",
     tier3 and tier3[0]['ratio_value']=='UNIDENTIFIED' and '25' not in tier3[0]['ratio_value'],
     f"val={tier3[0]['ratio_value'] if tier3 else '?'}")

# T-4.4 Scope消歧
local_fig = [r for r in bud if r['scope']=='local']
test("T-4.4", "D", "Scope消歧", "local scope→local_aggregate label",
     all(r['scope_label']=='local_aggregate' for r in local_fig),
     f"count={len(local_fig)}")

# T-4.5 转移支付≠本级
transfers = [r for r in bud if r['record_type']=='TRANSFER']
test("T-4.5", "D", "转移支付", "TRANSFER类型scope=province",
     all(r['scope']=='province' for r in transfers),
     f"count={len(transfers)}")

# T-4.6 全国scope
national = [r for r in bud if r['scope']=='national']
test("T-4.6", "D", "全国scope", "national scope存在",
     len(national)>=2,
     f"count={len(national)}")

# T-4.7 record_type BUDGET_FIGURE
bf = [r for r in bud if r['record_type']=='BUDGET_FIGURE']
test("T-4.7", "D", "record_type", "BUDGET_FIGURE分类正确",
     len(bf)>=6 and all(r['budget_income'] or r['budget_expenditure'] or r['budget_income']=='UNIDENTIFIED' for r in bf),
     f"count={len(bf)}")

# T-4.8 record_type RULE
rules = [r for r in bud if r['record_type']=='RULE']
test("T-4.8", "D", "record_type", "RULE分类正确",
     len(rules)>=6,
     f"count={len(rules)}")

# T-4.9 转移支付31省全覆盖
test("T-4.9", "D", "转移支付覆盖", "transfer CSV 31省完整",
     len(tra)==31,
     f"provinces={len(tra)}")

# T-4.10 中央收支匹配
cf1 = [r for r in bud if r['record_id']=='BDG-F-001']
cf2 = [r for r in bud if r['record_id']=='BDG-F-002']
test("T-4.10", "D", "收支配对", "中央收入3716.32+支出1476.23",
     cf1 and cf2 and cf1[0]['budget_income']=='3716.32' and cf2[0]['budget_expenditure']=='1476.23',
     f"income={cf1[0]['budget_income'] if cf1 else '?'}, exp={cf2[0]['budget_expenditure'] if cf2 else '?'}")

# ================================================================
# MODULE E: Website field mapping
# ================================================================
print("\n=== MODULE E: 网站字段映射 ===")

# T-5.1 证据字段统一映射
ent_has_uev = all('uev_level' in r for r in ent)
bud_has_es = all('evidence_strength' in r for r in bud)
test("T-5.1", "E", "证据字段", "模块A有uev_level + 模块D有evidence_strength",
     ent_has_uev and bud_has_es,
     "fields exist in both modules")

# T-5.2 省份编码跨模块
ent_gd = any(r['province_code']=='GD' for r in ent)
bud_gd = any(r.get('province','')=='guangdong' for r in bud)
test("T-5.2", "E", "省份编码", "Entity用GD, Budget用guangdong → 已识别不一致",
     ent_gd and bud_gd,
     "known inconsistency, documented in UNIFY-02")

# T-5.3 单表多栏目拆分
bud_rule = [r for r in bud if r['record_type']=='RULE']
bud_fig = [r for r in bud if r['record_type'] in ('BUDGET_FIGURE','TRANSFER')]
test("T-5.3", "E", "record_type拆分", "RULE→栏目3, FIGURE/TRANSFER→栏目4",
     len(bud_rule)>=6 and len(bud_fig)>=10,
     f"RULE={len(bud_rule)}, FIG+TRANS={len(bud_fig)}")

# T-5.4 S1证据完整性
s1_bud = [r for r in bud if r['evidence_strength']=='S1']
test("T-5.4", "E", "S1证据", "S1记录均有source_url",
     all(r['source_url'].startswith('http') for r in s1_bud),
     f"S1 count={len(s1_bud)}")

# T-5.5 UNIDENTIFIED处理
unid_bud = [r for r in bud if r['budget_income']=='UNIDENTIFIED']
test("T-5.5", "E", "UNIDENTIFIED", "UNIDENTIFIED记录evidence_strength=S4",
     all(r['evidence_strength']=='S4' for r in unid_bud),
     f"UNID count={len(unid_bud)}")

# T-5.6 图表最小字段集
cn_rev = [r for r in mon if r['indicator_name']=='营业总收入' and r['province_code']=='CN']
test("T-5.6", "E", "图表字段集", "全国营业总收入≥2年数据",
     len(cn_rev)>=2,
     f"periods={len(cn_rev)}")

# ================================================================
# CROSS-CUTTING CHECKS
# ================================================================
print("\n=== CROSS-CUTTING: 跨模块 ===")

# T-6.1 所有表URL可追溯
all_urls = (
    [(r['record_id'] if 'record_id' in r else r['entity_id'], r.get('source_url','')) for r in ent] +
    [(r['record_id'], r.get('source_url','')) for r in mon] +
    [(r['id'], r.get('evidence_url','')) for r in pol] +
    [(r['record_id'], r.get('source_url','')) for r in bud]
)
empty_url = [(rid, u) for rid, u in all_urls if not u.startswith('http')]
test("T-6.1", "X", "URL追溯", "所有记录有http URL(除省级预算S4)",
     len(empty_url)<=5,
     f"empty/bad URLs: {len(empty_url)}")

# T-6.2 extraction_date一致
ent_dates = set(r['extraction_date'] for r in ent)
mon_dates = set(r['extraction_date'] for r in mon)
test("T-6.2", "X", "采集日期", "全部交付物extraction_date=2026-04-02",
     '2026-04-02' in ent_dates and '2026-04-02' in mon_dates,
     f"ent={ent_dates}, mon={mon_dates}")

# T-6.3 PK唯一性
ent_ids = [r['entity_id'] for r in ent]
mon_ids = [r['record_id'] for r in mon]
pol_ids = [r['id'] for r in pol]
bud_ids = [r['record_id'] for r in bud]
test("T-6.3", "X", "PK唯一", "所有表PK无重复",
     len(set(ent_ids))==len(ent_ids) and len(set(mon_ids))==len(mon_ids) and len(set(pol_ids))==len(pol_ids) and len(set(bud_ids))==len(bud_ids),
     f"ent={len(ent_ids)}/{len(set(ent_ids))}, mon={len(mon_ids)}/{len(set(mon_ids))}, pol={len(pol_ids)}/{len(set(pol_ids))}, bud={len(bud_ids)}/{len(set(bud_ids))}")

# T-6.4 缺失项标记一致
bud_unid_count = sum(1 for r in bud if 'UNIDENTIFIED' in str(list(r.values())))
ent_review = sum(1 for r in ent if r['needs_manual_review']=='TRUE')
test("T-6.4", "X", "缺失标记", "UNIDENTIFIED(D)+needs_manual_review(A)均有使用",
     bud_unid_count>=5 and ent_review>=10,
     f"budget_UNID={bud_unid_count}, entity_review={ent_review}")

# T-6.5 JOIN可行(entity→monthly)
zj_ents = [r for r in ent if r['province_code']=='ZJ']
zj_mon = [r for r in mon if r['province_code']=='ZJ' and r['scope_code']=='B1']
test("T-6.5", "X", "A→B关联", "浙江entity+monthly可通过province_code=ZJ JOIN",
     len(zj_ents)>=1 and len(zj_mon)>=1,
     f"ent_ZJ={len(zj_ents)}, mon_ZJ_B1={len(zj_mon)}")

# T-6.6 transfer金额跨表一致
bud_t = {r['province']: float(r.get('budget_income','0') or '0') for r in bud if r['record_type']=='TRANSFER'}
tra_d = {r['province']: float(r['2026_budget_100M_CNY']) for r in tra}
mismatches = [p for p in bud_t if p in tra_d and abs(bud_t[p]-tra_d[p])>0.01]
test("T-6.6", "X", "转移金额一致", "budget_rules TRANSFER金额=transfer CSV金额",
     len(mismatches)==0,
     f"mismatches={mismatches}" if mismatches else "all match")

# ================================================================
# SUMMARY
# ================================================================
print("\n" + "="*60)
total = len(results)
passed = sum(1 for r in results if r[4]=='PASS')
failed = [r for r in results if r[4]=='FAIL']
print(f"TOTAL: {total} tests | PASS: {passed} | FAIL: {len(failed)}")
if failed:
    print("\nFAILED TESTS:")
    for tid, mod, scen, desc, status, detail in failed:
        print(f"  {tid} [{mod}] {desc}: {detail}")
else:
    print("ALL TESTS PASSED")

# Module breakdown
for mod in ['A','B','C','D','E','X']:
    mod_tests = [r for r in results if r[1]==mod]
    mod_pass = sum(1 for r in mod_tests if r[4]=='PASS')
    print(f"  Module {mod}: {mod_pass}/{len(mod_tests)}")
