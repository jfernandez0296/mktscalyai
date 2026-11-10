// Exporta cada lámina de cada carrusel a PNG 1080×1350.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const d of fs.readdirSync(__dirname).filter(f => fs.existsSync(path.join(__dirname, f, 'carrusel.html')))) {
    await p.goto('file://' + path.join(__dirname, d, 'carrusel.html')); await p.evaluate(() => document.fonts.ready);
    const n = await p.locator('section.slide').count();
    for (let i = 1; i <= n; i++) await p.locator('#slide-' + i).screenshot({ path: path.join(__dirname, d, 'slide-' + i + '.png') });
    console.log(d, n);
  }
  await b.close();
})();
