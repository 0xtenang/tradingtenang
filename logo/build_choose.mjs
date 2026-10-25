// Menyusun halaman pilihan arah logo dari logo/explore/*.svg.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('..', import.meta.url));
const src = readFileSync(root + 'logo/choose.src.html', 'utf8');
const out = src
  .replace(/\{\{font:([\w-]+)\}\}/g, (_, f) => `data:font/woff2;base64,${readFileSync(root + `fonts/${f}.woff2`).toString('base64')}`)
  .replace(/\{\{x:([\w-]+)\}\}/g, (_, f) => readFileSync(root + `logo/explore/${f}.svg`, 'utf8').trim()
    .replace(/ width="\d+" height="\d+"/, '')
    // id clipPath harus unik di satu halaman
    .replace(/(id="|url\(#)(\w+)/g, (_, pre, id) => `${pre}${id}_${f.replace(/-/g, '_')}`));
writeFileSync(root + 'logo-trading-tenang.html', out);
writeFileSync(root + 'site/logo.html', '<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + out + '\n</html>\n');
console.log('ok', (out.length / 1024).toFixed(0) + ' KB');
