const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('file:///C:/Users/ASUS/guozi_skill_prep/site/index.html');
  await page.waitForFunction(() => {
    const el = document.getElementById('idx-entities');
    return el && el.textContent && el.textContent !== '—' && el.textContent !== '加载失败';
  }, { timeout: 10000 });

  const homepage = await page.evaluate(() => ({
    entities: document.getElementById('idx-entities')?.textContent,
    monthly: document.getElementById('idx-monthly')?.textContent,
    policies: document.getElementById('idx-policies')?.textContent,
    budget: document.getElementById('idx-budget')?.textContent,
  }));

  await page.goto('file:///C:/Users/ASUS/guozi_skill_prep/site/pages/operations.html');
  await page.waitForFunction(() => {
    const el = document.getElementById('monthly-content');
    return el && el.textContent && !el.textContent.includes('加载中');
  }, { timeout: 10000 });

  const operations = await page.evaluate(() => ({
    chartHint: Array.from(document.querySelectorAll('p'))
      .map((node) => node.textContent || '')
      .find((text) => text.includes('图表字段')) || '',
    tableLoaded: document.getElementById('monthly-content')?.textContent.includes('利润总额') || false,
  }));

  console.log(JSON.stringify({ homepage, operations }, null, 2));
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});