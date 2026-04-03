# -*- coding: utf-8 -*-
"""
Attempt to fetch blocked provincial SASAC websites using Python with
proper browser-like headers and SSL workarounds.
"""
import urllib.request
import urllib.error
import ssl
import re
import sys
import time

# Blocked provinces to try
TARGETS = {
    "TJ": ("天津", "http://gzw.tj.gov.cn"),
    "HE": ("河北", "http://gzw.hebei.gov.cn"),
    "SH": ("上海", "http://gzw.sh.gov.cn"),
    "JS": ("江苏", "http://gzw.js.gov.cn"),
    "JX": ("江西", "http://gzw.jx.gov.cn"),
    "HB": ("湖北", "http://gzw.hubei.gov.cn"),
    "GX": ("广西", "http://gzw.gx.gov.cn"),
    "XZ": ("西藏", "http://gzw.xizang.gov.cn"),
    "SN": ("陕西", "http://gzw.shaanxi.gov.cn"),
    "GS": ("甘肃", "http://gzw.gansu.gov.cn"),
    "QH": ("青海", "http://gzw.qinghai.gov.cn"),
    "BT": ("新疆兵团", "http://bt.xinjiang.gov.cn"),
}

# Also try HTTPS variants
HTTPS_ALTS = {
    "TJ": "https://gzw.tj.gov.cn",
    "HE": "https://gzw.hebei.gov.cn",
    "SH": "https://gzw.sh.gov.cn",
    "JS": "https://gzw.js.gov.cn",
    "JX": "https://gzw.jx.gov.cn",
    "HB": "https://gzw.hubei.gov.cn",
    "GX": "https://gzw.gx.gov.cn",
    "XZ": "https://gzw.xizang.gov.cn",
    "SN": "https://gzw.shaanxi.gov.cn",
    "GS": "https://gzw.gansu.gov.cn",
    "QH": "https://gzw.qinghai.gov.cn",
    "BT": "https://bt.xinjiang.gov.cn",
}

# Some provinces use different domain patterns
EXTRA_URLS = {
    "SN": ["http://gzw.shaanxi.gov.cn/", "https://gzw.sn.gov.cn/"],
    "GS": ["http://gzw.gs.gov.cn/", "https://gzw.gs.gov.cn/"],
    "QH": ["http://gzw.qh.gov.cn/", "https://gzw.qh.gov.cn/"],
    "BT": ["http://gzw.btxjbt.gov.cn/", "http://www.xjbt.gov.cn/"],
    "GX": ["http://gzw.gxzf.gov.cn/", "https://gzw.gxzf.gov.cn/"],
    "XZ": ["http://gzw.xz.gov.cn/", "https://gzw.xz.gov.cn/"],
    "JX": ["http://gzw.jiangxi.gov.cn/", "https://gzw.jiangxi.gov.cn/"],
    "HB": ["http://gzw.hb.gov.cn/", "https://gzw.hb.gov.cn/"],
    "JS": ["http://gzw.jiangsu.gov.cn/", "https://gzw.jiangsu.gov.cn/"],
    "HE": ["http://gzw.he.gov.cn/", "https://gzw.he.gov.cn/"],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
}


def try_fetch(url, timeout=15):
    """Try to fetch a URL with browser-like headers. Returns (status, content_length, title, snippet)."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        data = resp.read()
        # Try multiple encodings
        for enc in ["utf-8", "gbk", "gb2312", "gb18030", "latin-1"]:
            try:
                text = data.decode(enc)
                break
            except (UnicodeDecodeError, LookupError):
                text = None
        if text is None:
            text = data.decode("latin-1")

        # Extract title
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        title = m.group(1).strip() if m else "(no title)"

        # Look for enterprise-related links
        ent_patterns = [
            r"监管企业", r"出资企业", r"企业名录", r"省属企业", r"国企",
            r"企业名单", r"jgqy", r"qyml", r"ssqy",
        ]
        ent_links = []
        for pat in ent_patterns:
            for match in re.finditer(rf'href=["\']([^"\']*{pat}[^"\']*)["\']', text, re.I):
                ent_links.append(match.group(1))
            if pat in text:
                ent_links.append(f"[text contains '{pat}']")

        return resp.status, len(data), title, list(set(ent_links))[:10]
    except urllib.error.HTTPError as e:
        return e.code, 0, str(e), []
    except urllib.error.URLError as e:
        return -1, 0, str(e.reason), []
    except Exception as e:
        return -2, 0, str(e), []


def main():
    results = {}
    for code, (name, url) in TARGETS.items():
        urls_to_try = [url]
        if code in HTTPS_ALTS:
            urls_to_try.append(HTTPS_ALTS[code])
        if code in EXTRA_URLS:
            urls_to_try.extend(EXTRA_URLS[code])

        print(f"\n{'='*60}")
        print(f"[{code}] {name}")
        print(f"{'='*60}")

        best = None
        for u in urls_to_try:
            print(f"  Trying: {u}")
            status, size, title, links = try_fetch(u)
            print(f"    Status: {status}, Size: {size}, Title: {title[:80]}")
            if links:
                print(f"    Enterprise links found: {links[:5]}")

            if status == 200 and size > 1000:
                best = (u, status, size, title, links)
                break  # Success, stop trying alternatives
            time.sleep(0.5)

        if best:
            results[code] = best
            print(f"  ✓ SUCCESS: {best[0]} ({best[2]} bytes)")
        else:
            results[code] = None
            print(f"  ✗ ALL FAILED for {name}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    ok = [k for k, v in results.items() if v is not None]
    fail = [k for k, v in results.items() if v is None]
    print(f"Success: {len(ok)}/{len(results)}")
    for code in ok:
        url, status, size, title, links = results[code]
        name = TARGETS[code][0]
        print(f"  ✓ [{code}] {name}: {url} ({size} bytes) - links: {links[:3]}")
    print(f"Failed: {len(fail)}/{len(results)}")
    for code in fail:
        name = TARGETS[code][0]
        print(f"  ✗ [{code}] {name}")


if __name__ == "__main__":
    main()
