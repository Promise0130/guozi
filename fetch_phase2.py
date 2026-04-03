# -*- coding: utf-8 -*-
"""
Phase 2: Extract enterprise lists from newly accessible SASAC sites.
"""
import urllib.request
import ssl
import re
import sys

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


def extract_links_and_text(html, patterns):
    """Extract all href links and text containing enterprise-related patterns."""
    results = []
    # Find all links with relevant text
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 2:
            for pat in patterns:
                if re.search(pat, text) or re.search(pat, href):
                    results.append((href, text))
                    break
    return results


def find_enterprise_names(html):
    """Extract enterprise-like names from HTML."""
    # Match typical SOE names: XX集团/公司/有限 etc.
    names = set()
    # Full formal names
    for m in re.finditer(r'[\u4e00-\u9fff（）\(\)]+(?:集团|有限公司|有限责任公司|股份有限公司)', html):
        name = m.group(0)
        # Filter: must be > 6 chars, contain province/city indicator
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持', name):
            names.add(name)
    return sorted(names)


# ─── Jiangxi ──────────────────────────────────────────────
print("=" * 60)
print("[JX] 江西 - http://gzw.jiangxi.gov.cn/")
print("=" * 60)

try:
    html = fetch("http://gzw.jiangxi.gov.cn/")
    # Find enterprise list page link
    ent_links = extract_links_and_text(html, [r'监管企业', r'企业名录', r'jgqy', r'qyml', r'ssqy', r'省属企业'])
    print("Enterprise-related links found on homepage:")
    for href, text in ent_links[:20]:
        print(f"  {text:40s} → {href}")

    # Also extract enterprise names from homepage
    names = find_enterprise_names(html)
    if names:
        print(f"\nEnterprise names found on homepage ({len(names)}):")
        for n in names[:50]:
            print(f"  - {n}")

    # Try known enterprise list URL pattern
    ent_url = None
    for href, text in ent_links:
        if 'jgqy' in href or 'qyml' in href or '企业' in text:
            if href.startswith('/'):
                ent_url = "http://gzw.jiangxi.gov.cn" + href
            elif href.startswith('http'):
                ent_url = href
            break

    if ent_url:
        print(f"\nFetching enterprise list page: {ent_url}")
        html2 = fetch(ent_url)
        names2 = find_enterprise_names(html2)
        if names2:
            print(f"Enterprise names ({len(names2)}):")
            for n in names2:
                print(f"  - {n}")
        # Also look for list links
        links2 = extract_links_and_text(html2, [r'集团', r'公司', r'有限'])
        if links2:
            print(f"\nEnterprise links ({len(links2)}):")
            for href, text in links2[:40]:
                print(f"  {text:50s}")

except Exception as e:
    print(f"Error: {e}")

# ─── Guangxi ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("[GX] 广西 - http://gzw.gxzf.gov.cn/")
print("=" * 60)

try:
    html = fetch("http://gzw.gxzf.gov.cn/")
    ent_links = extract_links_and_text(html, [r'监管企业', r'企业名录', r'jgqy', r'qyml', r'ssqy', r'省属'])
    print("Enterprise-related links found on homepage:")
    for href, text in ent_links[:20]:
        print(f"  {text:40s} → {href}")

    names = find_enterprise_names(html)
    if names:
        print(f"\nEnterprise names found on homepage ({len(names)}):")
        for n in names[:50]:
            print(f"  - {n}")

    # Try to find enterprise list page
    for href, text in ent_links:
        if '名录' in text or 'qyml' in href or 'ssqy' in href:
            if href.startswith('/'):
                ent_url = "http://gzw.gxzf.gov.cn" + href
            elif href.startswith('http'):
                ent_url = href
            else:
                continue
            print(f"\nFetching: {ent_url}")
            try:
                html2 = fetch(ent_url)
                names2 = find_enterprise_names(html2)
                links2 = extract_links_and_text(html2, [r'集团', r'公司', r'有限'])
                if names2:
                    print(f"Enterprise names ({len(names2)}): {names2[:30]}")
                if links2:
                    print(f"Enterprise links ({len(links2)}):")
                    for h, t in links2[:30]:
                        print(f"  {t}")
            except Exception as e2:
                print(f"  Error: {e2}")
            break

except Exception as e:
    print(f"Error: {e}")


# ─── Try remaining blocked sites with different approaches ─────
print("\n" + "=" * 60)
print("Trying remaining blocked sites with HTTP/1.0 and 302 follow")
print("=" * 60)

STILL_BLOCKED = {
    "TJ": [
        "https://gzw.tj.gov.cn/",
        "http://www.tj.gov.cn/zwgk/szfgz/szfz/gzw/",
    ],
    "HE": [
        "https://gzw.hebei.gov.cn/",
        "http://www.hebei.gov.cn/hebei/11937442/10756595/13390082/index.html",
    ],
    "SH": [
        "https://gzw.sh.gov.cn/",
        "http://www.shanghai.gov.cn/nw48547/index.html",
    ],
    "JS": [
        "https://gzw.jiangsu.gov.cn/",
        "http://www.jiangsu.gov.cn/col/s86982/",
    ],
    "HB": [
        "https://gzw.hubei.gov.cn/",
        "http://www.hubei.gov.cn/zfzs/szfz/gzw/",
    ],
    "SN": [
        "https://gzw.shaanxi.gov.cn/",
        "http://www.shaanxi.gov.cn/gk/gzzn/",
    ],
    "GS": [
        "https://gzw.gansu.gov.cn/",
        "http://www.gansu.gov.cn/col/col115/",
    ],
    "QH": [
        "https://gzw.qinghai.gov.cn/",
        "http://www.qinghai.gov.cn/xxgk/xxgk/s_gkml/sbm/gzw/",
    ],
}

for code, urls in STILL_BLOCKED.items():
    province_names = {"TJ":"天津","HE":"河北","SH":"上海","JS":"江苏","HB":"湖北","SN":"陕西","GS":"甘肃","QH":"青海"}
    print(f"\n[{code}] {province_names[code]}")
    for url in urls:
        print(f"  Trying: {url}")
        try:
            text = fetch(url, timeout=12)
            names = find_enterprise_names(text)
            title_m = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
            title = title_m.group(1).strip() if title_m else ""
            print(f"    ✓ {len(text)} bytes, title: {title[:60]}")
            if names:
                print(f"    Enterprise names ({len(names)}):")
                for n in names[:20]:
                    print(f"      - {n}")
            # Check for enterprise-related links
            ent_links = extract_links_and_text(text, [r'监管企业', r'企业名录', r'jgqy', r'qyml', r'ssqy', r'省属企业', r'国企'])
            if ent_links:
                print(f"    Enterprise links:")
                for h, t in ent_links[:10]:
                    print(f"      {t} → {h}")
            break
        except Exception as e:
            print(f"    ✗ {e}")
