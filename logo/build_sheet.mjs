// Menyusun lembar logo: SVG ditanam langsung, font sebagai data URI.
// Hasil: logo-trading-tenang.html (untuk Artifact) dan site/logo.html (untuk localhost).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('..', import.meta.url));
const src = readFileSync(root + 'logo/sheet.src.html', 'utf8');
const out = src
  .replace(/\{\{font:([\w-]+)\}\}/g, (_, n) => `data:font/woff2;base64,${readFileSync(root + `fonts/${n}.woff2`).toString('base64')}`)
  .replace(/\{\{svg:([\w-]+)\}\}/g, (_, n) => readFileSync(root + `logo/svg/${n}.svg`, 'utf8').trim().replace(/ width="\d+" height="\d+"/, ''));
writeFileSync(root + 'logo-trading-tenang.html', out);
mkdirSync(root + 'site', { recursive: true });
writeFileSync(root + 'site/logo.html', '<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + out + '\n</html>\n');
console.log('ok', (out.length / 1024).toFixed(0) + ' KB');
