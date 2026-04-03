const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const errors = [];
  page.on('console', msg => { if(msg.type()==='error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('PAGE_ERROR: ' + err.message));

  const failedReqs = [];
  page.on('response', resp => { if(!resp.ok()) failedReqs.push(resp.url() + ' ' + resp.status()); });

  await page.goto('http://localhost:4174/index.html', { waitUntil: 'networkidle' });

  const kpis = await page.evaluate(() => {
    return {
      entities: document.getElementById('idx-entities')?.textContent,
      monthly: document.getElementById('idx-monthly')?.textContent,
      policies: document.getElementById('idx-policies')?.textContent,
      budget: document.getElementById('idx-budget')?.textContent,
    };
  });

  console.log('KPIs:', JSON.stringify(kpis));
  console.log('Console errors:', JSON.stringify(errors));
  console.log('Failed requests:', JSON.stringify(failedReqs));

  await browser.close();
})();
