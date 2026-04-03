const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const targets = [
  { code: 'HB', province: '湖北', url: 'http://gzw.hubei.gov.cn/' },
  { code: 'GS', province: '甘肃', url: 'http://gzw.gansu.gov.cn/' },
  { code: 'QH', province: '青海', url: 'http://gzw.qinghai.gov.cn/' },
  { code: 'XZ', province: '西藏', url: 'http://gzw.xizang.gov.cn/' },
];

const candidatePathsByCode = {
  HB: ['/', '/index.html', '/gzw/', '/zwgk/', '/xxgk/'],
  GS: ['/', '/index.html', '/gzw/', '/zwgk/', '/xxgk/'],
  QH: ['/', '/index.html', '/gzw/', '/xxgk/', '/xxgk/xxgk/'],
  XZ: ['/', '/index.html'],
};

const waitMs = Number(process.env.WAIT_MS || 15000);
const headless = process.env.HEADLESS !== 'false';

function pickEnterpriseCandidates(text) {
  const matches = text.match(/[\u4e00-\u9fff（）()]+(?:集团|有限公司|有限责任公司|股份有限公司)/g) || [];
  const blacklist = /网站|版权|备案|技术支持|国务院|国有资产监督管理委员会|主办单位|京公网安备|联系我们|政务服务/;
  return [...new Set(matches.filter((name) => name.length >= 6 && !blacklist.test(name)))].slice(0, 80);
}

async function inspectTarget(browser, target) {
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    locale: 'zh-CN',
    viewport: { width: 1440, height: 1080 },
    ignoreHTTPSErrors: true,
  });
  const page = await context.newPage();
  const log = [];

  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
    Object.defineProperty(navigator, 'language', { get: () => 'zh-CN' });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(navigator, 'plugins', {
      get: () => [{ name: 'Chrome PDF Viewer' }, { name: 'Microsoft Edge PDF Viewer' }],
    });
    window.chrome = { runtime: {} };
  });

  page.on('response', (resp) => {
    if (resp.url().startsWith(target.url.replace(/\/$/, ''))) {
      log.push({ type: 'response', url: resp.url(), status: resp.status() });
    }
  });

  page.on('requestfailed', (req) => {
    log.push({ type: 'failed', url: req.url(), error: req.failure()?.errorText || 'unknown' });
  });

  const result = {
    ...target,
    ok: false,
    finalUrl: '',
    title: '',
    statusSummary: [],
    enterpriseCandidates: [],
    linkHints: [],
    cookies: [],
    probeEvents: [],
    consoleMessages: [],
    pageErrors: [],
    candidateChecks: [],
    htmlPath: '',
    screenshotPath: '',
    error: '',
  };

  try {
    page.on('console', (msg) => {
      result.consoleMessages.push({ type: msg.type(), text: msg.text() });
    });

    page.on('pageerror', (error) => {
      result.pageErrors.push(String(error));
    });

    await page.addInitScript(() => {
      window.__probeEvents = [];

      const record = (type, detail) => {
        window.__probeEvents.push({ type, detail, href: location.href, ts: Date.now() });
      };

      const cookieDescriptor = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
      if (cookieDescriptor && cookieDescriptor.set && cookieDescriptor.get) {
        Object.defineProperty(Document.prototype, 'cookie', {
          configurable: true,
          enumerable: cookieDescriptor.enumerable,
          get() {
            return cookieDescriptor.get.call(this);
          },
          set(value) {
            record('cookie-set', value);
            return cookieDescriptor.set.call(this, value);
          },
        });
      }

      const originalFetch = window.fetch;
      window.fetch = async (...args) => {
        record('fetch', args[0]);
        return originalFetch(...args);
      };

      const originalOpen = XMLHttpRequest.prototype.open;
      XMLHttpRequest.prototype.open = function open(method, url, ...rest) {
        record('xhr-open', { method, url });
        return originalOpen.call(this, method, url, ...rest);
      };

      const originalAssign = window.location.assign.bind(window.location);
      window.location.assign = (value) => {
        record('location-assign', value);
        return originalAssign(value);
      };

      const originalReplace = window.location.replace.bind(window.location);
      window.location.replace = (value) => {
        record('location-replace', value);
        return originalReplace(value);
      };

      const originalReload = window.location.reload.bind(window.location);
      window.location.reload = (...args) => {
        record('location-reload', 'reload');
        return originalReload(...args);
      };
    });

    const resp = await page.goto(target.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(waitMs);

    result.ok = true;
    result.finalUrl = page.url();
    result.title = await page.title();
    result.statusSummary = log.slice(-10);
    result.cookies = await context.cookies();
    result.probeEvents = await page.evaluate(() => window.__probeEvents || []).catch(() => []);

    const html = await page.content();
    const text = await page.locator('body').innerText().catch(() => '');
    const links = await page.locator('a').evaluateAll((nodes) => nodes.map((node) => ({
      text: (node.textContent || '').trim(),
      href: node.href || '',
    })));

    const outDir = path.join(process.cwd(), 'tmp_playwright');
    fs.mkdirSync(outDir, { recursive: true });
    result.htmlPath = path.join(outDir, `${target.code}.html`);
    result.screenshotPath = path.join(outDir, `${target.code}.png`);
    fs.writeFileSync(result.htmlPath, html, 'utf8');
    await page.screenshot({ path: result.screenshotPath, fullPage: true });

    result.enterpriseCandidates = pickEnterpriseCandidates(text);
    result.linkHints = links
      .filter((item) => item.text && /(企业|监管|名录|集团|公司|国企|出资)/.test(item.text))
      .slice(0, 40);

    const candidatePaths = candidatePathsByCode[target.code] || ['/'];
    for (const candidatePath of candidatePaths) {
      const candidateUrl = new URL(candidatePath, target.url).toString();
      const candidatePage = await context.newPage();
      const candidateResult = {
        url: candidateUrl,
        status: null,
        finalUrl: '',
        title: '',
        textSample: '',
      };
      try {
        const candidateResp = await candidatePage.goto(candidateUrl, {
          waitUntil: 'domcontentloaded',
          timeout: 30000,
        });
        await candidatePage.waitForTimeout(5000);
        candidateResult.status = candidateResp ? candidateResp.status() : null;
        candidateResult.finalUrl = candidatePage.url();
        candidateResult.title = await candidatePage.title();
        const candidateText = await candidatePage.locator('body').innerText().catch(() => '');
        candidateResult.textSample = candidateText.slice(0, 300);
      } catch (candidateError) {
        candidateResult.error = String(candidateError);
        candidateResult.finalUrl = candidatePage.url();
      } finally {
        await candidatePage.close();
      }
      result.candidateChecks.push(candidateResult);
    }

    if (resp) {
      result.initialStatus = resp.status();
    }
  } catch (error) {
    result.error = String(error);
    result.finalUrl = page.url();
    result.title = await page.title().catch(() => '');
    result.statusSummary = log.slice(-10);
  } finally {
    await context.close();
  }

  return result;
}

(async () => {
  const browser = await chromium.launch({
    headless,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const results = [];
  for (const target of targets) {
    results.push(await inspectTarget(browser, target));
  }
  await browser.close();
  const output = path.join(process.cwd(), 'tmp_playwright', 'official_probe_results.json');
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, JSON.stringify(results, null, 2), 'utf8');
  console.log(JSON.stringify(results, null, 2));
})();