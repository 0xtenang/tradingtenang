// Menyatukan halaman: font dan foto ditanam sebagai data URI.
// Hasil: trading-tenang.html (untuk Artifact) dan site/index.html (untuk localhost).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const src = readFileSync('src/index.src.html', 'utf8');
const b64 = (path) => readFileSync(path).toString('base64');

const page = src
  .replace(/\{\{font:([\w-]+)\}\}/g, (_, name) => `data:font/woff2;base64,${b64(`fonts/${name}.woff2`)}`)
  .replace(/\{\{img:([\w-]+)\}\}/g, (_, name) => `data:image/jpeg;base64,${b64(`assets/web/${name}.jpg`)}`)
  .replace(/\{\{svgdata:([\w-]+)\}\}/g, (_, name) => `data:image/svg+xml;base64,${b64(`logo/final/${name}.svg`)}`)
  .replace(/\{\{pngdata:([\w-]+)\}\}/g, (_, name) => `data:image/png;base64,${b64(`logo/final/png/${name}.png`)}`);

writeFileSync('trading-tenang.html', page);

mkdirSync('site', { recursive: true });
writeFileSync('site/index.html',
  '<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>\n' +
  page + '\n</html>\n');

for (const f of ['favicon.ico']) writeFileSync(`site/${f}`, readFileSync(`logo/final/${f}`));
console.log(`built ${(page.length / 1024).toFixed(0)} KB`);
