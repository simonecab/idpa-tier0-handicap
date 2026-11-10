# Uso: python correggi_identita.py <cartella gare originali> <cartella output> <log.csv>
# Eseguito il 10/11/2026: originali in Drive TIER 0/archivio/gare_originali_2026-11-10, log correzioni_identita_2026-11-10.csv
"""Unifica identita' dei tiratori nei CSV PractiScore (nome/cognome e IDPA ID).
Regole:
- ID valido: IT + cifre, ripulito da spazi e testo dopo (es. 'IT1031654 scad.07/2026' -> IT1031654).
  Segnaposto non validi: IT0000, IT0001, IT00001, IT001 e ogni valore senza prefisso IT.
- Chiave nome: parole normalizzate (senza accenti/maiuscole/punteggiatura) ordinate: gestisce nome/cognome invertiti.
- Due chiavi nome diverse sono la stessa persona se condividono l'ID che per entrambe e' il piu' frequente
  (cosi' un ID usato una volta per errore non fonde due persone diverse). Piu' fusioni manuali (MANUALI).
- Forma canonica: nome = coppia (Last, First) piu' frequente della chiave piu' frequente; ID = ID valido piu' frequente
  (a parita', il piu' recente).
- Si riscrive una riga solo se il nome normalizzato o l'ID (in maiuscolo) differisce dalla forma canonica,
  oppure se l'ID e' non valido e la persona ne ha uno valido. Tutti gli altri campi restano identici."""
import csv, io, glob, os, re, sys, unicodedata, collections
SRC, DST, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
MANUALI = [('cattiveria massimo','cattivera massimo')]
SEPARATI = {'cappella max'}
FORZA = {'bufalini milco':('Bufalini','Milco'),'cacio osvaldo':('Cacio','Osvaldo'),'napolitano niko':('Napolitano','Niko')}  # orientamento deciso a mano   # stesso ID di Cappella Nicola, identita' non certa: non si fonde e non si tocca
PLACEHOLDER = re.compile(r'^IT0*1?$')
def norm(s): return re.sub(r'[^a-z ]',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).split()
def nkey(l,f): return ' '.join(sorted(norm(l)+norm(f)))
def clean_id(s):
    m=re.match(r'^\s*IT\s*(\d+)',s,re.I)
    if not m: return None
    v='IT'+m.group(1)
    if PLACEHOLDER.match(v): return None
    d=m.group(1)
    if len(d)==8 and 1<=int(d[:2])<=31 and 1<=int(d[2:4])<=12 and d[4:6] in ('19','20'): return None  # data di nascita
    return v
files={}
for f in sorted(glob.glob(SRC+'/*.csv')):
    raw=open(f,'rb').read(); txt=raw.decode('utf-8-sig')
    files[os.path.basename(f)]=(raw.startswith(b'\xef\xbb\xbf'),'\r\n' if '\r\n' in txt else '\n',txt.endswith(('\n','\r\n')),list(csv.reader(io.StringIO(txt,newline=''))))
recs=[]
for fn,(bom,nl,endnl,rows) in files.items():
    h=rows[0]; iL,iF,iI=h.index('Last Name'),h.index('First Name'),h.index('IDPA ID')
    for j,r in enumerate(rows[1:],1):
        if len(r)<=iI: continue
        recs.append(dict(fn=fn,j=j,last=r[iL],first=r[iF],id=r[iI],cid=clean_id(r[iI]),nk=nkey(r[iL],r[iF])))
FC=collections.Counter(t for x in recs for t in norm(x['first'])); LC=collections.Counter(t for x in recs for t in norm(x['last']))
bynk=collections.defaultdict(list)
for x in recs: bynk[x['nk']].append(x)
mode_id={}
for nk,v in bynk.items():
    c=collections.Counter(x['cid'] for x in v if x['cid'])
    if c:
        top=max(c.values()); cand=[i for i in c if c[i]==top]
        mode_id[nk]=max(cand,key=lambda i:(len(i),max(x['fn'] for x in v if x['cid']==i)))
par={}
def find(a):
    while par.setdefault(a,a)!=a: par[a]=par[par[a]]; a=par[a]
    return a
def union(a,b): par[find(a)]=find(b)
for nk in bynk: find('N:'+nk)
for nk,i in mode_id.items():
    if nk not in SEPARATI: union('N:'+nk,'I:'+i)
