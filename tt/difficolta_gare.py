"""Difficolta' delle gare e TT compensato.
Modello: log(TT) = difficolta_gara + livello(tiratore, divisione). Stima a mediane alternate (robusta).
Informano la stima solo le coppie tiratore/divisione con almeno 2 gare: lo stesso tiratore in gare diverse
dice quanto una gara e' piu' lenta dell'altra, senza dipendere da chi era presente.
Indice di difficolta' D = exp(effetto gara), normalizzato a media geometrica 1 sulle gare usate.
D = 1,10: nella gara ogni tiratore impiega il 10% in piu' per colpo rispetto alla gara media.
TT compensato = TT / D. Controllo: stessa stima col modello pxp (gara + divisione x classe).
Uso: python difficolta_gare.py <cartella gare> <difficolta.csv> [nome tiratore]"""
import sys, os, math, csv, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_tiratori import leggi
from colpi_minimi import COLPI
def stima(rows, chiave, iters=200):
    by=collections.defaultdict(list)
    for r in rows: by[chiave(r)].append(r)
    use=[r for r in rows if len(by[chiave(r)])>=2]
    G=collections.defaultdict(float); S=collections.defaultdict(float)
    for _ in range(iters):
        t=collections.defaultdict(list)
        for r in use: t[chiave(r)].append(math.log(r['tt'])-G[r['g']])
        S={k:st.median(v) for k,v in t.items()}
        t=collections.defaultdict(list)
        for r in use: t[r['g']].append(math.log(r['tt'])-S[chiave(r)])
        G={k:st.median(v) for k,v in t.items()}
    m=st.mean(G.values())
    n=collections.Counter(r['g'] for r in use)
    res=collections.defaultdict(list)
    for r in use: res[r['g']].append(math.log(r['tt'])-S[chiave(r)]-G[r['g']])
    return {g:math.exp(v-m) for g,v in G.items()}, n, {g:1.4826*st.median(abs(x) for x in v)/math.sqrt(len(v)) for g,v in res.items()}
if __name__=='__main__':
    rows=leggi(sys.argv[1])
    D,n,se=stima(rows,lambda r:(r['key'],r['div']))
    Dc,_,_=stima(rows,lambda r:(r['div'],r['cls']))
    tot=collections.Counter(r['g'] for r in rows); med=collections.defaultdict(list)
    for r in rows: med[r['g']].append(r['tt'])
    f=lambda x,d=3:f"{x:.{d}f}".replace('.',',')
    with open(sys.argv[2],'w',newline='',encoding='utf-8-sig') as fo:
        w=csv.writer(fo,delimiter=';')
        w.writerow(['gara','colpi_minimi','tiratori','tiratori_usati_stima','tt_mediano_grezzo','difficolta','errore_std','difficolta_controllo_pxp'])
        for g in sorted(D): w.writerow([g,COLPI[g],tot[g],n[g],f(st.median(med[g])),f(D[g]),f(se[g]),f(Dc[g])])
    print(f"{'gara':44s} colpi   n  usati TTmed  diff   ±    diff_pxp")
    for g in sorted(D): print(f"{g[:44]:44s} {COLPI[g]:4d} {tot[g]:4d} {n[g]:4d}  {st.median(med[g]):.2f}  {D[g]:.3f} {se[g]:.3f}  {Dc[g]:.3f}")
    xs=[math.log(D[g]) for g in D]; ys=[math.log(Dc[g]) for g in D]; mx=st.mean(xs); my=st.mean(ys)
    print('correlazione fra le due stime: r = %.3f'%(sum((a-mx)*(b-my) for a,b in zip(xs,ys))/math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))))
    if len(sys.argv)>3:
        who=sys.argv[3].lower(); mine=[r for r in rows if who in r['nome'].lower()]
        for k,d in sorted(set((r['key'],r['div']) for r in mine)):
            v=[r for r in mine if r['div']==d and r['key']==k]
            print(f"\n{v[0]['nome']} {d}: {len(v)} gare")
            for r in v: print(f"  {r['g'][:40]:40s} {r['cls']}  TT {r['tt']:.3f}  diff {D[r['g']]:.3f}  TT comp {r['tt']/D[r['g']]:.3f}")
            a=[r['tt'] for r in v]; b=[r['tt']/D[r['g']] for r in v]
            sd=lambda x: st.stdev(x) if len(x)>1 else 0
            print(f"  media grezzo {st.mean(a):.3f} (dev.std {sd(a):.3f}, min {min(a):.3f}, max {max(a):.3f})")
            print(f"  media compensato {st.mean(b):.3f} (dev.std {sd(b):.3f}, min {min(b):.3f}, max {max(b):.3f})")
