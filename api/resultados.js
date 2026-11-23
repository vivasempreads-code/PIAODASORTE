// Feed de resultados da própria promoção. Nunca consulta nem republica ganhadores de terceiros.
const URL=process.env.UPSTASH_REDIS_REST_URL;
const TOKEN=process.env.UPSTASH_REDIS_REST_TOKEN;
const KEY='promocao:resultados:publicados';
async function redis(command,...args){const r=await fetch(URL,{method:'POST',headers:{Authorization:`Bearer ${TOKEN}`,'Content-Type':'application/json'},body:JSON.stringify([command,...args])});if(!r.ok)throw Error('Redis indisponível');const data=await r.json();if(data.error)throw Error('Redis indisponível');return data.result;}
export default async function handler(req,res){res.setHeader('Cache-Control','no-store');if(!URL||!TOKEN)return res.status(503).json({error:'Configure Upstash'});
try{if(req.method==='GET'){const data=await redis('GET',KEY);return res.status(200).json({resultados:data?JSON.parse(data):[],fonte:'Resultados publicados pelo organizador'});}
if(req.method==='PUT'){const {timingSafeEqual}=await import('node:crypto');const expected=process.env.ADMIN_PASSWORD||'';const supplied=String(req.headers.authorization||'').replace(/^Bearer\s+/i,'');const a=Buffer.from(expected),b=Buffer.from(supplied);if(!expected||a.length!==b.length||!timingSafeEqual(a,b))return res.status(401).json({error:'Não autorizado'});
const rows=req.body?.resultados;if(!Array.isArray(rows)||rows.length>100)return res.status(400).json({error:'Lista inválida'});
const valid=rows.map(x=>({nome:String(x.nome||'').slice(0,50),valor:Number(x.valor),estado:String(x.estado||'').slice(0,40),horario:String(x.horario||'').slice(0,35),confirmado:x.confirmado===true})).filter(x=>x.confirmado&&x.nome&&Number.isFinite(x.valor)&&x.valor>0&&x.estado&&x.horario);
await redis('SET',KEY,JSON.stringify(valid));return res.status(200).json({ok:true,publicados:valid.length});}
return res.status(405).json({error:'Método não permitido'});}catch(e){return res.status(500).json({error:'Não foi possível consultar resultados'});}}
