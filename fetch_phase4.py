# -*- coding: utf-8 -*-
"""
Phase 4: Extract correct SASAC URLs from the central SASAC's local list page,
then try those URLs.
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


# ─── Extract all links from central SASAC page ─────────────
print("=" * 60)
print("Central SASAC local SASAC list page")
print("=" * 60)

try:
    html = fetch("http://www.sasac.gov.cn/n4422011/n17627531/c17633273/content.html")
    # Extract all href links
    links = []
    for m in re.finditer(r'href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href = m.group(1).strip()
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and '国资' in text:
            links.append((href, text))
            print(f"  {text:30s} → {href}")
    
    if not links:
        print("  No SASAC links found with '国资' in text. Looking for all links:")
        for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.I):
            href = m.group(1)
            if 'gzw' in href or 'gov.cn' in href:
                print(f"  → {href}")
    
    # Also search for gzw URLs in the raw text
    print("\nAll gzw*.gov.cn URLs in page:")
    for m in re.finditer(r'https?://gzw[.\w]*\.gov\.cn[/\w]*', html, re.I):
        print(f"  {m.group(0)}")

    # Also search for any gov.cn URLs 
    print("\nAll unique gov.cn domains in page:")
    domains = set()
    for m in re.finditer(r'https?://([\w.]+\.gov\.cn)', html, re.I):
        domains.add(m.group(1))
    for d in sorted(domains):
        print(f"  {d}")

except Exception as e:
    print(f"Error: {e}")


# ─── Try to use open_browser_page approach via HTTP requests ────
# Some sites return 412/502 to plain HTTP but may respond to specific
# cookie/session initialization

print("\n" + "=" * 60)
print("Trying sites with cookie handling and HTTP/1.1")
print("=" * 60)

import http.client

def fetch_http11(host, path="/", use_https=True, timeout=15):
    """Low-level HTTP/1.1 fetch with explicit headers."""
    try:
        if use_https:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(host, timeout=timeout, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, timeout=timeout)
        
        conn.request("GET", path, headers={
            "Host": host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        resp = conn.getresponse()
        status = resp.status
        body = resp.read()
        
        # Check for redirect
        if status in (301, 302, 307, 308):
            loc = resp.getheader("Location", "")
            return status, 0, f"Redirect → {loc}", ""
        
        # Handle cookies - some sites need cookie bounce
        cookies = resp.getheader("Set-Cookie", "")
        
        # Decode body
        text = ""
        if body:
            for enc in ["utf-8", "gbk", "gb2312", "gb18030"]:
                try:
                    text = body.decode(enc)
                    break
                except:
                    pass
            if not text:
                text = body.decode("latin-1")
        
        conn.close()
        return status, len(body), cookies[:100] if cookies else "(no cookies)", text
    except Exception as e:
        return -1, 0, str(e), ""


blocked_sites = [
    ("gzw.tj.gov.cn", "天津", "TJ"),
    ("gzw.hebei.gov.cn", "河北", "HE"),
    ("gzw.sh.gov.cn", "上海", "SH"),
    ("gzw.hubei.gov.cn", "湖北", "HB"),
    ("gzw.shaanxi.gov.cn", "陕西", "SN"),
    ("gzw.gansu.gov.cn", "甘肃", "GS"),
    ("gzw.qinghai.gov.cn", "青海", "QH"),
    ("gzw.xizang.gov.cn", "西藏", "XZ"),
]

for host, name, code in blocked_sites:
    print(f"\n[{code}] {name} ({host})")
    for use_https in [False, True]:
        proto = "HTTPS" if use_https else "HTTP"
        status, size, cookies, text = fetch_http11(host, "/", use_https=use_https)
        print(f"  {proto}: status={status}, size={size}, cookies={cookies[:60]}")
        if status == 200 and size > 1000:
            title_m = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
            title = title_m.group(1).strip() if title_m else "(no title)"
            print(f"  ✓ Title: {title}")
            names = find_enterprise_names(text)
            if names:
                print(f"  Enterprises: {len(names)}")
                for n in names[:10]:
                    print(f"    - {n}")
            break
        elif status in (301, 302):
            print(f"  → Redirect: {cookies}")
