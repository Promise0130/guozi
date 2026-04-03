# -*- coding: utf-8 -*-
"""Phase 6: Fetch enterprise list pages for newly accessible provinces."""
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
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标条件|关于印发|关于对|关于支持|建设服务|合胜合|拓尔通|投资主体', name):
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


# ─── 天津 委管企业名录 ────────────────────────────
print("="*60)
print("[TJ] 天津 - 委管企业名录")
print("="*60)
try:
    html = fetch("https://sasac.tj.gov.cn/GZJG8342/GZFM8996/WGQYML2210/")
    names = find_enterprise_names(html)
    links = extract_links(html, [r'集团', r'公司'])
    print(f"委管企业 names ({len(names)}):")
    for n in names:
        print(f"  - {n}")
    if links:
        print(f"\n委管企业 links ({len(links)}):")
        for h, t in links[:30]:
            print(f"  {t}")
except Exception as e:
    print(f"Error: {e}")

# ─── 河北 监管企业 ──────────────────────────────────
print("\n" + "="*60)
print("[HE] 河北 - 监管企业")
print("="*60)
try:
    html = fetch("http://hbsa.hebei.gov.cn/")
    # Find enterprise list links
    ent_links = extract_links(html, [r'监管企业', r'企业名录', r'qyml', r'jgqy', r'ssqy'])
    print("Enterprise links:")
    for h, t in ent_links[:20]:
        print(f"  {t:40s} → {h}")
    # Look for enterprise subsection
    names = find_enterprise_names(html)
    print(f"\nNames ({len(names)}):")
    for n in names[:30]:
        print(f"  - {n}")

    # Try common paths for enterprise list
    for path in ["/GZJG/JGQY/", "/jgqy/", "/ssqy/", "/GZJG418/JGQY/", "/gqjj/"]:
        url = "http://hbsa.hebei.gov.cn" + path
        try:
            h2 = fetch(url, timeout=10)
            n2 = find_enterprise_names(h2)
            l2 = extract_links(h2, [r'集团', r'公司'])
            if n2 or l2:
                print(f"\n{url}:")
                if n2:
                    for n in n2:
                        print(f"  - {n}")
                if l2:
                    for h, t in l2[:30]:
                        print(f"  link: {t}")
                break
        except:
            pass
except Exception as e:
    print(f"Error: {e}")

# ─── 江苏 省属企业 ──────────────────────────────────
print("\n" + "="*60)
print("[JS] 江苏 - 省属企业")
print("="*60)
try:
    html = fetch("http://jsgzw.jiangsu.gov.cn/col/col11779/index.html")
    names = find_enterprise_names(html)
    links = extract_links(html, [r'集团', r'公司'])
    print(f"Names ({len(names)}):")
    for n in names:
        print(f"  - {n}")
    if links:
        print(f"\nLinks ({len(links)}):")
        for h, t in links[:30]:
            print(f"  {t}")
except Exception as e:
    print(f"Error: {e}")

# ─── 上海 企业名录/list ────────────────────────────
print("\n" + "="*60)
print("[SH] 上海 - 省属企业")
print("="*60)
try:
    # Try common paths for enterprise directories
    for path in ["/ssqy/", "/jgqy/", "/gqzc/", "/shgzw_wsbs_ssqy/", "/shgzw_gzgk_ssqy/"]:
        url = "http://www.gzw.sh.gov.cn" + path
        print(f"  Trying: {url}")
        try:
            html = fetch(url, timeout=10)
            title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
            title = title_m.group(1).strip() if title_m else ""
            names = find_enterprise_names(html)
            links = extract_links(html, [r'集团', r'公司'])
            if title:
                print(f"    Title: {title[:80]}")
            if names:
                print(f"    Names ({len(names)}):")
                for n in names[:20]:
                    print(f"      - {n}")
            if links:
                print(f"    Links ({len(links)}):")
                for h, t in links[:20]:
                    print(f"      {t}")
            if names or links:
                break
        except Exception as e:
            print(f"    {e}")
except Exception as e:
    print(f"Error: {e}")

# ─── 陕西 省属企业 ──────────────────────────────────
print("\n" + "="*60)
print("[SN] 陕西 - 省属企业")
print("="*60)
try:
    # Find enterprise list page from homepage
    html = fetch("http://sxgz.shaanxi.gov.cn/")
    for path in ["/sy/gqzc/", "/gzgk/ssqy/", "/gk/ssqy/", "/gzgk/jgqy/"]:
        url = "http://sxgz.shaanxi.gov.cn" + path
        print(f"  Trying: {url}")
        try:
            html2 = fetch(url, timeout=10)
            title_m = re.search(r'<title[^>]*>(.*?)</title>', html2, re.I | re.S)
            title = title_m.group(1).strip() if title_m else ""
            names = find_enterprise_names(html2)
            links = extract_links(html2, [r'集团', r'公司'])
            if title:
                print(f"    Title: {title[:80]}")
            if names:
                print(f"    Names ({len(names)}):")
                for n in names[:20]:
                    print(f"      - {n}")
            if links:
                print(f"    Links ({len(links)}):")
                for h, t in links[:20]:
                    print(f"      {t}")
            if (names and len(names) > 3) or (links and len(links) > 3):
                break
        except Exception as e:
            print(f"    {e}")
except Exception as e:
    print(f"Error: {e}")

# ─── 新疆兵团 企业名录 ────────────────────────────
print("\n" + "="*60)
print("[BT] 新疆兵团 - 监管企业")
print("="*60)
try:
    html = fetch("http://gyzc.xjbt.gov.cn/")
    ent_links = extract_links(html, [r'监管', r'企业', r'jgqy', r'qyml'])
    print("Enterprise links:")
    for h, t in ent_links[:10]:
        print(f"  {t:40s} → {h}")

    names = find_enterprise_names(html)
    if names:
        print(f"\nNames ({len(names)}):")
        for n in names:
            print(f"  - {n}")

    for path in ["/col/col9/", "/jgqy/", "/ssqy/", "/gzgk/ssqy/"]:
        url = "http://gyzc.xjbt.gov.cn" + path
        try:
            h2 = fetch(url, timeout=10)
            n2 = find_enterprise_names(h2)
            l2 = extract_links(h2, [r'集团', r'公司'])
            if n2 or l2:
                print(f"\n{url}:")
                for n in n2:
                    print(f"  - {n}")
                for h, t in l2[:20]:
                    print(f"  link: {t}")
                break
        except:
            pass
except Exception as e:
    print(f"Error: {e}")
