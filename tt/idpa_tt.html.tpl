<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IDPA · TT Handicap</title>
<style>
:root{--bg:#12131a;--surface:#1c1e2a;--card:#252840;--border:#2a2d42;--accent:#e94560;--blue:#4c9fff;--text:#eaeaea;--muted:#7a7a9a;--green:#4caf50;--yellow:#ffa726;--red:#ef5350;--gold:#ffd700;--silver:#c0c0c0;--bronze:#cd7f32}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;padding:2rem 1rem}
.container{max-width:1060px;margin:0 auto}
h1{font-size:1.6rem;color:var(--accent);margin-bottom:.2rem}
.sub{color:var(--muted);font-size:.82rem;margin-bottom:1.5rem;line-height:1.5}
.row{display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:1.25rem}
.card{flex:1 1 240px;background:var(--surface);border:2px dashed var(--border);border-radius:10px;padding:1rem;cursor:pointer;transition:border-color .18s}
.card:hover{border-color:var(--blue)}.card.ok{border-style:solid;border-color:var(--green)}
.card input[type=file]{display:none}
.lbl{font-size:.69rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-bottom:.4rem}
.val{font-size:.85rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hint{font-size:.68rem;color:var(--muted);margin-top:.3rem;font-style:italic}
.panel{background:var(--surface);border-radius:10px;padding:.9rem 1rem;margin-bottom:1.25rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.panel label{font-size:.9rem}
.panel input[type=number]{width:90px;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:1rem;font-weight:600;padding:.3rem .5rem;text-align:center}
.panel input.req{border-color:var(--accent)}
.btn{padding:.55rem 1.4rem;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:.95rem;font-weight:600;cursor:pointer}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn2{padding:.35rem .85rem;border:1px solid var(--border);border-radius:7px;background:transparent;color:var(--text);font-size:.82rem;cursor:pointer}
.msg{font-size:.82rem;margin-bottom:1rem}.err{color:var(--red)}.warn{color:var(--yellow)}.okm{color:var(--green)}
.stats{display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:1rem}
.stat{background:var(--surface);border-radius:8px;padding:.6rem .9rem;min-width:150px}
.stat b{display:block;font-size:1.15rem}.stat span{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.85rem}
th{background:var(--card);padding:.5rem .6rem;text-align:left;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);white-space:nowrap;cursor:pointer;user-select:none}
th.num,td.num{text-align:right}
td{padding:.45rem .6rem;border-bottom:1px solid var(--border);background:var(--surface);white-space:nowrap}
tr:hover td{background:var(--card)}
.rk{font-weight:700}.r1{color:var(--gold)}.r2{color:var(--silver)}.r3{color:var(--bronze)}
.better{color:var(--green);font-weight:700}.worse{color:var(--red);font-weight:700}
.dim{color:var(--muted);font-size:.78rem}
.sect{font-size:.75rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:1.5rem 0 .5rem}
.foot{font-size:.72rem;color:var(--muted);margin-top:1.5rem;line-height:1.6}
@media (max-width:700px){
  body{padding:1rem 12px}
  h1{font-size:1.3rem}
  .opt{display:none}
  td,th{padding:.4rem .35rem;font-size:.8rem}
  .stat{min-width:0;flex:1 1 45%}
  .panel{gap:.6rem}
  .nm{white-space:normal;min-width:110px}
}
</style>
</head>
<body>
<div class="container">
<h1>🎯 IDPA · TT Handicap</h1>
<p class="sub">Gare tier 0: ogni tiratore confrontato con il proprio TT (secondi per colpo) nella stessa divisione.<br>
TT gara = punteggio finale (PD e penalità incluse) / colpi minimi. Rapporto = TT gara / TT handicap: sotto 1 = meglio del suo handicap.</p>

<div class="row">
  <div class="card" id="cGara" onclick="document.getElementById('fGara').click()">
    <div class="lbl">Risultati gara (CSV PractiScore)</div>
    <div class="val" id="nGara">Seleziona il CSV…</div>
    <div class="hint">export standard IDPA</div>
    <input type="file" id="fGara" accept=".csv">
  </div>
  <div class="card ok" id="cTT" style="cursor:default">
    <div class="lbl">Tabella TT handicap</div>
    <div class="val" id="nTT">caricamento da Google Drive…</div>
    <div class="hint" id="hTT">Google Sheet "TT_handicap_pubblico"</div>
  </div>
</div>

<div class="panel">
  <label for="colpi">Colpi minimi della gara <b style="color:var(--accent)">*</b></label>
  <input type="number" id="colpi" class="req" min="1" step="1" placeholder="es. 120">
  <button class="btn" id="calc" disabled onclick="calcola()">Calcola</button>
  <span class="dim" id="why">Carica il CSV e inserisci i colpi minimi.</span>
</div>

<div id="msgs"></div>
<div id="out" style="display:none">
  <div class="stats" id="stats"></div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem">
    <div class="sect" style="margin:0">Classifica per miglioramento rispetto al TT handicap</div>
    <button class="btn2" onclick="esporta()">⬇ Esporta CSV</button>
  </div>
  <div class="wrap"><table id="tab"></table></div>
  <div id="senza"></div>
  <p class="foot">
  <b>Rapporto</b> = TT gara / TT handicap. 0,90 = il 10% più veloce del proprio handicap. L'ordine per rapporto non dipende dalla difficoltà della gara.<br>
  <b>Indice gara</b> = mediana dei rapporti: stima quanto questa gara è stata più lenta (>1) o più veloce (&lt;1) di una gara media.<br>
  <b>Al netto della gara</b> = rapporto / indice gara: miglioramento rispetto agli altri tiratori oggi.<br>
  TT handicap: media dei TT delle gare 2025-2026, compensati per la difficoltà di ogni gara; solo tiratori con almeno 2 gare nella divisione. Il tiratore è riconosciuto per nome e cognome (anche invertiti) e divisione. Uso esclusivo per gare tier 0.
  </p>
</div>
</div>

<script>
const SHEET_URL = 'https://docs.google.com/spreadsheets/d/__SHEET_ID__/export?format=csv';
const TT_DEFAULT = __TT_JSON__;   // copia interna, usata solo se Drive non risponde
const TT_DEFAULT_DATA = '__TT_DATA__';
let TT = null, ttNome = '', gara = null, garaNome = '', ultimo = null;

function norm(s){
  return (s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'').toLowerCase()
    .replace(/[^a-z ]/g,' ').split(/\s+/).filter(Boolean).sort().join(' ');
}
function normId(s){ const m=(s||'').toUpperCase().replace(/\s/g,'').match(/^IT\d+/); return m&&!/^IT0*1?$/.test(m[0])?m[0]:null; }
function fmt(x,d=3){ return (x==null||isNaN(x))?'—':x.toFixed(d).replace('.',','); }
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

function parseCSV(text){
  text=text.replace(/^﻿/,'');
  const first=text.split(/\r?\n/)[0];
  const sep=(first.match(/;/g)||[]).length>(first.match(/,/g)||[]).length?';':',';
  const rows=[];let row=[],f='',q=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(c==='"'){ if(q&&text[i+1]==='"'){f+='"';i++;} else q=!q; }
    else if(c===sep&&!q){row.push(f);f='';}
    else if((c==='\n'||c==='\r')&&!q){ if(c==='\r'&&text[i+1]==='\n')i++; row.push(f);f=''; if(row.some(x=>x!==''))rows.push(row); row=[]; }
    else f+=c;
  }
  row.push(f); if(row.some(x=>x!==''))rows.push(row);
  const h=(rows[0]||[]).map(x=>x.trim());
  return rows.slice(1).map(r=>{const o={};h.forEach((k,i)=>o[k]=(r[i]||'').trim());return o;});
}
const num=s=>parseFloat(String(s).replace(',','.'));

// righe: [tiratore, divisione, classe, n_gare, tt_ms, dev_std_ms]
function caricaTT(rows){
  TT={byName:{}}; let n=0;
  rows.forEach(r=>{
    const [tir,div,cls,ng,ttms,sdms]=r;
    if(!tir||!div||!(ttms>0))return;
    TT.byName[norm(tir)+'|'+div.toUpperCase()]={tir,div,cls,ng,tt:ttms/1000,sd:sdms/1000};
    n++;
  });
  return n;
}
function fonte(testo,colore,hint){
  document.getElementById('nTT').textContent=testo;
  document.getElementById('cTT').style.borderColor=colore;
  if(hint) document.getElementById('hTT').textContent=hint;
}
async function caricaDaDrive(){
  try{
    const r=await fetch(SHEET_URL,{credentials:'omit',cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    const rows=parseCSV(await r.text());
    const agg=rows.length?rows[0]['aggiornato']:'';
    const n=caricaTT(rows.map(x=>[x['tiratore'],x['divisione'],x['classe_ultima'],parseInt(x['n_gare']),parseInt(x['tt_ms']),parseInt(x['dev_std_ms'])]));
    if(!n) throw new Error('foglio vuoto o colonne errate');
    fonte(`Google Drive · ${n} tiratori/divisione`,'var(--green)',`aggiornato ${agg.replace(/(\d{4})(\d\d)(\d\d)/,'$3/$2/$1')}`);
  }catch(e){
    const n=caricaTT(TT_DEFAULT);
    fonte(`Copia interna · ${n} tiratori/divisione`,'var(--yellow)',`Drive non raggiungibile (${e.message}); dati del ${TT_DEFAULT_DATA}`);
  }
  if(ultimo) calcola();
}
caricaDaDrive();
document.getElementById('fGara').addEventListener('change',function(){
  const f=this.files[0]; if(!f)return;
  const rd=new FileReader(); rd.onload=e=>{
    const rows=parseCSV(e.target.result);
    if(!rows.length||!('Total Score' in rows[0])||!('Division' in rows[0])){ msg('err','Il file non sembra un export risultati PractiScore (mancano Total Score / Division).'); gara=null; aggiorna(); return; }
    gara=rows; garaNome=f.name;
    document.getElementById('nGara').textContent=`${f.name} · ${rows.length} righe`;
    document.getElementById('cGara').className='card ok';
    msg('',''); document.getElementById('out').style.display='none'; aggiorna();
  }; rd.readAsText(f,'UTF-8'); this.value='';
});
document.getElementById('colpi').addEventListener('input',aggiorna);
function aggiorna(){
  const c=parseInt(document.getElementById('colpi').value);
  const ok=gara&&c>0;
  document.getElementById('calc').disabled=!ok;
  document.getElementById('colpi').className=c>0?'':'req';
  document.getElementById('why').textContent=ok?'':(!gara?'Carica il CSV della gara.':'Inserisci i colpi minimi (obbligatorio).');
}
function msg(cls,t){ document.getElementById('msgs').innerHTML=t?`<div class="msg ${cls}">${t}</div>`:''; }

function calcola(){
  const colpi=parseInt(document.getElementById('colpi').value);
  if(!gara||!(colpi>0))return;
  const con=[],senza=[],esclusi=[];
  gara.forEach(r=>{
    const nome=`${r['Last Name']||''} ${r['First Name']||''}`.trim();
    const div=(r['Division']||'').toUpperCase().trim();
    const sc=num(r['Total Score']);
    if(r['Completed']!=='1'||r['DNF']==='1'||!(sc>0)){ esclusi.push(nome); return; }
    const ttg=sc/colpi;
    const h=TT&&TT.byName[norm(nome)+'|'+div];
    const base={nome,div,cls:(r['Class']||'').toUpperCase(),score:sc,ttg};
    if(h) con.push({...base,h,rap:ttg/h.tt});
    else senza.push(base);
  });
  if(!con.length){ msg('warn','Nessun tiratore della gara ha un TT handicap nella sua divisione.'); document.getElementById('out').style.display='none'; return; }
  const rs=con.map(x=>x.rap).sort((a,b)=>a-b);
  const mid=rs.length>>1, idx=rs.length%2?rs[mid]:(rs[mid-1]+rs[mid])/2;
  con.forEach(x=>x.netto=x.rap/idx);
  con.sort((a,b)=>a.rap-b.rap);
  ultimo={con,senza,esclusi,idx,colpi};
  render();
}
function render(){
  const {con,senza,esclusi,idx,colpi}=ultimo;
  const migl=con.filter(x=>x.rap<1).length;
  document.getElementById('stats').innerHTML=
    `<div class="stat"><span>Colpi minimi</span><b>${colpi}</b></div>`+
    `<div class="stat"><span>Con handicap</span><b>${con.length}</b></div>`+
    `<div class="stat"><span>Meglio del proprio TT</span><b>${migl} / ${con.length}</b></div>`+
    `<div class="stat"><span>Indice gara (mediana rapporti)</span><b>${fmt(idx,2)}</b></div>`;
  let h=`<thead><tr><th>Pos</th><th>Tiratore</th><th>Div/Cls</th><th class="num opt">Punteggio</th><th class="num">TT hcp</th><th class="num opt">Gare</th><th class="num">TT gara</th><th class="num">Rapp.</th><th class="num opt">Variaz.</th><th class="num opt">Netto gara</th></tr></thead><tbody>`;
  con.forEach((x,i)=>{
    const p=i+1, rc=p===1?'r1':p===2?'r2':p===3?'r3':'';
    const v=(x.rap-1)*100, cl=x.rap<1?'better':'worse';
    h+=`<tr><td class="rk ${rc}">${p}</td><td class="nm">${esc(x.nome)}</td><td class="dim">${x.div}/${x.cls}</td>
      <td class="num opt">${fmt(x.score,2)}</td><td class="num">${fmt(x.h.tt)}<span class="dim opt"> ±${fmt(x.h.sd,2)}</span></td>
      <td class="num dim opt">${x.h.ng}</td><td class="num">${fmt(x.ttg)}</td>
      <td class="num ${cl}">${fmt(x.rap)}</td><td class="num ${cl} opt">${v>0?'+':''}${fmt(v,1)}%</td>
      <td class="num opt">${fmt(x.netto)}</td></tr>`;
  });
  document.getElementById('tab').innerHTML=h+'</tbody>';
  let s='';
  if(senza.length){
    s+=`<div class="sect">Senza TT handicap in questa divisione (${senza.length})</div><div class="wrap"><table><thead><tr><th>Tiratore</th><th>Div/Cls</th><th class="num">Punteggio</th><th class="num">TT gara</th></tr></thead><tbody>`;
    senza.sort((a,b)=>a.ttg-b.ttg).forEach(x=>s+=`<tr><td>${esc(x.nome)}</td><td class="dim">${x.div}/${x.cls}</td><td class="num">${fmt(x.score,2)}</td><td class="num">${fmt(x.ttg)}</td></tr>`);
    s+='</tbody></table></div>';
  }
  if(esclusi.length) s+=`<p class="foot">Esclusi (DNF, non completato o senza punteggio): ${esclusi.map(esc).join(', ')}</p>`;
  document.getElementById('senza').innerHTML=s;
  document.getElementById('out').style.display='';
}
function esporta(){
  if(!ultimo)return;
  const n=x=>String(x).replace('.',',');
  let csv='﻿pos;tiratore;divisione;classe;punteggio;tt_handicap;dev_std;gare_handicap;tt_gara;rapporto;variazione_pct;al_netto_gara\n';
  ultimo.con.forEach((x,i)=>csv+=[i+1,`"${x.nome}"`,x.div,x.cls,n(x.score.toFixed(2)),n(x.h.tt.toFixed(3)),n(x.h.sd.toFixed(3)),x.h.ng,n(x.ttg.toFixed(3)),n(x.rap.toFixed(3)),n(((x.rap-1)*100).toFixed(1)),n(x.netto.toFixed(3))].join(';')+'\n');
  ultimo.senza.forEach(x=>csv+=['',`"${x.nome}"`,x.div,x.cls,n(x.score.toFixed(2)),'','','',n(x.ttg.toFixed(3)),'','',''].join(';')+'\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  a.download='classifica_tt_'+(garaNome.replace(/\.csv$/i,'')||'gara')+'.csv'; a.click();
}
</script>
</body>
</html>
