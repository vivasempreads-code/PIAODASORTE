import { timingSafeEqual } from 'node:crypto';
const url=process.env.UPSTASH_REDIS_REST_URL;
const token=process.env.UPSTASH_REDIS_REST_TOKEN;
function authorized(req){
 const expected=process.env.ADMIN_PASSWORD;
 const supplied=(req.headers.authorization||'').replace(/^Bearer\s+/i,'');
 if(!expected||!supplied)return false;
 const a=Buffer.from(supplied),b=Buffer.from(expected);
 return a.length===b.length&&timingSafeEqual(a,b);
}
async function redis(...args){
 const r=await fetch(url,{method:'POST',headers:{Authorization:`Bearer ${token}`,'Content-Type':'application/json'},body:JSON.stringify(args)});
 if(!r.ok)throw new Error('Falha no armazenamento');
 const j=await r.json();if(j.error)throw new Error('Falha no armazenamento');return j.result;
}
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');
 if(!url||!token)return res.status(503).json({error:'Configure UPSTASH_REDIS_REST_URL e UPSTASH_REDIS_REST_TOKEN na Vercel'});
 try{
  if(req.method==='PUT'){
   if(!authorized(req))return res.status(401).json({error:'Acesso não autorizado'});
   const rows=req.body?.fichas;
   if(!Array.isArray(rows)||rows.length>10000)return res.status(400).json({error:'JSON inválido ou grande demais'});
   let added=0,skipped=0;
   for(const row of rows){
    if(!row||typeof row!=='object'||!/^[-\w]{5,128}$/.test(String(row.id||''))||!/^[0-9]{11}$/.test(String(row.cpf||''))){skipped++;continue}
    const exists=await redis('GET',`ficha:${row.id}`);if(exists){skipped++;continue}
    const safe={id:String(row.id),cpf:String(row.cpf),nome:String(row.nome||'').slice(0,120),data_nascimento:String(row.data_nascimento||'').slice(0,30),telefone:String(row.telefone||'').slice(0,20),quantidade:Number(row.quantidade)||0,valor:Number(row.valor)||0,status:String(row.status||'importado').slice(0,40),criado_em:String(row.criado_em||new Date().toISOString()).slice(0,40),...(row.piao&&typeof row.piao==='object'?{piao:{giros:Number(row.piao.giros)||0,premio:Number(row.piao.premio)||0,status:String(row.piao.status||'').slice(0,60)}}:{})};
    await redis('SET',`ficha:${safe.id}`,JSON.stringify(safe));await redis('ZADD','fichas:indices',Date.parse(safe.criado_em)||Date.now(),safe.id);added++;
   }return res.status(200).json({ok:true,importadas:added,ignoradas:skipped});
  }
  if(req.method==='POST'){
   const x=req.body||{};
   const cpf=String(x.cpf||'').replace(/\D/g,''),tel=String(x.telefone||'').replace(/\D/g,'');
   const qtd=Number(x.quantidade),valor=Number(x.valor),id=String(x.transaction_id||'');
   if(cpf.length!==11||tel.length<10||!Number.isInteger(qtd)||qtd<8||qtd>500||Math.abs(valor-qtd*.49)>.011||!/^[-\w]{5,128}$/.test(id))return res.status(400).json({error:'Dados inválidos'});
   const item={id,cpf,nome:String(x.nome||'').slice(0,120),data_nascimento:String(x.data_nascimento||'').slice(0,30),telefone:tel,quantidade:qtd,valor,status:'pix_gerado',criado_em:new Date().toISOString()};
   const old=await redis('GET',`ficha:${id}`);if(old)return res.status(200).json({ok:true,duplicada:true});
   await redis('SET',`ficha:${id}`,JSON.stringify(item));
   await redis('ZADD','fichas:indices',Date.now(),id);
   return res.status(201).json({ok:true});
  }
  if(!authorized(req))return res.status(401).json({error:'Acesso não autorizado'});
  if(req.method==='GET'){
   const ids=await redis('ZREVRANGE','fichas:indices',0,-1)||[];
   const rows=await Promise.all(ids.map(async id=>{const data=await redis('GET',`ficha:${id}`);try{return JSON.parse(data)}catch{return null}}));
   return res.status(200).json({fichas:rows.filter(Boolean)});
  }
  if(req.method==='DELETE'){
   const id=String(req.query.id||'');if(!/^[-\w]{5,128}$/.test(id))return res.status(400).json({error:'ID inválido'});
   await redis('DEL',`ficha:${id}`);await redis('ZREM','fichas:indices',id);
   return res.status(200).json({ok:true});
  }
  return res.status(405).json({error:'Método não permitido'});
 }catch(e){return res.status(500).json({error:'Erro ao processar ficha'});}
}
