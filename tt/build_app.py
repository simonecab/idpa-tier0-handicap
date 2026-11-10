"""Genera idpa_tt.html incorporando la tabella TT compensato.
Uso: python tt/build_app.py <tt_compensato_AAAA-MM-GG.csv>"""
import csv, json, os, sys
src=sys.argv[1]; here=os.path.dirname(os.path.abspath(__file__))
rows=[[r['tiratore'],r['idpa_id'],r['divisione'],r['classe_ultima'],int(r['n_gare']),float(r['tt_compensato'].replace(',','.')),float(r['dev_std'].replace(',','.'))]
      for r in csv.DictReader(open(src,encoding='utf-8-sig'),delimiter=';')]
t=open(os.path.join(here,'idpa_tt.html.tpl'),encoding='utf-8').read()
t=t.replace('__TT_JSON__',json.dumps(rows,ensure_ascii=False,separators=(',',':'))).replace('__TT_NOME__',os.path.basename(src))
open(os.path.join(here,'..','idpa_tt.html'),'w',encoding='utf-8').write(t)
print('idpa_tt.html:',len(rows),'righe TT')
