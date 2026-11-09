# IDPA Tier 0: classifiche compensate

Strumenti per gare IDPA **tier 0** (piccole gare di allenamento) in cui tiratori di classe e divisione diverse competono a tempi compensati. I tiratori conoscono il proprio handicap. **Non** servono a confrontare tiratori nelle gare IDPA ufficiali.

Stato al 9 novembre 2026.

## Cosa c'è e funziona

| Cosa | Dove | Stato |
|---|---|---|
| **pxp** (Pound for Pound), app | `idpa_handicap.html` = `index.html`, pubblicata su https://simonecab.github.io/idpa-tier0-handicap/ (link "IDPA Tier0 pound per pound" su cabasino.com) | in uso, matrice ricalibrata il 9/11/2026 |
| **Team Score**, app | `idpa_team_score.html`, https://simonecab.github.io/idpa-tier0-handicap/idpa_team_score.html | invariata da maggio 2026, solo vettore per divisione |
| Calibrazione pxp | `calibrazione/` | script Python riproducibili |
| Dati | Google Drive `TIER 0/gare` (30 CSV PractiScore, 2025-01-25 .. 2026-11-05) | fuori dal repo |
| Handicap TT (time to target) | definizione e prima prova su 10 gare (agosto 2026), Drive `TIER 0/handicap_tt` | **da fare** su 30 gare, nessuna app |

## pxp: come funziona

Ogni combinazione classe × divisione ha un coefficiente, riferimento **SSP/SS = 100**.

`punteggio compensato = punteggio IDPA × coefficiente / 100` (più basso vince, come in IDPA)

Coefficiente sopra 100: la combinazione è più veloce di SSP/SS e il suo tempo viene aumentato. Sotto 100: più lenta, il tempo viene ridotto. Esempio: MA in CO = 140, cioè un MA in CO è atteso il 40% più veloce di un SS in SSP.

### Matrice in uso (9/11/2026)

| | SSP | ESP | CDP | CCP | CO | REV | BUG | PCC |
|---|---|---|---|---|---|---|---|---|
| MA | 129 | 127 | 113 | 128 | 140 | 97 | 108 | 182 |
| EX | 116 | 113 | 100 | 113 | 120 | 88 | 97 | 163 |
| SS | 100 | 100 | 82 | 97 | 109 | 76 | 86 | 142 |
| MM | 89 | 92 | 80 | 86 | 98 | 69 | 78 | 127 |
| NV | 71 | 77 | 60 | 75 | 79 | 52 | 56 | 107 |

Classe UN (non classificato) trattata come NV.

### Come si usa l'app

1. Scarica da PractiScore l'export CSV dei risultati della gara (formato standard IDPA).
2. Apri l'app, scegli **Individuale** o **Squadra**.
3. Carica il CSV dei risultati. In modalità Squadra carica anche il CSV delle squadre, colonne `nome cognome`, `tessera idpa`, `squadra` (minimo 3 tiratori per squadra). Il tiratore si trova per tessera, poi per nome (anche invertito).
4. In Squadra puoi contare solo i migliori N per squadra (N = squadra più piccola).
5. **Calcola classifica**, poi **Esporta CSV** se serve.

