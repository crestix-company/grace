// Cloudflare Pages advanced mode. Only the contact endpoint needs a Worker.
const endpoint = '/api/contact';
const maxBytes = 14000;
const keepFor = 90 * 24 * 60 * 60;
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const subjects = new Set(['施術・メニュー','ご来店について','採用・見学','その他']);
function json(status, body) {
  return Response.json(body, {status, headers:{'Cache-Control':'no-store', 'X-Content-Type-Options':'nosniff'}});
}
async function readInput(request) {
  const reader = request.body?.getReader();
  if (!reader) throw new Error('empty');
  const bytes = new Uint8Array(maxBytes);
  let used = 0;
  try {
    for (;;) {
      const {done,value} = await reader.read();
      if (done) break;
      if (used + value.length > maxBytes) {
        await reader.cancel();
        throw new RangeError('size');
      }
      bytes.set(value, used);
      used += value.length;
    }
    return JSON.parse(new TextDecoder('utf-8', {fatal:true}).decode(bytes.subarray(0,used)));
  } finally { reader.releaseLock(); }
}
function fields(data) {
  if (!data || typeof data !== 'object' || data.consent !== true || typeof data.ticket !== 'string' || !uuid.test(data.ticket)) return null;
  const text = {};
  for (const [key,max] of Object.entries({name:80,email:254,phone:30,subject:30,message:2000})) {
    if (typeof data[key] !== 'string') return null;
    const value = data[key].trim();
    if ((!value && key !== 'phone') || value.length > max) return null;
    text[key] = value;
  }
  if (!subjects.has(text.subject) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text.email) || (text.phone && !/^[0-9０-９\s()+＋ー－-]{3,30}$/.test(text.phone))) return null;
  return text;
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== endpoint) return env.ASSETS.fetch(request);
    const available = typeof env.CONTACT_INBOX?.put === 'function';
    if (request.method === 'GET') return json(200,{available});
    if (request.method !== 'POST') return new Response(null,{status:405, headers:{Allow:'GET, POST','Cache-Control':'no-store'}});
    if (!available) return json(503,{error:'closed'});
    if (request.headers.get('Origin') !== url.origin) return json(403,{error:'origin'});
    if (request.headers.get('Content-Type')?.split(';')[0].trim().toLowerCase() !== 'application/json') return json(415,{error:'format'});
    let data;
    try { data = await readInput(request); }
    catch (error) { return json(error instanceof RangeError ? 413 : 400,{error:'input'}); }
    const values = fields(data);
    if (!values || data.website) return json(400,{error:'input'});
    // The same retry writes to the same key. Unrelated submissions cannot overwrite it.
    const raw = await crypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify([data.ticket,values])));
    const key = Array.from(new Uint8Array(raw), b => b.toString(16).padStart(2,'0')).join('');
    const receivedAt = new Date().toISOString();
    try {
      await env.CONTACT_INBOX.put('inquiry:'+key, JSON.stringify({receivedAt,...values}),{expirationTtl:keepFor});
    } catch { return json(503,{error:'storage'}); }
    return json(201,{received:true,receipt:key.slice(0,12)});
  }
};
