// Tager skærmbilleder af telefonens skærm i Lysning-prototypen.
import puppeteer from 'puppeteer-core';

const URL = process.env.PROTOTYPE_URL || 'http://localhost:8766/Lysning%20App.html';
const OUT = process.argv[2] || 'screens';
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true,
  defaultViewport: { width: 1280, height: 950, deviceScaleFactor: 2 },
});
const page = await browser.newPage();
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function screen() {
  return page.evaluateHandle(() => [...document.querySelectorAll('div')].find(d => {
    const r = d.getBoundingClientRect();
    return r.width === 390 && r.height === 844 && getComputedStyle(d).overflow === 'hidden';
  }));
}
async function click(text, { exact = false, last = false } = {}) {
  const ok = await page.evaluate((text, exact, last) => {
    const els = [...document.querySelectorAll('button, a, [role=button], div, span')]
      .filter(e => {
        const t = (e.innerText || '').trim();
        const r = e.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && (exact ? t === text : t.includes(text));
      });
    // vælg det inderste element
    const inner = els.filter(e => !els.some(o => o !== e && e.contains(o)));
    const el = last ? inner[inner.length - 1] : inner[0];
    if (!el) return false;
    el.click();
    return true;
  }, text, exact, last);
  if (!ok) throw new Error('Fandt ikke: ' + text);
  await sleep(900);
}
async function tab(name) {
  await click(name, { exact: true, last: true });
  const intro = await page.evaluate(() => [...document.querySelectorAll('button, div')].some(e => (e.innerText || '').trim() === 'Kom i gang' && e.getBoundingClientRect().width > 0));
  if (intro) await click('Kom i gang', { exact: true, last: true });
}
async function scrollTop() {
  await page.evaluate(() => document.querySelectorAll('div').forEach(d => { if (d.scrollTop) d.scrollTop = 0; }));
  await sleep(300);
}
async function shot(name) {
  await scrollTop();
  const el = await screen();
  await el.screenshot({ path: `${OUT}/${name}.png`, omitBackground: true });
  console.log('gemt', name);
}
async function start(role) {
  await page.goto(URL, { waitUntil: 'networkidle0' });
  await sleep(1500);
  await click('Spring til appen · ' + role, { exact: true });
  await sleep(800);
}

const step = process.argv[3] || 'all';
if (step === 'probe') {
  await start(process.argv[4] || 'ramt');
  for (const t of (process.argv[5] || '').split('|').filter(Boolean)) await click(t, { exact: true });
  const el = await screen();
  await el.screenshot({ path: `${OUT}/probe.png` });
  console.log(await page.evaluate(() => [...document.querySelectorAll('div')].find(d => d.getBoundingClientRect().width === 390 && d.getBoundingClientRect().height === 844).innerText.slice(0, 800)));
} else {
  await start('ramt');
  await shot('ramt_hjem');
  await tab('Helbred');
  await shot('ramt_helbred');
  await click('Din vej tilbage til arbejdet');
  await shot('ramt_arbejdslog');
  await start('ramt');
  await tab('Træning');
  await shot('ramt_traening');
  await tab('Viden');
  await shot('ramt_viden');
  await start('ramt');
  await click('Din profil', { exact: true });
  await shot('ramt_profil');
  await start('ramt');
  await tab('Helbred');
  await click('Start ·');
  await shot('ramt_spoergeskema');
  await start('pårørende');
  await shot('paar_hjem');
  await tab('Helbred');
  await shot('paar_helbred');
}
await browser.close();
