"""TT (time per target) per tiratore e divisione, prima approssimazione (decisioni del 10/11/2026):
- TT di una gara = Total Score (tempo finale, PD e penalita' incluse) / colpi minimi della gara.
- Gare senza colpi minimi (ND) escluse. Nessun peso per recenza. Nessuna normalizzazione sulla difficolta' della gara.
- Esclusi DNF e Completed != 1.
- TT tiratore/divisione = media aritmetica dei TT delle sue gare in quella divisione.
- Classe di riferimento = classe nell'ultima gara corsa in quella divisione.
- Identita': nome normalizzato (i CSV in 'gare' sono gia' unificati da dati/correggi_identita.py).
Uso: python tt_tiratori.py <cartella gare> <output.csv>"""
import csv, glob, os, re, sys, unicodedata, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colpi_minimi import COLPI
def norm(s): return ' '.join(sorted(re.sub(r'[^a-z ]',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).split()))
def cls(c):
    c=c.upper().strip(); return 'NV' if c in ('UN','U','') else c
def leggi(D):
    out=[]
    for f in sorted(glob.glob(os.path.join(D,'*.csv'))):
        g=os.path.basename(f)[:-4]; c=COLPI.get(g)
        if not c: continue
        for r in csv.DictReader(open(f,encoding='utf-8-sig')):
            if r['Completed']!='1' or r['DNF']=='1': continue
            try: s=float(r['Total Score'])
            except ValueError: continue
            if s<=0: continue
            out.append(dict(g=g,key=norm(r['Last Name']+' '+r['First Name']),nome=f"{r['Last Name']} {r['First Name']}",
                            id=r['IDPA ID'],div=r['Division'].upper().strip(),cls=cls(r['Class']),tt=s/c))
    return out
def tt_tiratori(rows):
    by=collections.defaultdict(list)
    for r in rows: by[(r['key'],r['div'])].append(r)
    res=[]
    for (k,d),v in by.items():
        v.sort(key=lambda r:r['g'])
        res.append(dict(nome=v[-1]['nome'],id=v[-1]['id'],div=d,cls=v[-1]['cls'],n=len(v),tt=st.mean(r['tt'] for r in v),
                        tt_min=min(r['tt'] for r in v),tt_max=max(r['tt'] for r in v),prima=v[0]['g'][:10],ultima=v[-1]['g'][:10]))
    return res
if __name__=='__main__':
    rows=leggi(sys.argv[1]); res=tt_tiratori(rows)
    res.sort(key=lambda x:(x['div'],x['tt']))
    with open(sys.argv[2],'w',newline='',encoding='utf-8-sig') as fo:
        w=csv.writer(fo,delimiter=';')
        w.writerow(['tiratore','idpa_id','divisione','classe_ultima','n_gare','tt_medio','tt_min','tt_max','prima_gara','ultima_gara'])
        for x in res: w.writerow([x['nome'],x['id'],x['div'],x['cls'],x['n'],f"{x['tt']:.3f}".replace('.',','),f"{x['tt_min']:.3f}".replace('.',','),f"{x['tt_max']:.3f}".replace('.',','),x['prima'],x['ultima']])
    print('risultati usati',len(rows),' gare',len(set(r['g'] for r in rows)),' coppie tiratore/divisione',len(res),' tiratori',len(set(x['nome'] for x in res)))
    c=collections.Counter(x['n'] for x in res); print('distribuzione n_gare:',sorted(c.items()))
