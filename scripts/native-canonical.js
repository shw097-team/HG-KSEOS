// Independent restricted canonical-profile implementation; no signing/authority.
'use strict';
const fs = require('fs');
function canonical(value) {
  function render(v) {
    if (v === null || typeof v === 'boolean') return JSON.stringify(v);
    if (typeof v === 'number') {
      if (!Number.isSafeInteger(v)) throw Error('INTEGER');
      return JSON.stringify(v);
    }
    if (typeof v === 'string') {
      if (!/^[\x20-\x7e]*$/.test(v)) throw Error('ASCII');
      return JSON.stringify(v);
    }
    if (Array.isArray(v)) return '['+v.map(render).join(',')+']';
    if (typeof v === 'object') return '{'+Object.keys(v).sort().map(k=>render(k)+':'+render(v[k])).join(',')+'}';
    throw Error('TYPE');
  }
  return Buffer.from('HGK-B1-ASCII-C14N/1\x00'+render(value),'ascii');
}
if (require.main === module) process.stdout.write(canonical(JSON.parse(fs.readFileSync(0,'utf8'))));
module.exports = { canonical };
