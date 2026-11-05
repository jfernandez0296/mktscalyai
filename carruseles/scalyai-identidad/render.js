// Exporta cada lámina del carrusel a PNG 1080×1350 (4:5, Instagram).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'carrusel.html'));
  await p.evaluate(() => document.fonts.ready);
  const n = await p.locator('section.slide').count();
  for (let i = 1; i <= n; i++) await p.locator('#slide-' + i).screenshot({ path: path.join(__dirname, 'slide-' + i + '.png') });
  await b.close();
})();
