# Calibrazione matrice Pound for Pound (pxp)

- `calibra_pxp.py <cartella gare>`: stima la matrice dai CSV PractiScore (`AAAA-MM-GG nome.csv`), stampa la validazione temporale e scrive il JSON importabile nell'app.
- `test_pxp.py <cartella gare>`: percentile medio per classe, divisione e cella con la matrice di maggio 2026 (0 = primo, 0,5 = neutro).
- `matrice_pfp_2026-11-09.json`: matrice in uso (default dell'app). `matrice_pfp_2026-05.json`: matrice precedente.

I CSV non stanno nel repo: sono su Google Drive, `TIER 0/gare`.
