from pathlib import Path
p=Path('/mnt/data/piao_work/faunaeflora-main');f=p/'index.html';s=f.read_text();s=s.replace('<div id="piaoWheel" class="piao-wheel"></div>','<div id="piaoWheel" class="piao-wheel"><div class="piao-cubo" aria-hidden="true"><span>R$ 2 MIL</span><span>R$ 4 MIL</span><span>R$ 5 MIL</span><span>R$ 10 MIL</span></div></div>')
s=s.replace("piaoGrau+=1440+Math.floor(Math.random()*360);", "tocarSomPiao();piaoGrau+=1440+Math.floor(Math.random()*360);")
s=s.replace('setTimeout(()=>{atualizarPiao(j);','setTimeout(()=>{pararSomPiao();atualizarPiao(j);if(j.premio>0)celebrarPiao();')
s=s.replace("piaoOcupado=false}}\n", "pararSomPiao();piaoOcupado=false}}\n")
extra='''<style id="piao-animado">
.piao-wheel:after{display:none!important}.piao-cubo{position:absolute;inset:36%;z-index:1;border:5px solid #fff;border-radius:18px;background:linear-gradient(145deg,#ffd579,#e9a62d);box-shadow:inset -8px -8px 15px #ad751f77,0 8px 20px #0006;display:flex;align-items:center;justify-content:center;transform:perspective(240px) rotateY(16deg);animation:cuboFlutua 3s ease-in-out infinite}.piao-cubo span{position:absolute;font-size:clamp(9px,2.5vw,13px);font-weight:950;color:#092f79;backface-visibility:hidden;text-shadow:0 1px white}.piao-cubo span:nth-child(2){transform:rotateY(90deg) translateZ(24px)}.piao-cubo span:nth-child(3){transform:rotateY(180deg) translateZ(24px)}.piao-cubo span:nth-child(4){transform:rotateY(270deg) translateZ(24px)}.piao-cubo span:first-child{transform:translateZ(24px)}
@keyframes cuboFlutua{0%,100%{transform:perspective(240px) rotateY(10deg) rotateX(8deg)}50%{transform:perspective(240px) rotateY(165deg) rotateX(-12deg)}}
.piao-confete{position:fixed;top:-20px;width:10px;height:17px;z-index:100001;pointer-events:none;animation:confeteCai 3.4s linear forwards}@keyframes confeteCai{to{transform:translateY(110vh) rotate(900deg);opacity:0}}
@media(prefers-reduced-motion:reduce){.piao-cubo{animation:none}.piao-confete{animation-duration:.01s}}
</style><script>
let somPiaoCtx=null,somPiaoTimer=null;
function tocarSomPiao(){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;somPiaoCtx=somPiaoCtx||new AC();somPiaoCtx.resume();let n=0;somPiaoTimer=setInterval(()=>{let osc=somPiaoCtx.createOscillator(),gain=somPiaoCtx.createGain();osc.type='triangle';osc.frequency.value=620+(n++%5)*80;gain.gain.setValueAtTime(.045,somPiaoCtx.currentTime);gain.gain.exponentialRampToValueAtTime(.001,somPiaoCtx.currentTime+.08);osc.connect(gain);gain.connect(somPiaoCtx.destination);osc.start();osc.stop(somPiaoCtx.currentTime+.09)},115)}catch(e){}}
function pararSomPiao(){if(somPiaoTimer){clearInterval(somPiaoTimer);somPiaoTimer=null}}
function celebrarPiao(){for(let i=0;i<65;i++){let c=document.createElement('span');c.className='piao-confete';c.style.left=Math.random()*100+'vw';c.style.background=['#ffd24f','#21d779','#fff','#467eff'][i%4];c.style.animationDelay=Math.random()*.8+'s';document.body.append(c);setTimeout(()=>c.remove(),4400)}}
</script>'''
s=s.replace('</body>',extra+'</body>');f.write_text(s)
# server payment must match count at least 8
q=p/'api/allowpay.js';t=q.read_text();t=t.replace('quantidade <= 0','quantidade < 8 || Math.abs(amount - quantidade * 0.49) > 0.011');q.write_text(t)
