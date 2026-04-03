# -*- coding: utf-8 -*-
"""
Phase 3: Deep-dive into Jiangxi enterprise list + try more blocked sites.
"""
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
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标|咨询|投资主体|建设服务', name):
            names.add(name)
    return sorted(names)


def extract_links(html, patterns):
    results = []
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 2:
            for pat in patterns:
                if re.search(pat, text) or re.search(pat, href):
                    results.append((href, text))
                    break
    return results


# ─── Jiangxi enterprise list page ──────────────────────────
print("=" * 60)
print("[JX] 江西 - Enterprise list page")
print("=" * 60)

try:
    # Try the enterprise list URL found from homepage
    url = "http://gzw.jiangxi.gov.cn/jxsgzw/sczjgqykjcgtgyyqd/pc/list.html"
    print(f"Fetching: {url}")
    html = fetch(url)
    print(f"Got {len(html)} bytes")

    names = find_enterprise_names(html)
    print(f"\nEnterprise names from list page ({len(names)}):")
    for n in names:
        print(f"  - {n}")

    # Also try to find links to individual enterprise pages
    links = extract_links(html, [r'集团', r'公司'])
    if links:
        print(f"\nEnterprise links ({len(links)}):")
        for h, t in links[:30]:
            print(f"  {t:50s} → {h}")

except Exception as e:
    print(f"Error: {e}")

# Also try to extract from jgqy/ path
print("\nTrying /jxsgzw/jgqy/ ...")
try:
    for path in ["/jxsgzw/jgqy/", "/col/col83766/", "/jxsgzw/ssqyml/"]:
        url = "http://gzw.jiangxi.gov.cn" + path
        try:
            html = fetch(url, timeout=10)
            names = find_enterprise_names(html)
            if names:
                print(f"\n  {url}: {len(names)} names")
                for n in names[:30]:
                    print(f"    - {n}")
                break
            else:
                # Look for enterprise-related text
                if re.search(r'监管企业|企业名录|省属企业', html):
                    print(f"  {url}: enterprise text found but no names extracted")
                    # Print relevant context
                    for m in re.finditer(r'[\u4e00-\u9fff]{2,}(?:集团|公司)', html):
                        print(f"    possibe: {m.group(0)}")
        except Exception as e2:
            print(f"  {url}: {e2}")
except Exception as e:
    print(f"Error: {e}")


# ─── Try remaining really blocked sites via search engines / open search ──
print("\n" + "=" * 60)
print("Try accessing blocked sites via alternative methods")
print("=" * 60)

# Try gov portal integration pages that may aggregate SASAC data
alt_approaches = {
    "TJ": [
        "http://gzw.tj.gov.cn/gzw/gzdt/",  # national affair dynamics
        "http://www.sasac.gov.cn/n4422011/n17627531/c17633273/content.html",  # central SASAC's local list
    ],
    "SN": [
        "http://gzw.sxgzw.shaanxi.gov.cn/",
        "http://sxgzw.shaanxi.gov.cn/",
    ],
    "GS": [
        "http://gzw.gansu.gov.cn/gzw/",
        "http://gansu.gzw.gov.cn/",
    ],
    "QH": [
        "http://gzw.qinghai.gov.cn/gzw/", 
    ],
    "HB": [
        "http://gzw.hubei.gov.cn/gzw/",
    ],
}

for code, urls in alt_approaches.items():
    province_names = {"TJ":"天津","SN":"陕西","GS":"甘肃","QH":"青海","HB":"湖北"}
    print(f"\n[{code}] {province_names[code]}")
    for url in urls:
        print(f"  Trying: {url}")
        try:
            text = fetch(url, timeout=10)
            title_m = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
            title = title_m.group(1).strip() if title_m else ""
            names = find_enterprise_names(text)
            print(f"    ✓ {len(text)} bytes, title: {title[:60]}, enterprises: {len(names)}")
            if names:
                for n in names[:15]:
                    print(f"      - {n}")
        except Exception as e:
            print(f"    ✗ {e}")


# ─── 西藏 - CORRECT URL ──────────────────────────────────
print("\n" + "=" * 60)
print("[XZ] 西藏 - Finding correct URL")
print("=" * 60)

xz_urls = [
    "http://gzw.xizang.gov.cn/",
    "https://gzw.xizang.gov.cn/",
    "http://gzw.tibet.gov.cn/",
    "http://xzgzw.xizang.gov.cn/",
    "http://www.xizang.gov.cn/zwgk/xxfb/szdw/gzw/",
]
for url in xz_urls:
    print(f"  Trying: {url}")
    try:
        text = fetch(url, timeout=10)
        title_m = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
        title = title_m.group(1).strip() if title_m else ""
        print(f"    ✓ {len(text)} bytes, title: {title[:80]}")
        names = find_enterprise_names(text)
        if names:
            print(f"    Enterprises: {len(names)}")
            for n in names[:20]:
                print(f"      - {n}")
        break
    except Exception as e:
        print(f"    ✗ {e}")
