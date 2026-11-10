"""Dal file tt_compensato (CSV ';' con decimali a virgola) al CSV pubblico per il Google Sheet TT_handicap_pubblico:
niente IDPA ID, TT in millisecondi interi, ordine alfabetico per tiratore e divisione.
Uso: python esporta_pubblico.py <tt_compensato.csv> <tt_handicap_pubblico.csv> <AAAAMMGG>"""
import csv, sys
r=list(csv.DictReader(open(sys.argv[1],encoding='utf-8-sig'),delimiter=';'))
r.sort(key=lambda x:(x['tiratore'].lower(),x['divisione']))
with open(sys.argv[2],'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['tiratore','divisione','classe_ultima','n_gare','tt_ms','dev_std_ms','aggiornato'])
    for x in r: w.writerow([x['tiratore'],x['divisione'],x['classe_ultima'],x['n_gare'],round(float(x['tt_compensato'].replace(',','.'))*1000),round(float(x['dev_std'].replace(',','.'))*1000),sys.argv[3]])
print(len(r),'righe')
