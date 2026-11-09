import csv, glob, os, math, sys, collections
DIR = sys.argv[1]
M = {
 'MA': dict(SSP=132,ESP=139,CDP=138,CCP=127,CO=139,REV=131,BUG=115,PCC=170),
 'EX': dict(SSP=118,ESP=120,CDP=114,CCP=108,CO=118,REV=113,BUG=104,PCC=150),
 'SS': dict(SSP=100,ESP=102,CDP=98,CCP=94,CO=102,REV=88,BUG=84,PCC=134),
 'MM': dict(SSP=87,ESP=91,CDP=88,CCP=73,CO=89,REV=70,BUG=66,PCC=118),
 'NV': dict(SSP=71,ESP=79,CDP=71,CCP=66,CO=74,REV=63,BUG=60,PCC=110)}
def ncls(c):
    c=c.upper().strip(); return 'NV' if c in ('UN','U','UNCLASSIFIED') else c
rows=[]; skipped=collections.Counter(); unc=0
for f in sorted(glob.glob(os.path.join(DIR,'*.csv'))):
    g=os.path.basename(f)[:-4]
    sh=[]
    for r in csv.DictReader(open(f,encoding='utf-8-sig')):
        if r.get('Completed')!='1' or r.get('DNF')=='1': skipped['incompleto/DNF']+=1; continue
        try: s=float(r['Total Score'])
        except: skipped['score non numerico']+=1; continue
        if s<=0: skipped['score<=0']+=1; continue
        d=r['Division'].upper().strip(); c=ncls(r['Class'])
        if r['Class'].upper().strip() in ('UN','U'): unc+=1
        if c not in M or d not in M[c]: skipped[f'cella {d}/{c} assente']+=1; continue
        sh.append(dict(g=g,d=d,c=c,raw=s,adj=s*M[c][d]/100))
    n=len(sh)
    if n<10: skipped[f'gara con <10 tiratori ({g})']+=n; continue
    sh.sort(key=lambda x:x['adj'])
    for i,x in enumerate(sh): x['pct']=(i+0.5)/n  # 0 = migliore
    rows+=sh
print(f"gare usate: {len(set(r['g'] for r in rows))}, tiratori-gara: {len(rows)}, di cui UN->NV: {unc}")
for k,v in skipped.items(): print('  escluso:',k,v)
def table(key,label):
    agg=collections.defaultdict(list)
    for r in rows: agg[key(r)].append(r['pct'])
    print(f"\n{label:10s}   n   pct medio   z")
    for k in sorted(agg, key=lambda k: sum(agg[k])/len(agg[k])):
        v=agg[k]; m=sum(v)/len(v); z=(m-0.5)/(1/math.sqrt(12*len(v)))
        flag='  <<' if abs(z)>3 else ('  <' if abs(z)>2 else '')
        print(f"{str(k):10s} {len(v):4d}   {m:6.3f}   {z:+6.1f}{flag}")
    return agg
table(lambda r:r['c'],'CLASSE')
table(lambda r:r['d'],'DIVISIONE')
agg=table(lambda r:f"{r['d']}/{r['c']}",'CELLA')
