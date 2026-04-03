# -*- coding: utf-8 -*-
"""Phase 6c: Fetch Hebei enterprise pages, Shanghai enterprise section, Shaanxi省属."""
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
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标|关于印发|关于对|关于支持|合胜|拓尔|投资主体|评审|处分条例|选聘|服务合同|操作规则', name):
            names.add(name)
    return sorted(names)

# ─── 河北 enterprise pages ────────────────────────
print("="*60)
print("[HE] 河北 - /xxgk/jgqy/ (监管企业)")
print("="*60)
try:
    html = fetch("http://hbsa.hebei.gov.cn/xxgk/jgqy/")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    names = find_enterprise_names(html)
    print(f"Names ({len(names)}):")
    for n in names:
        print(f"  - {n}")
    # Find links
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and ('集团' in text or '公司' in text or '企业' in text) and len(text) > 3:
            print(f"  link: {text:50s} → {href}")
except Exception as e:
    print(f"Error: {e}")

print("\n[HE] 河北 - /xxgk/ssqy/ (省属企业)")
try:
    html = fetch("http://hbsa.hebei.gov.cn/xxgk/ssqy/")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    names = find_enterprise_names(html)
    print(f"Names ({len(names)}):")
    for n in names:
        print(f"  - {n}")
    # Find all numbered article links
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 3 and not text.startswith('http'):
            print(f"  article: {text[:80]}")
except Exception as e:
    print(f"Error: {e}")

# Try GZJG419 path from the homepage link
print("\n[HE] 河北 - /GZJG419/")
try:
    html = fetch("http://hbsa.hebei.gov.cn/GZJG419/art_page1.html")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    names = find_enterprise_names(html)
    print(f"Names ({len(names)}):")
    for n in names[:20]:
        print(f"  - {n}")
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and ('集团' in text or '公司' in text) and len(text) > 4:
            print(f"  link: {text[:80]}")
except Exception as e:
    print(f"Error: {e}")

# ─── 上海 gqzc section ─────────────────────────────
print("\n" + "="*60)
print("[SH] 上海 - /shgzw_gqzc/ and /shgzw_wsbs/ sections")
print("="*60)
for path in ["/shgzw_gqzc/", "/shgzw_wsbs/", "/shgzw_xxgk_cyggcz/"]:
    url = "http://www.gzw.sh.gov.cn" + path
    print(f"\n  {url}")
    try:
        html = fetch(url, timeout=10)
        title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
        print(f"  Title: {title_m.group(1).strip() if title_m else 'N/A'}")
        names = find_enterprise_names(html)
        if names:
            print(f"  Names ({len(names)}):")
            for n in names[:20]:
                print(f"    - {n}")
        # Enterprise links
        for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
            href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
            if text and ('集团' in text or '公司' in text or '企业' in text) and len(text) > 3:
                print(f"    link: {text[:60]:60s} → {href[:60]}")
    except Exception as e:
        print(f"  Error: {e}")

# ─── 陕西 gqzc section for 省属企业 ────────────────
print("\n" + "="*60)
print("[SN] 陕西 - 国企之窗 deep dive")
print("="*60)
try:
    html = fetch("http://sxgz.shaanxi.gov.cn/sy/gqzc/")
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    print(f"Title: {title_m.group(1).strip() if title_m else 'N/A'}")
    # Find all enterprise-related links
    ent_names_from_brackets = set()
    for m in re.finditer(r'【(.+?)】', html):
        name = m.group(1).strip()
        if len(name) >= 3:
            ent_names_from_brackets.add(name)
    print(f"\n企业 from 【】 brackets ({len(ent_names_from_brackets)}):")
    for n in sorted(ent_names_from_brackets):
        print(f"  - {n}")
except Exception as e:
    print(f"Error: {e}")

# Fetch enterprise dynamics page for more names
for path in ["/sy/gqzc/qydt/", "/gk/ssqy/", "/sy/gqzc/qydt/index_1.html", "/sy/gqzc/qydt/index_2.html"]:
    url = "http://sxgz.shaanxi.gov.cn" + path
    print(f"\n  {url}")
    try:
        html = fetch(url, timeout=10)
        names_brackets = set()
        for m in re.finditer(r'【(.+?)】', html):
            names_brackets.add(m.group(1).strip())
        if names_brackets:
            print(f"  From 【】: {', '.join(sorted(names_brackets))}")
    except Exception as e:
        print(f"  Error: {e}")
