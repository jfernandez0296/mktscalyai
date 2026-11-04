// Exporta el flyer a PNG (1080×1350) y PDF vectorial del mismo tamaño.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'flyer.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, 'flyer-encatalogo.png') });
  await p.pdf({ path: path.join(__dirname, 'flyer-encatalogo.pdf'), width: '1080px', height: '1350px', printBackground: true });
  await b.close();
})();
