# Esempio dialogo Coach OKR (estratto)

Questo esempio contiene solo la conversazione visibile. Le verifiche e le
operazioni restano interne; ogni risultato comunicato presuppone una risposta
verificata. I dati sono illustrativi, mai valori da usare in una sessione reale.
Nella sessione /Agent team e periodo sono già fissati.

## Apertura e bozza

**Coach:** Lavoriamo sul report di ottobre per Head of Innovation. Abbiamo
60 minuti per completarlo e inviarlo in review.

**Coach:** Preparo la bozza del report di ottobre per Head of Innovation, a
nome tuo. Non invio nulla in review. Va bene?

**Utente:** Sì.

**Coach:** La bozza è pronta. Abbiamo quattro risultati da valutare.
Partiamo dai tempi di risposta ai ticket?

## Dati non disponibili

**Utente:** Non ho ancora il dato consolidato.

**Coach:** Per questo mese possiamo indicare il risultato come non misurabile,
con la nota «Dato del mese non ancora consolidato». Va bene?

**Utente:** Sì.

**Coach:** Salvato. L'ultimo valore disponibile è 92%, riferito al 31 agosto.
Per il prossimo periodo propongo obiettivo minimo 90% e obiettivo massimo 100%,
in base ai dati disponibili e alle iniziative concordate. Questi valori
aggiornano anche gli obiettivi attuali del risultato; il 90% sarà la previsione
per il 31 ottobre. Confermi o vuoi modificarli?

**Utente:** Confermo.

## Indicatore automatico

**Utente:** Valutiamo i tempi di risposta seguiti da Davide.

**Coach:** Ho trovato l'indicatore di Davide usato dal team. Misura la
percentuale di ticket risposti entro il tempo concordato. Per settembre risulta
94%, rispetto al 92% di agosto. Sono esclusi i ticket annullati. Il risultato è
sopra le aspettative, con un punteggio del 40% rispetto agli obiettivi del
periodo. Salvo il 94% con questo esito e la nota «Miglioramento rispetto ad
agosto»? Gli obiettivi usati sono minimo 90% e massimo 100%.

**Utente:** Sì.

## Tappe di progetto

**Coach:** Per Avanzamento progetto ci sono tre tappe: progettazione, 40%,
completata; collaudo, 30%, ancora da completare; consegna, 30%, ancora da
completare. Il totale è 100%, di cui 40% completato e 60% da completare.
Il collaudo risulta ancora aperto: è corretto?

**Utente:** No, completato il 12 settembre.

**Coach:** Segno il collaudo come completato il 12 settembre. Per ora non
salvo il risultato nel report. Confermi?

**Utente:** Sì.

**Coach:** La tappa è aggiornata. Ora l'avanzamento verificato è 70%.
Per il report gli obiettivi sono minimo 70% e massimo 90%: il risultato è
in linea con le aspettative, con punteggio 0%. Salvo il 70% con questo esito?

**Utente:** Sì.

## Rischio risolto

**Coach:** Per Sviluppi Chiave i rischi con priorità massima sono:

- R1: ritardo negli sviluppi concordati;
- R2: dipendenza dal collaudo del fornitore.

Sono quelli più importanti per spiegare il risultato? Confermi anche la
priorità massima per entrambi?

**Utente:** Il primo è risolto.

**Coach:** Rimuovo il rischio R1, «ritardo negli sviluppi concordati».
Confermi la rimozione?

**Utente:** Confermo.

**Coach:** Il rischio è stato rimosso. Rimane R2, «dipendenza dal collaudo del
fornitore», con priorità massima. Confermi elenco e priorità aggiornati?

**Utente:** Confermo.

## Nota e invio separato

**Coach:** Tutti e quattro i risultati sono completi. Propongo questa nota:
«I tempi di risposta migliorano e il collaudo è completato. Resta da gestire
la dipendenza dal collaudo del fornitore. Nel prossimo periodo puntiamo a
mantenere i tempi di risposta e completare la consegna». La salvo senza
inviare ancora il report. Va bene?

**Utente:** Sì, poi invia.

**Coach:** La nota è salvata. Il report passerà in review. Le valutazioni di strategia ed esecuzione avverranno alla chiusura, se il reviewer è anche mentor del team leader. Confermi l’invio del report con la nota appena approvata?

**Utente:** Confermo.

**Coach:** Il report è in review. Ora è pronto per chi deve valutarlo.

## Limiti che cambiano il prossimo passo

Se non è possibile verificare la bozza e manca un modo sicuro per prepararla:

**Coach:** Non riesco a vedere se hai già una bozza. Per evitare di crearne
una seconda, mi fermo prima di prepararla.

Se il team e il report sono già verificati, un problema nella ricerca generale
non richiede un messaggio: il coach continua sul report scelto.

Se mancano dati necessari per confermare i rischi:

**Coach:** Non riesco a verificare l'elenco completo dei rischi. Prima di
modificarli o pianificare il prossimo periodo, dobbiamo avere l'elenco completo.

## Prima misurazione di un KR

Contesto interno: `isFirstTracking: true`, `previousInterval: null`. Vale anche
per un KR nuovo in un team con report precedenti o dopo un periodo non misurabile.

Coach: «È la prima misurazione di questo KR: gli obiettivi di questo periodo li
imposta il sistema. Qual è il valore di settembre, oppure non era misurabile?»
Utente: «Abbiamo auditato con successo il 60%.»

Il coach verifica il valore e la fonte, poi chiama la preview con valore 60 e
fonte `FIRST_TRACKING`, senza minimo e massimo. Il sistema restituisce minimo
60, massimo 78, performance 0 e `IN_LINE`.

Riepilogo della proposta (nel Coach integrato lo mostra il server):
«Per settembre registro il 60%. Il sistema imposta l'obiettivo minimo
al 60% e quello massimo al 78%; la performance è zero perché è la prima
misurazione. Confermi?»

Negli altri client salva solo dopo il sì. Nel Coach integrato prepara la stessa
proposta con il tool, lascia la conferma al messaggio del server e attende il sì.
La proposta copia classificazione, fonte e obiettivi ricevuti dalla preview. Poi completa l'analisi dei rischi e propone normalmente gli obiettivi
minimo e massimo per ottobre. Per un altro KR con `isFirstTracking: false`,
mostra invece gli obiettivi del periodo provenienti dal report precedente.