Matrice:
- si modifica a mano nelle celle; la modifica resta salvata **in quel browser** (non si condivide con altri);
- **Esporta matrice** / **Importa matrice** in JSON per passarla ad altri o archiviarla (l'import rifiuta un file con SSP/SS diverso da 100);
- accanto al titolo compaiono fonte e data della matrice in uso;
- **Ripristina default** torna alla matrice calibrata e cancella quella salvata.

Esclusi dal calcolo: tiratori con Completed diverso da 1 o DNF.

## Calibrazione della matrice

**Criterio** (di Simone): con la matrice giusta, nella classifica compensata di ogni gara classi e divisioni si distribuiscono a caso. Misura: percentile del tiratore nella gara (0 = primo, 1 = ultimo); ogni classe, divisione e cella deve avere media 0,5. Sotto 0,5 = troppo premiata, sopra = troppo penalizzata.

**Modello**: `log(score) = gara + divisione + classe + interazione`, stimato con mediane (robusto alle gare andate male). L'interazione di cella è ridotta verso 0 con peso n/(n+30), così le celle con pochi dati seguono la struttura divisione + classe. `coeff = 100 · exp(−(effetto_cella − effetto_SSP/SS))`.

**Risultati**:
- La matrice di maggio 2026 era sbilanciata: percentile medio CDP 0,78 e REV 0,81 (molto penalizzate), CCP 0,38 e CO 0,42 (favorite), MM 0,43.
- Validazione fuori campione (stima su 24 gare fino a maggio 2026, test sulle 6 successive, 812 risultati): scarto medio delle celle da 0,5 sceso da 0,137 a 0,092. CDP 0,79 → 0,48, CCP 0,41 → 0,52, CO 0,44 → 0,53.
- Restano incerte REV (0,59, n 20) e BUG (0,27, n 36): pochi dati.
- Celle con meno di 15 risultati: CDP/MA, REV/MA, REV/EX, REV/MM, REV/NV.
- Controllo incrociato: il vettore della Team Score (maggio, fatto a mano) coincide entro pochi punti con la riga SS della nuova matrice, tranne CDP (89 contro 82).

**Limiti**: i risultati dello stesso tiratore in gare diverse non sono indipendenti (la significatività del test è ottimistica); nessun peso per recenza; il criterio misura la divisione rispetto alla classe dichiarata, quindi corregge anche classi in ritardo sul livello reale (voluto per una tier 0).

### Rifare la calibrazione

Serve Python 3, nessuna libreria esterna.

```
python calibrazione/test_pxp.py "<cartella gare>"     # diagnosi con la matrice di maggio
python calibrazione/calibra_pxp.py "<cartella gare>"  # stima + validazione
```

`calibra_pxp.py` scrive `calibrazione/matrice_pfp_calcolata.json`, importabile nell'app. Per renderla default si aggiorna `DEFAULT_MATRIX` in `idpa_handicap.html` e si copia il file su `index.html`. La cartella gare contiene i CSV PractiScore con nome `AAAA-MM-GG nome gara.csv` (il CSV non contiene né nome né data della gara).

## Pubblicazione

Push sul branch `main`: GitHub Pages pubblica in 1-2 minuti. `index.html` deve essere sempre una copia di `idpa_handicap.html`. Claude pubblica dal cloud tramite l'account GitHub collegato; non servono token sul PC. Gli script `pubblica_*.ps1` / `.bat` (non nel repo) sono obsoleti: leggono il token da `GH_TOKEN` e il `.bat` lancia un file che non esiste.

## Storia

- **Maggio 2026**. Prima app Pound for Pound (`idpa_handicap.html`) con matrice da classifier 5x5 e mediane di 10 gare, metodo non riproducibile. App Team Score con vettore per sola divisione, calibrato a mano su LAWLESS (8/5/2026). Pubblicazione con script PowerShell e token GitHub scritto in chiaro.
- **Agosto 2026**. Dataset di 10 gare dagli export PractiScore; identità del tiratore per nome normalizzato + IDPA ID valido (420 tiratori distinti). Definizione del TT = Total Score / colpi minimi della gara, prima prova su 7 gare (tre senza round count).
- **Novembre 2026, riorganizzazione**. Dati su Google Drive `TIER 0` (30 gare in `gare`, colpi minimi, elaborati TT, classifier). Decisione: coefficienti pxp da rifare da zero.
- **9 novembre 2026**.
  - Token GitHub trapelato negli script: era già scaduto, cancellato; tolto da script e remote git.
  - `index.html` locale conteneva per errore la Team Score: ripristinato.
  - App pxp: salvataggio matrice, import/export JSON, indicazione della fonte.
  - Test del criterio di distribuzione casuale sulle 30 gare, nuova matrice calibrata, validata fuori campione e pubblicata come default.
  - Repo collegato a Claude, pubblicazione dal cloud.

## Prossimi passi aperti

1. **Handicap TT**: ricalcolare su 30 gare, con peso per recenza, per divisione e normalizzato sulla difficoltà della gara (lo stesso termine "gara" del modello pxp). Poi app per i risultati tier 0 a tempi compensati.
2. **Controllo incrociato**: la media dei TT di una classe e divisione deve essere coerente con il coefficiente pxp della stessa cella.
3. **Team Score**: valutare se passarla alla matrice classe × divisione o al vettore preso dalla riga SS.
4. Ricalibrare pxp quando si aggiungono gare; tenere d'occhio REV e BUG.
5. Skill per scaricare e aggiungere al dataset le gare più recenti da PractiScore (lo scaricamento resta manuale).
