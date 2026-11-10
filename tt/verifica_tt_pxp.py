"""Verifica incrociata TT / matrice pxp.
Per ogni cella divisione x classe: TT medio dei tiratori (un valore per tiratore/divisione, classe = ultima).
Se la matrice pxp e' coerente: TT_cella x coeff_cella / 100 ~ TT(SSP/SS) per ogni cella,
cioe' coeff implicito = 100 x TT(SSP/SS) / TT_cella ~ coeff pxp.
Uso: python verifica_tt_pxp.py <cartella gare> [n_min_gare]"""
import sys, os, math, json, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tt_tiratori import leggi, tt_tiratori
M=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','calibrazione','matrice_pfp_2026-11-09.json')))['matrice']
DIVS=['SSP','ESP','CDP','CCP','CO','REV','BUG','PCC']; CLS=['MA','EX','SS','MM','NV']
nmin=int(sys.argv[2]) if len(sys.argv)>2 else 1
res=[x for x in tt_tiratori(leggi(sys.argv[1])) if x['n']>=nmin]
cell=collections.defaultdict(list)
for x in res: cell[(x['div'],x['cls'])].append(x['tt'])
ref=st.mean(cell[('SSP','SS')])
print(f"n_gare >= {nmin}: {len(res)} coppie tiratore/divisione. TT medio SSP/SS = {ref:.3f} s/colpo (n={len(cell[('SSP','SS')])})\n")
print("TT medio per cella (n tiratori)")
print('      '+''.join(f'{d:>13}' for d in DIVS))
for c in CLS: print(f'{c:5s} '+''.join(f"{st.mean(cell[(d,c)]):8.2f}({len(cell[(d,c)]):3d})" if cell[(d,c)] else f"{'-':>13}" for d in DIVS))
print("\nCoeff implicito dal TT = 100 x TT(SSP/SS) / TT cella   [coeff pxp]")
print('      '+''.join(f'{d:>11}' for d in DIVS))
xs=[];ys=[];ws=[]
for c in CLS:
    line=f'{c:5s} '
    for d in DIVS:
        v=cell[(d,c)]
        if v:
            imp=100*ref/st.mean(v); line+=f"{imp:5.0f} [{M[c][d]:3d}]"
            if len(v)>=5 and not (d=='SSP' and c=='SS'): xs.append(math.log(M[c][d])); ys.append(math.log(imp)); ws.append(len(v))
        else: line+=f"{'-':>11}"
    print(line)
n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
r=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
b=sum((a-mx)*(c-my) for a,c in zip(xs,ys))/sum((a-mx)**2 for a in xs)
rms=math.sqrt(sum((y-x)**2 for x,y in zip(xs,ys))/n)
print(f"\nCelle con >=5 tiratori: {n}. Correlazione (log) coeff implicito vs pxp: r = {r:.3f}; pendenza {b:.2f} (1 = stessa scala); scarto rms {100*rms:.1f}%")
