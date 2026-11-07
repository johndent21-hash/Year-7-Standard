// Render HTML files to PDF with Chromium (Playwright). Usage: node render.js in.html out.pdf [--transparent]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const jobs = [];
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i += 3) jobs.push([args[i], args[i + 1], args[i + 2] === 'T']);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [inp, out, transparent] of jobs) {
    await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 60000 });
    const warn = await page.evaluate(() => document.body.dataset.warn || '');
    if (warn) console.log('LAYOUT WARNINGS in ' + inp + ':\n' + warn);
    await page.pdf({ path: out, format: 'A4', printBackground: true, omitBackground: !!transparent,
                     margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    console.log('rendered ' + out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
