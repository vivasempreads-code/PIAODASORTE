from pathlib import Path
p=Path('/mnt/data/piao_work/faunaeflora-main'); f=p/'index.html'; s=f.read_text()
s=s.replace('const MINIMO_TITULOS = 15;', 'const MINIMO_TITULOS = 8;').replace('quantidade: 6,\n        valor: 2.94','quantidade: 8,\n        valor: 3.92').replace('value="15" min="15"','value="8" min="8"').replace('O pedido mínimo é de 15 títulos (R$ 7,35).','O pedido mínimo é de 8 títulos (R$ 3,92).')
for a,b in [('selecionarPacote(15, 7.35','selecionarPacote(8, 3.92'),('selecionarPacote(25, 12.25','selecionarPacote(15, 7.35'),('selecionarPacote(50, 24.50','selecionarPacote(25, 12.25'),('selecionarPacote(75, 36.75','selecionarPacote(50, 24.50'),('selecionarPacote(100, 49.00','selecionarPacote(75, 36.75'),('selecionarPacote(150, 73.50','selecionarPacote(100, 49.00')]:s=s.replace(a,b)
for a,b in [('+15</div><h1>R$7,35','+8</div><h1>R$3,92'),('+25</div><h1>R$12,25','+15</div><h1>R$7,35'),('+50</div><h1>R$24,50','+25</div><h1>R$12,25'),('+75</div><h1>R$36,75','+50</div><h1>R$24,50'),('+100</div><h1>R$49,00','+75</div><h1>R$36,75'),('+150</div><h1>R$73,50','+100</div><h1>R$49,00')]:s=s.replace(a,b)
# replace default display-only quantities
s=s.replace('id="cartQtd">15','id="cartQtd">8').replace('id="cartQtdOferta">15','id="cartQtdOferta">8').replace('id="cartQtdResumo">15','id="cartQtdResumo">8')
# details sheet: deliberately avoid importing unverifiable results, official approval or trademarked branding
sheet='''
<style id="nova-identidade">
:root{--azul-premio:#1047ef;--verde-premio:#24ca6b}
.white-header{background:#1047ef!important;color:white!important}
.cotas,.contador-cotas{border-radius:16px!important}
.adc-carrinho,#etapaCarrinho .btn-principal{background:linear-gradient(90deg,#16c45f,#43da85)!important;color:#fff!important;border:0!important;border-radius:12px!important}
#etapaCarrinho .cart-head,#etapa2 .pix-payment-heading{background:#1047ef!important}
#etapaCarrinho .cart-total{background:#f4f6fb!important;color:#122039!important}
#etapaCarrinho .cart-line{border-color:#edf0f6!important}
#etapaCarrinho .cart-offer{background:#f7f9ff!important;border-color:#dce5ff!important}
#etapaCarrinho .cart-offer-top{background:#1047ef!important}
.detalhes-card{max-width:920px;margin:16px auto;padding:20px;background:#f5f7fc;border-radius:18px;color:#172033;font-family:Inter,system-ui,sans-serif}
.detalhes-card h2{font-size:24px;font-weight:850}.detalhes-card p{font-size:14px;color:#4b5563}
.detalhes-btn{border:0;border-radius:10px;background:#1047ef;color:#fff;padding:13px 24px;font-weight:800;cursor:pointer;width:100%}
#detalhesOverlay{display:none;position:fixed;inset:0;background:#07132fbb;z-index:999999;align-items:center;justify-content:center;padding:10px}
#detalhesOverlay.open{display:flex}
.detalhes-dialog{position:relative;width:min(100%,620px);max-height:94dvh;overflow:auto;background:#fff;border-radius:20px;padding:24px 20px 30px;color:#16223a;box-shadow:0 20px 80px #0005;overscroll-behavior:contain}
.detalhes-dialog h2{font-size:25px;font-weight:900;margin:12px 0}.detalhes-dialog h3{font-size:18px;font-weight:800;margin:22px 0 9px}
.detalhes-dialog p,.detalhes-dialog li{font-size:15px;line-height:1.6}.detalhes-dialog .close-detail{position:sticky;top:0;float:right;border:0;background:#eaf0ff;color:#1047ef;padding:10px 14px;border-radius:12px;font-weight:800;z-index:2}
.detalhes-dialog .detail-step{padding:12px;background:#f3f6fd;border-radius:12px;margin:8px 0}
@media(max-width:600px){.detalhes-card{margin:12px;padding:16px}.detalhes-dialog{max-height:100dvh;height:100dvh;border-radius:0;padding:20px 16px}#detalhesOverlay{padding:0}}
</style>
<section class="detalhes-card" aria-label="Informações da participação">
<h2>Últimos resultados e informações</h2><p>Confira como funciona a participação, os valores e as condições do Pião da Sorte. Resultados e prêmios somente são confirmados após validação.</p>
<button class="detalhes-btn" type="button" onclick="abrirDetalhes()">VER DETALHES ›</button>
</section>
<div id="detalhesOverlay" role="dialog" aria-modal="true" aria-labelledby="detalhesTitulo" aria-hidden="true" onclick="if(event.target===this)fecharDetalhes()">
<div class="detalhes-dialog" tabindex="-1"><button class="close-detail" type="button" onclick="fecharDetalhes()" aria-label="Fechar detalhes">✕ Fechar</button>
<h2 id="detalhesTitulo">Detalhes da participação</h2>
<p>Informações da experiência de títulos e do Pião da Sorte deste site. Os exemplos visuais não representam garantia de premiação.</p>
<h3>Valor dos títulos</h3><p>Cada título custa R$ 0,49. Compra mínima de 8 títulos, totalizando R$ 3,92. A quantidade selecionada e o total são exibidos antes de gerar o PIX.</p>
<h3>Como participar</h3><div class="detail-step">1. Escolha a quantidade de títulos.</div><div class="detail-step">2. Informe os dados solicitados para identificação.</div><div class="detail-step">3. Confira o resumo e pague por PIX.</div><div class="detail-step">4. Aguarde a confirmação real do pagamento.</div><div class="detail-step">5. Se elegível, acesse o Pião da Sorte e consulte o resultado registrado.</div>
<h3>Pião da Sorte</h3><p>Os giros dependem da confirmação do pagamento e da disponibilidade do sistema. A animação não define o resultado: a validação ocorre no servidor. Nenhum prêmio é garantido.</p>
<h3>Premiações e resultados</h3><p>Consulte somente o regulamento oficial e os resultados verificáveis da campanha efetivamente contratada. Esta versão não publica nomes de ganhadores, números de autorização nem valores de prêmios que não tenham sido comprovados.</p>
<h3>Condições gerais</h3><p>O pagamento não garante prêmio instantâneo. Confira regras, elegibilidade, datas, limites e procedimentos de validação antes de participar.</p>
<button class="detalhes-btn" type="button" onclick="fecharDetalhes()">VOLTAR À PÁGINA INICIAL</button>
</div></div>
<script>
let detalhesAberto=false;
function abrirDetalhes(){let o=document.getElementById('detalhesOverlay');o.classList.add('open');o.setAttribute('aria-hidden','false');detalhesAberto=true;history.pushState({detalhes:true},'','#detalhes');o.querySelector('.close-detail').focus()}
function fecharDetalhes(fromPop){let o=document.getElementById('detalhesOverlay');o.classList.remove('open');o.setAttribute('aria-hidden','true');detalhesAberto=false;if(!fromPop&&history.state?.detalhes)history.back()}
window.addEventListener('popstate',()=>{if(detalhesAberto)fecharDetalhes(true)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&detalhesAberto)fecharDetalhes()});
</script>
'''
s=s.replace('</body>',sheet+'</body>')
# prevent misleading unconditional award language in wheel UI
s=s.replace('<p>Prêmio instantâneo de R$ 10.000</p>','<p>Gire para consultar seu resultado. Prêmios sujeitos às regras.</p>')
# remove false promotional claims in wheel if server response doesn't establish a prize
f.write_text(s)
# server-side min
q=p/'api/fichas.js';t=q.read_text().replace('qtd<15','qtd<8');q.write_text(t)
