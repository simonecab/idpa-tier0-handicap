"""Genera idpa_tt.html. La tabella TT si legge a runtime dal Google Sheet pubblico; nel file c'e' una copia di riserva.
Uso: python tt/build_app.py <tt_handicap_pubblico.csv> <id Google Sheet>"""
import csv, json, os, sys
src,sheet=sys.argv[1],sys.argv[2]; here=os.path.dirname(os.path.abspath(__file__))
rr=list(csv.DictReader(open(src,encoding='utf-8-sig')))
rows=[[r['tiratore'],r['divisione'],r['classe_ultima'],int(r['n_gare']),int(r['tt_ms']),int(r['dev_std_ms'])] for r in rr]
d=rr[0]['aggiornato']; d=f"{d[6:8]}/{d[4:6]}/{d[:4]}"
t=open(os.path.join(here,'idpa_tt.html.tpl'),encoding='utf-8').read()
t=t.replace('__TT_JSON__',json.dumps(rows,ensure_ascii=False,separators=(',',':'))).replace('__TT_DATA__',d).replace('__SHEET_ID__',sheet)
open(os.path.join(here,'..','idpa_tt.html'),'w',encoding='utf-8').write(t)
print('idpa_tt.html:',len(rows),'righe di riserva, sheet',sheet)
