# -*- coding: utf-8 -*-
"""
Phase 5: Try CORRECT URLs discovered from central SASAC page.
"""
import urllib.request
import ssl
import re
import time

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
        if len(name) >= 6 and not re.search(r'主办|版权|网站|邮箱|电话|备案|技术支持|招标|咨询|投资主体|建设服务|关于印发|关于对|关于支持', name):
            names.add(name)
    return sorted(names)


def extract_links(html, base_url, patterns):
    results = []
    for m in re.finditer(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, text = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 2:
            for pat in patterns:
                if re.search(pat, text) or re.search(pat, href):
                    results.append((href, text))
                    break
    return results


# Correct URLs from central SASAC:
CORRECTED = {
    "TJ": ("天津", ["http://sasac.tj.gov.cn/", "https://sasac.tj.gov.cn/"]),
    "HE": ("河北", ["http://hbsa.hebei.gov.cn/", "https://hbsa.hebei.gov.cn/"]),
    "SH": ("上海", ["http://www.gzw.sh.gov.cn/", "https://www.gzw.sh.gov.cn/"]),
    "JS": ("江苏", ["http://jsgzw.jiangsu.gov.cn/", "https://jsgzw.jiangsu.gov.cn/"]),
    "SN": ("陕西", ["http://sxgz.shaanxi.gov.cn/", "https://sxgz.shaanxi.gov.cn/"]),
    "FJ": ("福建", ["http://gzw.fujian.gov.cn/", "https://gzw.fujian.gov.cn/"]),
    "BT": ("新疆兵团", ["http://gyzc.xjbt.gov.cn/", "https://gyzc.xjbt.gov.cn/"]),
}

for code, (name, urls) in CORRECTED.items():
    print(f"\n{'='*60}")
    print(f"[{code}] {name}")
    print(f"{'='*60}")
    for url in urls:
        print(f"  Trying: {url}")
        try:
            html = fetch(url, timeout=15)
            title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
            title = title_m.group(1).strip() if title_m else "(no title)"
            print(f"  ✓ {len(html)} bytes, Title: {title[:80]}")

            # Find enterprise-related links
            ent_links = extract_links(html, url, 
                [r'监管企业', r'企业名录', r'出资企业', r'jgqy', r'qyml', r'ssqy', r'省属企业', r'国企'])
            if ent_links:
                print(f"  Enterprise-related links:")
                for h, t in ent_links[:15]:
                    print(f"    {t:50s} → {h}")

            # Find enterprise names  
            names = find_enterprise_names(html)
            if names:
                print(f"  Enterprise names ({len(names)}):")
                for n in names[:30]:
                    print(f"    - {n}")

            # If we found enterprise list link, try to fetch it
            for h, t in ent_links[:5]:
                if '名录' in t or 'qyml' in h or 'jgqy' in h or '企业名单' in t or 'ssqy' in h:
                    if h.startswith('/'):
                        ent_url = url.rstrip('/') + h
                    elif h.startswith('http'):
                        ent_url = h
                    elif h.startswith('./'):
                        ent_url = url.rstrip('/') + h[1:]
                    else:
                        continue
                    print(f"\n  Fetching enterprise list: {ent_url}")
                    try:
                        html2 = fetch(ent_url, timeout=15)
                        names2 = find_enterprise_names(html2)
                        links2 = extract_links(html2, ent_url, [r'集团', r'公司'])
                        if names2:
                            print(f"  Enterprise names from list ({len(names2)}):")
                            for n in names2:
                                print(f"    - {n}")
                        if links2:
                            print(f"  Enterprise links ({len(links2)}):")
                            for h2, t2 in links2[:30]:
                                print(f"    {t2}")
                    except Exception as e2:
                        print(f"  Error fetching list: {e2}")
                    break

            break  # Success, don't try next URL

        except Exception as e:
            print(f"  ✗ {e}")
        time.sleep(0.3)

# ─── Also try WAF bypass for 412 sites ──────────────────────
print("\n" + "=" * 60)
print("WAF bypass for 412 sites (Gansu, Qinghai, Hubei)")
print("=" * 60)

import http.client

def fetch_with_cookie_bounce(host, path="/", use_https=True):
    """Some WAFs set a cookie on first request and expect it on retry."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        if use_https:
            conn = http.client.HTTPSConnection(host, timeout=15, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, timeout=15)

        # First request to get cookies
        conn.request("GET", path, headers={
            "Host": host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "identity",
        })
        resp = conn.getresponse()
        body1 = resp.read()
        cookies_raw = resp.getheader("Set-Cookie", "")
        status1 = resp.status
        conn.close()

        print(f"    First request: status={status1}, cookies={cookies_raw[:100]}")

        if status1 == 412 and cookies_raw:
            # Parse cookies for replay
            cookie_parts = []
            for c in cookies_raw.split(","):
                c = c.strip()
                name_val = c.split(";")[0].strip()
                if "=" in name_val:
                    cookie_parts.append(name_val)
            cookie_str = "; ".join(cookie_parts)
            
            # Also check if the 412 page contains JS that sets cookies
            text1 = ""
            for enc in ["utf-8", "gbk", "gb18030"]:
                try:
                    text1 = body1.decode(enc)
                    break
                except:
                    pass
            
            # Look for JS-based cookie setting
            js_cookies = re.findall(r'document\.cookie\s*=\s*["\']([^"\']+)', text1)
            if js_cookies:
                for jc in js_cookies:
                    name_val = jc.split(";")[0].strip()
                    if "=" in name_val:
                        cookie_parts.append(name_val)
                cookie_str = "; ".join(cookie_parts)
                print(f"    JS cookies found: {js_cookies[:3]}")

            # Look for meta refresh or JS redirect
            redirect = re.search(r'location\.href\s*=\s*["\']([^"\']+)', text1)
            if redirect:
                print(f"    JS redirect found: {redirect.group(1)}")

            if cookie_str:
                print(f"    Retrying with cookies: {cookie_str[:80]}")
                time.sleep(1)

                if use_https:
                    conn2 = http.client.HTTPSConnection(host, timeout=15, context=ctx)
                else:
                    conn2 = http.client.HTTPConnection(host, timeout=15)

                conn2.request("GET", path, headers={
                    "Host": host,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Accept-Encoding": "identity",
                    "Cookie": cookie_str,
                    "Referer": f"{'https' if use_https else 'http'}://{host}/",
                })
                resp2 = conn2.getresponse()
                body2 = resp2.read()
                status2 = resp2.status
                conn2.close()

                print(f"    Second request: status={status2}, size={len(body2)}")
                if status2 == 200:
                    text2 = ""
                    for enc in ["utf-8", "gbk", "gb18030"]:
                        try:
                            text2 = body2.decode(enc)
                            break
                        except:
                            pass
                    title_m = re.search(r'<title[^>]*>(.*?)</title>', text2, re.I | re.S)
                    title = title_m.group(1).strip() if title_m else ""
                    print(f"    ✓ Title: {title[:80]}")
                    names = find_enterprise_names(text2)
                    if names:
                        print(f"    Enterprises ({len(names)}):")
                        for n in names[:20]:
                            print(f"      - {n}")
                    return text2
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


waf_sites = [
    ("gzw.gansu.gov.cn", "甘肃", "GS"),
    ("gzw.qinghai.gov.cn", "青海", "QH"),
    ("gzw.hubei.gov.cn", "湖北", "HB"),
]

for host, name, code in waf_sites:
    print(f"\n[{code}] {name} ({host})")
    for use_https in [False, True]:
        proto = "HTTPS" if use_https else "HTTP"
        print(f"  {proto}:")
        result = fetch_with_cookie_bounce(host, "/", use_https=use_https)
        if result:
            break