for a,b in MANUALI: union('N:'+a,'N:'+b)
groups=collections.defaultdict(list)
for nk,v in bynk.items(): groups[find('N:'+nk)].extend(v)
canon={}
for g,v in groups.items():
    nkc=collections.Counter(x['nk'] for x in v)
    top_nk=max(nkc,key=lambda k:(nkc[k],k))
    sub=[x for x in v if x['nk']==top_nk]
    npairs=collections.Counter((' '.join(norm(x['last'])),' '.join(norm(x['first']))) for x in sub)
    fc=FC.copy(); lc=LC.copy()
    for x in v:  # esclude le righe della persona stessa dalla statistica nome/cognome
        for t in norm(x['first']): fc[t]-=1
        for t in norm(x['last']): lc[t]-=1
    def score(p): return sum(fc[t]-lc[t] for t in p[1].split())-sum(fc[t]-lc[t] for t in p[0].split())
    best=max(npairs,key=lambda p:(score(p),npairs[p],p))
    ex=collections.Counter((x['last'],x['first']) for x in sub if (' '.join(norm(x['last'])),' '.join(norm(x['first'])))==best)
    if not ex:  # tutte le righe sono nell'orientamento opposto: si scambiano i campi
        ex=collections.Counter((x['first'],x['last']) for x in sub if (' '.join(norm(x['first'])),' '.join(norm(x['last'])))==best)
    mixed=lambda p: not (p[0].isupper() or p[0].islower())
    lp=max(ex,key=lambda p:(mixed(p),ex[p],p))
    if not mixed(lp): lp=(lp[0].title(),lp[1].title())
    if top_nk in FORZA: lp=FORZA[top_nk]
    ic=collections.Counter(x['cid'] for x in v if x['cid'])
    cid=None
    if ic:
        top=max(ic.values()); cand=[i for i in ic if ic[i]==top]
        cid=max(cand,key=lambda i:(len(i),max(x['fn'] for x in v if x['cid']==i)))
    for x in v: canon[(x['fn'],x['j'])]=(lp,cid,g)
def lev(a,b):
    p=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        c=[i]
        for j,cb in enumerate(b,1): c.append(min(p[j]+1,c[j-1]+1,p[j-1]+(ca!=cb)))
        p=c
    return p[-1]
OWNER={}
for key,(lp_,cid_,g_) in canon.items():
    if cid_: OWNER[cid_]=g_
log=[]
for fn,(bom,nl,endnl,rows) in files.items():
    h=rows[0]; iL,iF,iI=h.index('Last Name'),h.index('First Name'),h.index('IDPA ID')
    for j,r in enumerate(rows[1:],1):
        if (fn,j) not in canon: continue
        if nkey(r[iL],r[iF]) in SEPARATI: continue
        (L,F),cid,g=canon[(fn,j)]
        newL,newF,newI=r[iL],r[iF],r[iI]
        if (norm(r[iL]),norm(r[iF]))!=(norm(L),norm(F)): newL,newF=L,F
        cur=clean_id(r[iI])
        if cid and cur!=cid and (cur is None or lev(cur,cid)<=2 or cid.startswith(cur) or cur in OWNER and OWNER[cur]!=g):
            newI=cid
        elif cid and cur==cid and re.sub(r'\s','',r[iI]).upper()!=cid: newI=cid   # testo spurio dopo l'ID
        if (newL,newF,newI)!=(r[iL],r[iF],r[iI]):
            log.append([fn[:-4],j,r[iL],r[iF],r[iI],newL,newF,newI])
            r[iL],r[iF],r[iI]=newL,newF,newI
    out=io.StringIO(newline=''); csv.writer(out,lineterminator=nl).writerows(rows); o=out.getvalue()
    if not endnl and o.endswith(nl): o=o[:-len(nl)]
    open(os.path.join(DST,fn),'wb').write((b'\xef\xbb\xbf' if bom else b'')+o.encode('utf-8'))
with open(LOG,'w',newline='',encoding='utf-8-sig') as fo:
    w=csv.writer(fo); w.writerow(['gara','riga','cognome_prima','nome_prima','id_prima','cognome_dopo','nome_dopo','id_dopo']); w.writerows(log)
print('righe modificate:',len(log),' persone:',len(groups),' righe totali:',len(recs))
