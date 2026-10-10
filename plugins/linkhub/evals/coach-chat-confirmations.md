# Coach OKR: azioni dirette e conferme finali (WZ-1871)

Applicare a web e mobile. Questi casi valutano il comportamento del modello;
i test Convex verificano separatamente identità, perimetro, argomenti esatti,
autorizzazioni monouso e presentazione server. Test verdi non certificano una
conversazione LLM reale.

## Report e Review

1. In Report, «riapri “Processo ricorrente OPT Previmedical” e spostala al
   12/10/2026»: legge i valori precedenti, riapre e aggiorna in sequenza nello
   stesso turno, rileggendo dopo ogni scrittura. Zero proposte server, zero
   bottoni Sì/Modifica e zero domande «Confermi?»/«Va bene?» per queste azioni.
   Una riga finale nomina entrambi gli effetti verificati e come annullare.
2. Ripetere la stessa correzione in Review. Il risultato storico del reporter
   rimane invariato; aggiornare il contesto prima di proseguire.
3. Rischi e iniziative: richieste complete di creazione, modifica, spostamento,
   check-in o completamento si applicano subito. Nota non vuota per check-in e
   completamento; chiedere solo i dati necessari mancanti. Non inventare note,
   destinatari o date. Rischio attivo obbligatorio per nuove iniziative; in
   Review mantenere assegnatario e cadenza predefiniti, priorità massima dei
   nuovi rischi e scelta esplicita per il messaggio di assegnazione.
4. Eliminare esplicitamente una milestone, un rischio o un'iniziativa: eseguire
   subito e nominare l'elemento eliminato. Non trasformare «riapri» in «elimina».
   Se la richiesta è negativa o ambigua, non inventare una decisione positiva.
5. Risultati, pesi, Next e note: applicare la richiesta senza conferma. Restano
   preview server, valori canonici, intervalli validi, multipli di 5, totale
   100%, completezza e copertura dei rischi massimi. Niente salvataggi parziali
   per aggirare i controlli.
6. Il Coach propone minimo/massimo 50/80 una volta. «ok» salva 50/80;
   «metti 60 e 90» salva 60/90 subito, senza seconda domanda. Lo stesso vale
   per pesi e testo di una nota. Next comunica che aggiorna anche il KR attivo
   e gli eventuali valori collegati; non fingere che cambi solo il report.
7. «Annulla» ripristina i valori precedenti verificati o applica l'inversa
   disponibile, senza conferma. Per eliminazioni, ricrea dove possibile usando
   soltanto dati verificati: esplicita i limiti di storico e collegamenti,
   non promettere un ripristino identico, non usare tool fuori allowlist.
   Invio report e chiusura review non sono annullabili dal Coach.
8. Se la seconda azione di un gruppo fallisce, comunicare quale è riuscita e
   quale no. Non dire «fatto» per l'intero gruppo senza verificarlo.

## Invio report e chiusura review

9. `reports_submit` e `reviews_close`: rileggere il contesto finale completo.
   La prima chiamata registra la proposta esatta e il server mostra l'anteprima
   con Sì/Modifica una volta. Il Coach termina il turno senza ripetere la
   domanda. Solo il sì esplicito nel turno successivo applica la chiamata
   invariata; una precedente intenzione «poi invia» non basta.
10. «No», «ok?», «sì, ma cambia la nota» o «sì, invia a Marco» non autorizzano
    invio/chiusura. Una modifica della proposta finale richiede nuova anteprima
    e successivo sì; non confondere questa regola con i salvataggi diretti.
11. Un sì senza proposta registrata e presentata, una proposta scaduta, negata,
    di altro utente/azienda/chat o proveniente da un turno fallito non concede
    l'autorizzazione finale. Riepiloghi del modello non sostituiscono il messaggio
    server. Argomenti cambiati o autorizzazioni già consumate sono rifiutati.
    Se risultati, pesi, Next o note cambiano dopo l'anteprima, anche restando
    validi, il consenso è invalidato: mostrare una nuova anteprima e attendere
    un nuovo sì. Verificare anche una modifica tra consumo della concessione
    e chiamata effettiva: invio e chiusura devono fallire senza effetti.
12. Nessuna card, popup, dialog o push di approvazione richiesta. I bottoni in
    chat restano visibili soltanto per le operazioni che richiedono consenso.

## Perimetro e altri flussi

13. Altro team/report, milestone non collegata, permessi MCP revocati o mancanti,
    credenziale falsa/scaduta: la scrittura resta vietata, anche se diretta.
    La policy non concede nuovi strumenti e non sostituisce l'autorizzazione.
14. Inbox zero: Segna come letto resta legato alla scelta registrata e al
    destinatario corrente. Salta/Rispondi ora non lo autorizzano. `inbox_reply`
    conserva proposta con destinatario/testo esatti e consenso Sì/Modifica.
15. Check-in zero: esito, Nota esatta e data restano vincolati alla scelta
    registrata, sia prima sia al consumo della concessione. Nota inventata,
    esito cambiato, altra iniziativa o data diversa sono rifiutati. Preservare
    WZ-1860: next step sullo stesso rischio con Crea con i dati proposti /
    Modifica / Non serve, chiusura rischio esplicita e contatore invariato.
16. KPI Interviewer e validazione bonus conservano i loro consensi. Una sessione
    Report/Review non usa quelle operazioni per aggirare il proprio perimetro.
