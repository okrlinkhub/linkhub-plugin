# Inbox zero: un solo contatore (WZ-1884)

## Casi positivi

- Con tre conversazioni assegnate non lette, la Fase 0 conserva «📬 Inbox non letta: 3 messaggi». Il primo messaggio ha `[1/3]` nell’intestazione, poi sintesi, domanda e opzioni. Non compare «3 rimaste» sotto il messaggio.
- Dopo aver letto la prima conversazione, la seconda ha `[2/3]`, senza ridurre il denominatore a 2; la terza ha `[3/3]`.
- Dopo un salto, la conversazione resta non letta ma l’avanzamento del giro procede. A fine giro si rileggono riepilogo e lista: un eventuale nuovo giro riparte da `[1/N]` sul nuovo insieme.
- Con riepilogo limitato si conserva «almeno N» e l’intestazione usa `[X/almeno N]`; nessuna dichiarazione di totale esatto o Inbox zero su campione saturato.

## Casi contestuali e negativi

- In inglese valgono le stesse regole: nessun «N remaining» sotto il messaggio. Fuori dal Coach integrato, le azioni sono in testo naturale ma il contatore resta solo nell’intestazione.
- Le menzioni restano escluse dal conteggio. Un nuovo messaggio durante il giro non altera retroattivamente il denominatore; viene verificato nel riepilogo successivo.
- La modifica della presentazione non autorizza letture o risposte senza la scelta dell’utente e non modifica il routing della skill.
- Non si aggiungono contatori duplicati nelle opzioni o dopo la sintesi. Zero può essere dichiarato solo dal riepilogo non limitato verificato.
