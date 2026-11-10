"""TT compensato per tiratore e divisione (solo coppie con almeno N gare, default 2).
TT gara = Total Score / colpi minimi; TT compensato gara = TT / indice di difficolta' della gara (difficolta_gare.py).
TT compensato tiratore/divisione = media dei TT compensati delle sue gare. Classe = ultima gara in quella divisione.
Uso: python tt_compensato.py <cartella gare> <output.csv> [n_min]"""
import sys, os, csv, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_tiratori import leggi
from difficolta_gare import stima
rows=leggi(sys.argv[1]); nmin=int(sys.argv[3]) if len(sys.argv)>3 else 2
D,_,_=stima(rows,lambda r:(r['key'],r['div']))
by=collections.defaultdict(list)
for r in rows: by[(r['key'],r['div'])].append(r)
f=lambda x:f"{x:.3f}".replace('.',',')
out=[]
for (k,d),v in by.items():
    if len(v)<nmin: continue
    v.sort(key=lambda r:r['g'])
    g=[r['tt'] for r in v]; c=[r['tt']/D[r['g']] for r in v]
    nm=collections.Counter(r['nome'] for r in v if not (r['nome'].isupper() or r['nome'].islower()))
    nome=nm.most_common(1)[0][0] if nm else v[-1]['nome'].title()
    ids=collections.Counter(r['id'].upper() for r in v)
    out.append([nome,ids.most_common(1)[0][0],d,v[-1]['cls'],len(v),st.mean(c),st.stdev(c),min(c),max(c),st.mean(g),v[0]['g'][:10],v[-1]['g'][:10]])
out.sort(key=lambda x:(x[2],x[5]))
with open(sys.argv[2],'w',newline='',encoding='utf-8-sig') as fo:
    w=csv.writer(fo,delimiter=';')
    w.writerow(['tiratore','idpa_id','divisione','classe_ultima','n_gare','tt_compensato','dev_std','tt_comp_min','tt_comp_max','tt_grezzo','prima_gara','ultima_gara'])
    for x in out: w.writerow(x[:5]+[f(y) for y in x[5:10]]+x[10:])
print('coppie tiratore/divisione:',len(out),' tiratori:',len(set(x[0].lower() for x in out)))
print('per divisione:',dict(collections.Counter(x[2] for x in out)))
