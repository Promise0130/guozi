# -*- coding: utf-8 -*-
"""Phase 6b: Deep-dive into homepage HTML to find enterprise list URLs."""
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

def find_all_links(html, base_url):
    """Find all <a> links with their text and href."""
    results = []
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 1:
            results.append((href, text))
    return results

def find_enterprise_names(html):
    names = set()
    for m in re.finditer(r'[\u4e00-\u9fff（）\(\)]+(?:集团|有限公司|有限责任公司|股份有限公司)', html):
        name = m.group(0)
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标|关于印发|关于对|关于支持|合胜|拓尔|投资主体|评审|处分条例', name):
            names.add(name)
    return sorted(names)


# ─── 河北 homepage deep dive ──────────────────────
print("="*60)
print("[HE] 河北 - Homepage deep dive")
print("="*60)
try:
    html = fetch("http://hbsa.hebei.gov.cn/")
    links = find_all_links(html, "http://hbsa.hebei.gov.cn")
    # Look for any link containing enterprise/qy/jg words
    ent_kw = re.compile(r'企业|监管|qy|jgqy|ssqy|gqjj|国企|出资', re.I)
    print("All enterprise-related links:")
    for h, t in links:
        if ent_kw.search(t) or ent_kw.search(h):
            print(f"  {t:50s} → {h}")
    
    # Also find navigation menu items
    nav_kw = re.compile(r'nav|menu|col|channel', re.I)
    all_paths = set()
    for h, t in links:
        if h.startswith("/") or h.startswith("http://hbsa"):
            all_paths.add(h)
    print(f"\nAll unique paths ({len(all_paths)}):")
    for p in sorted(all_paths):
        if nav_kw.search(p) or '/col/' in p:
            print(f"  {p}")
except Exception as e:
    print(f"Error: {e}")

# Try specific paths for Hebei
print("\nTrying Hebei enterprise list paths:")
for path in ["/col/col6/", "/col/col7/", "/col/col8/", "/col/col9/", "/col/col10/",
             "/col/col11/", "/col/col12/", "/xxgk/jgqy/", "/xxgk/ssqy/",
             "/gzgk/jgqy/", "/gzgk/ssqy/", "/jgqy/qyml/", "/gqjj/"]:
    url = "http://hbsa.hebei.gov.cn" + path
    try:
        h2 = fetch(url, timeout=10)
        title_m = re.search(r'<title[^>]*>(.*?)</title>', h2, re.I | re.S)
        title = title_m.group(1).strip() if title_m else ""
        names = find_enterprise_names(h2)
        if title and ("404" not in title and "error" not in title.lower()):
            print(f"  ✓ {path:30s} Title: {title[:60]}")
            if names:
                for n in names[:10]:
                    print(f"    - {n}")
    except:
        pass

# ─── 江苏 deep dive ──────────────────────────────
print("\n" + "="*60)
print("[JS] 江苏 - Deep dive")
print("="*60)
try:
    html = fetch("http://jsgzw.jiangsu.gov.cn/")
    links = find_all_links(html, "http://jsgzw.jiangsu.gov.cn")
    ent_kw = re.compile(r'企业|监管|省属|ssqy|jgqy|qyml', re.I)
    print("Enterprise-related links:")
    for h, t in links:
        if ent_kw.search(t) or ent_kw.search(h):
            print(f"  {t:50s} → {h}")
    
    # Look for all col/ links
    print("\nAll column links:")
    for h, t in links:
        if '/col/' in h:
            print(f"  {t:50s} → {h}")
except Exception as e:
    print(f"Error: {e}")

# Fetch the col11779 page and look for actual content beyond JS
print("\nJS col/col11779 content analysis:")
try:
    html = fetch("http://jsgzw.jiangsu.gov.cn/col/col11779/index.html")
    # Print raw snippets with 集团/公司 context
    for m in re.finditer(r'.{0,30}(?:集团|公司).{0,30}', html):
        print(f"  {m.group(0).strip()}")
    # Look for dataUrl or AJAX patterns
    for m in re.finditer(r'(dataUrl|ajaxurl|data-url|url\s*[:=])\s*["\']([^"\']+)["\']', html, re.I):
        print(f"  AJAX URL: {m.group(2)}")
    # Look for iframe
    for m in re.finditer(r'<iframe[^>]*src=["\']([^"\']+)["\']', html, re.I):
        print(f"  iframe: {m.group(1)}")
except Exception as e:
    print(f"Error: {e}")

# ─── 上海 deep dive ──────────────────────────────
print("\n" + "="*60)
print("[SH] 上海 - Deep dive")
print("="*60)
try:
    html = fetch("http://www.gzw.sh.gov.cn/")
    links = find_all_links(html, "http://www.gzw.sh.gov.cn")
    ent_kw = re.compile(r'企业|监管|国企|出资|ssqy|jgqy|gqzc', re.I)
    print("Enterprise-related links:")
    for h, t in links:
        if ent_kw.search(t) or ent_kw.search(h):
            print(f"  {t:50s} → {h}")
    print("\nAll column/section links:")
    for h, t in links:
        if '/shgzw' in h or ('/col/' in h and t and len(text) > 2):
            print(f"  {t:50s} → {h}")
except Exception as e:
    print(f"Error: {e}")

# ─── 陕西 deep dive ──────────────────────────────
print("\n" + "="*60)
print("[SN] 陕西 - Deep dive")
print("="*60)
try:
    html = fetch("http://sxgz.shaanxi.gov.cn/")
    links = find_all_links(html, "http://sxgz.shaanxi.gov.cn")
    ent_kw = re.compile(r'企业|监管|国企|出资|ssqy|jgqy|gqzc|省属', re.I)
    print("Enterprise-related links:")
    for h, t in links:
        if ent_kw.search(t) or ent_kw.search(h):
            print(f"  {t:50s} → {h}")
    
    # Also print all nav-level links
    print("\nAll top-level section links:")
    for h, t in links:
        if h.startswith("/") and h.count("/") <= 3 and len(t) > 2:
            print(f"  {t:50s} → {h}")
except Exception as e:
    print(f"Error: {e}")
