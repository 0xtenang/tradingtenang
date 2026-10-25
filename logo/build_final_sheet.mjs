// Menyusun halaman logo final dari logo/final/*.svg.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('..', import.meta.url));
const src = readFileSync(root + 'logo/final.src.html', 'utf8');
const out = src
  .replace(/\{\{font:([\w-]+)\}\}/g, (_, f) => `data:font/woff2;base64,${readFileSync(root + `fonts/${f}.woff2`).toString('base64')}`)
  .replace(/\{\{f:([\w-]+)\}\}/g, (_, f) => readFileSync(root + `logo/final/${f}.svg`, 'utf8').trim().replace(/ width="\d+" height="\d+"/, ''));
const head = `<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,${readFileSync(root + 'logo/final/favicon.svg').toString('base64')}">\n`;
writeFileSync(root + 'logo-trading-tenang.html', head + out);
writeFileSync(root + 'site/logo.html', '<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + head + out + '\n</html>\n');
console.log('ok', (out.length / 1024).toFixed(0) + ' KB');
