"""Calibrazione matrice Pound for Pound (pxp).
Criterio: dopo la correzione, ogni cella divisione x classe deve avere
percentile medio 0.5 nelle classifiche normalizzate delle gare.
Stima: log(score) = gara + divisione + classe + interazione (shrink verso 0 per celle piccole),
residui con mediana (robusta a gare disastrose). coeff = 100*exp(-(effetto_cella - effetto_SSP/SS))."""
import csv, glob, os, math, sys, collections, json, statistics as st
DIVS=['SSP','ESP','CDP','CCP','CO','REV','BUG','PCC']; CLS=['MA','EX','SS','MM','NV']
K_SHRINK=30   # interazione pesata n/(n+K)
def ncls(c):
    c=c.upper().strip(); return 'NV' if c in ('UN','U','UNCLASSIFIED') else c
def load(DIR, files=None):
    rows=[]
    for f in sorted(glob.glob(os.path.join(DIR,'*.csv'))):
        g=os.path.basename(f)[:-4]
        if files and not files(g): continue
        for r in csv.DictReader(open(f,encoding='utf-8-sig')):
            if r.get('Completed')!='1' or r.get('DNF')=='1': continue
            try: s=float(r['Total Score'])
            except: continue
            d=r['Division'].upper().strip(); c=ncls(r['Class'])
            if s<=0 or d not in DIVS or c not in CLS: continue
            rows.append(dict(g=g,d=d,c=c,y=math.log(s)))
    return rows
def fit(rows, iters=60):
    gm=collections.defaultdict(float); a=dict.fromkeys(DIVS,0.0); b=dict.fromkeys(CLS,0.0)
    inter=collections.defaultdict(float)
    eff=lambda r: a[r['d']]+b[r['c']]+inter[(r['d'],r['c'])]
    for _ in range(iters):
        by=collections.defaultdict(list)
        for r in rows: by[r['g']].append(r['y']-eff(r))
        gm={g:st.median(v) for g,v in by.items()}
        for key,par in (('d',a),('c',b)):
            by=collections.defaultdict(list)
            for r in rows: by[r[key]].append(r['y']-gm[r['g']]-eff(r))
            for k,v in by.items(): par[k]+=st.median(v)
        by=collections.defaultdict(list)
        for r in rows: by[(r['d'],r['c'])].append(r['y']-gm[r['g']]-a[r['d']]-b[r['c']])
        for k,v in by.items(): inter[k]=st.median(v)*len(v)/(len(v)+K_SHRINK)
    ref=a['SSP']+b['SS']+inter[('SSP','SS')]
    n=collections.Counter((r['d'],r['c']) for r in rows)
    M={c:{d:round(100*math.exp(-(a[d]+b[c]+inter[(d,c)]-ref))) for d in DIVS} for c in CLS}
    M['SS']['SSP']=100
    return M,n
def pct_test(rows_raw, M):
    by=collections.defaultdict(list)
    for r in rows_raw: by[r['g']].append(r)
    agg=collections.defaultdict(list)
    for g,sh in by.items():
        if len(sh)<10: continue
        sh=sorted(sh,key=lambda r: math.exp(r['y'])*M[r['c']][r['d']]/100)
        for i,r in enumerate(sh):
            p=(i+0.5)/len(sh); agg['D:'+r['d']].append(p); agg['C:'+r['c']].append(p); agg[r['d']+'/'+r['c']].append(p)
    return {k:(len(v),sum(v)/len(v)) for k,v in agg.items()}
if __name__=='__main__':
    DIR=sys.argv[1]
    allr=load(DIR); M,n=fit(allr)
    print('MATRICE (tutte le 30 gare)'); print('     '+' '.join(f'{d:>5}' for d in DIVS))
    for c in CLS: print(f'{c:4s} '+' '.join(f'{M[c][d]:5d}' for d in DIVS))
    print('n:  '); 
    for c in CLS: print(f'{c:4s} '+' '.join(f'{n[(d,c)]:5d}' for d in DIVS))
    # validazione temporale: stima fino al 2026-05-31, test sulle gare dopo
    cut='2026-06'
    Mtr,_=fit(load(DIR,lambda g:g<cut)); te=load(DIR,lambda g:g>=cut)
    old={'MA':dict(SSP=132,ESP=139,CDP=138,CCP=127,CO=139,REV=131,BUG=115,PCC=170),'EX':dict(SSP=118,ESP=120,CDP=114,CCP=108,CO=118,REV=113,BUG=104,PCC=150),'SS':dict(SSP=100,ESP=102,CDP=98,CCP=94,CO=102,REV=88,BUG=84,PCC=134),'MM':dict(SSP=87,ESP=91,CDP=88,CCP=73,CO=89,REV=70,BUG=66,PCC=118),'NV':dict(SSP=71,ESP=79,CDP=71,CCP=66,CO=74,REV=63,BUG=60,PCC=110)}
    t_new=pct_test(te,Mtr); t_old=pct_test(te,old); t_in=pct_test(allr,M)
    print(f'\nVALIDAZIONE: stima su gare < {cut} ({len(set(r["g"] for r in load(DIR,lambda g:g<cut)))}), test su gare >= {cut} ({len(set(r["g"] for r in te))}, {len(te)} risultati)')
    print(f'{"gruppo":9s}{"n":>5} {"vecchia":>8} {"nuova":>7}   {"in-sample":>9}')
    for k in ['C:'+c for c in CLS]+['D:'+d for d in DIVS]:
        if k in t_new: print(f'{k:9s}{t_new[k][0]:5d} {t_old[k][1]:8.3f} {t_new[k][1]:7.3f}   {t_in[k][1]:9.3f}')
    def rms(t): 
        v=[(x[1]-.5)**2*x[0] for k,x in t.items() if '/' in k]; return math.sqrt(sum(v)/sum(x[0] for k,x in t.items() if '/' in k))
    print(f'scarto medio celle (pesato n): vecchia {rms(t_old):.3f}  nuova {rms(t_new):.3f}  in-sample {rms(t_in):.3f}')
    json.dump({'tipo':'idpa-tier0-pfp-matrice','versione':1,'riferimento':'SSP/SS = 100','fonte':'Calibrazione pxp su 30 gare 2025-01..2026-11','data':'2026-11-09','divisioni':DIVS,'classi':CLS,'matrice':M,'n_cella':{c:{d:n[(d,c)] for d in DIVS} for c in CLS}},open('/home/claude/pxp/matrice_pfp_2026-11-09.json','w'),indent=2)
