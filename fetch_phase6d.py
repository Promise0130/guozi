# -*- coding: utf-8 -*-
"""Phase 6d: Shanghai info disclosure + Hebei more pages."""
import urllib.request
import ssl
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "identity",
}

def fetch(url, timeout=20):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
    data = resp.read()
    for enc in ["utf-8", "gbk", "gb2312", "gb18030"]:
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            pass
    return data.decode("latin-1")

def find_enterprise_names(html):
    names = set()
    for m in re.finditer(r'[\u4e00-\u9fff（）\(\)]+(?:集团|有限公司|有限责任公司|股份有限公司)', html):
        name = m.group(0)
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标|关于|合胜|拓尔|投资主体|评审|处分|选聘|服务合同|操作规则|办公厅|国务院|中央|监督管理|审计|中介|中国船舶|国家体育', name):
            names.add(name)
    return sorted(names)


# ─── 上海 企业目录/信息披露 ─────────────────────
print("="*60)
print("[SH] 上海 - /shgzw_xwzx_xxpl/ (信息披露)")
print("="*60)
try:
    html = fetch("http://www.gzw.sh.gov.cn/shgzw_xwzx_xxpl/")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    names = find_enterprise_names(html)
    print(f"Names ({len(names)}):")
    for n in names:
        print(f"  - {n}")
    # Look for enterprise directory links
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 3:
            if '集团' in text or '公司' in text or '银行' in text or '证券' in text:
                print(f"  link: {text[:80]}")
except Exception as e:
    print(f"Error: {e}")

# ─── 上海 sitemap ──────────────────────────────
print("\n[SH] 上海 - /shgzw_wzdt/ (网站地图)")
try:
    html = fetch("http://www.gzw.sh.gov.cn/shgzw_wzdt/")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    # Find all links with 企业/公司/集团
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 2 and ('企业' in text or '监管' in text or '国企' in text or '出资' in text):
            print(f"  {text:50s} → {href}")
except Exception as e:
    print(f"Error: {e}")

# ─── 上海 statistics page ──────────────────────
print("\n[SH] 上海 - /shgzw_xxgk_tzxx/ (统计数据)")
try:
    html = fetch("http://www.gzw.sh.gov.cn/shgzw_xxgk_tzxx/")
    names = find_enterprise_names(html)
    print(f"Names ({len(names)}):")
    for n in names[:20]:
        print(f"  - {n}")
except Exception as e:
    print(f"Error: {e}")

# ─── 河北 more pages ────────────────────────────
print("\n" + "="*60)
print("[HE] 河北 - more pages for enterprise names")
print("="*60)
for path in ["/GZJG419/art_page2.html", "/GZJG419/art_page3.html", 
             "/GQGG418/art_page1.html", "/GQDJ123/art_page1.html"]:
    url = "http://hbsa.hebei.gov.cn" + path
    print(f"\n  {url}")
    try:
        html = fetch(url, timeout=10)
        names = find_enterprise_names(html)
        # Also search for 【】 pattern
        brackets = set()
        for m in re.finditer(r'【(.+?)】', html):
            brackets.add(m.group(1).strip())
        if names:
            print(f"  Names: {', '.join(names[:10])}")
        if brackets:
            print(f"  【】: {', '.join(sorted(brackets))}")
        # Also get enterprise links
        for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
            href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
            if text and ('集团' in text or '公司' in text) and len(text) > 4:
                # Extract just the enterprise name
                ent_m = re.search(r'([\u4e00-\u9fff]+(?:集团|公司))', text)
                if ent_m:
                    brackets.add(ent_m.group(1))
        if brackets:
            print(f"  All enterprises: {', '.join(sorted(brackets))}")
    except Exception as e:
        print(f"  Error: {e}")

# Also try the Hebei sitemap
print("\n[HE] 河北 - sitemap")
try:
    html = fetch("http://hbsa.hebei.gov.cn/sitemap.html")
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and ('企业' in text or '监管' in text or '国企' in text):
            print(f"  {text:50s} → {href}")
except Exception as e:
    print(f"  Error: {e}")
