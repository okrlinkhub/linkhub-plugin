---
name: coach-cluster-report
description: >-
  Facilita la rendicontazione contemporanea dei team presenti in un Cluster
  LinkHub, con coach amministratore company via OAuth personale, preparazione
  per aree tematiche e invio separato di ogni report in revisione. Usa per un
  workshop di report del Cluster; per il report di un solo team usa
  linkhub-report-coach e per la review usa linkhub-review-coach.
---

# Workshop report del Cluster

Rispondi nella lingua del gruppo. Il coach è admin company con OAuth personale. I report vanno al normale reviewer, il Cluster Leader. Il team del Cluster Leader rendiconta nel workshop del proprio Cluster e resta fuori da questo inventario. Non mostrare sullo schermo condiviso nomi, trend o altre valutazioni individuali OTO.

## 1. Apri il workshop

Con `mcp_membershipProfile`, `companies_list` e `workshops_discoverCluster` identifica il Cluster scelto. Chiedi **quali team sono presenti**. Se il team Cluster Leader manca o gli elenchi sono troncati, ferma l'avanzamento dipendente dall'inventario. Leggi `workshops_listCollaborations` fino a `isDone` e `workshops_listDueReports`; presenta la strategia comune, le aree tematiche e le collaborazioni verticali verificate. Se una collaborazione attesa manca, segnala il gap senza inventarla. L'inventario dei report comprende i team del Cluster anche se il coach non ne è membro; lavora solo sui presenti, registra gli assenti come facoltativi.

Invita i team presenti a preparare **contemporaneamente** per area tematica: KR e pesi, risultati e fonti, rischi `highest`, iniziative, obiettivo minimo/massimo del prossimo periodo e nota per il Cluster Leader. Raccogli poi un team alla volta. La preparazione parallela non cambia l'ordine delle scritture MCP per ciascun KR.

## 2. Start del periodo che si chiude

Per ogni team crea o riprendi una bozza con `reports_createDraft` dopo aver mostrato team e periodo e ottenuto consenso. Leggi `reports_getWorkflowProgress`, `objectives_byTeam`, `keyResults_byTeam` e tutte le pagine di `initiatives_byTeam`. Le modifiche ai KR e ai pesi fatte in **Start** valgono per il periodo che si sta chiudendo; non presentarle come sola pianificazione futura.

Prima di togliere un KR, chiedi se il team intende **completarlo con peso zero** e mantenerlo nella rendicontazione, oppure **eliminarlo davvero** ed escluderlo dal report. Mostra per entrambe le scelte l'effetto su snapshot, risultato e pesi; evidenzia la cancellazione come azione distruttiva e chiedi conferma distinta. Usa `resultTracked_markCompleted` per il primo caso, poi registra il risultato con evidenza oppure come non misurabile nella fase Evaluate, così il KR a peso zero resta nel report. Usa `workshops_removeKeyResultFromDraft` solo quando la vera eliminazione è esplicita: rimuove il KR e i suoi snapshot dalla bozza corrente. Ribilancia i pesi con `keyResults_rebalanceWeightInDraftReport` dopo una proposta leggibile e verifica il totale del periodo chiuso pari a 100% per i KR rendicontati. Se il backend rifiuta una rimozione o lo snapshot non è coerente, ferma quel report e non simularne l'esito.

## 3. Evaluate → Analyze → Next, in sequenza per KR

Per ogni KR segui nell'ordine la procedura di `linkhub-report-coach`: `reports_getEvaluateContext` → risultato verificato oppure `resultTracked_markUnmeasurable`/`resultTracked_markCompleted` → `reports_getAnalyzeContext` e rischi/iniziative → `resultNext_upsert` o `resultNext_skipWithDefaults` dopo la proposta dei valori. Non saltare Analyze né proporre Next da un elenco rischi potenzialmente troncato. Presenta ogni gruppo di scritture in parole leggibili e attendi il consenso relativo.

Per indicatori automatici usa `indicators_getExplanation` e `indicators_queryEvidence` sul periodo approvato; per milestone rileggi `milestones_listByIndicator` prima del risultato. Distingui dato non misurabile da zero. Non inventare actual, forecast, target, fonte, rischio o iniziativa. Mostra tutti i rischi `highest` del KR e chiedi se spiegano il risultato; non imporre la regola reviewer di un `highest` per ogni KR. Le nuove iniziative mitigano rischi identificati e hanno owner e check-in concordati. Per Next mostra valore operativo con data, limiti delle evidenze e proposta concreta di **obiettivo minimo** e **obiettivo massimo** coerente con la direzione della metrica. Controlla `reports_getWorkflowProgress` ogni uno o due KR.

## 4. Nota, consenso e invio per ciascun team

Prepara una nota breve per il Cluster Leader con risultati confermati, limiti di misura, fino a tre rischi `highest` scelti dal team e focus successivo. Mostrala prima di `reports_updateReporterNotes`. Presenta poi **il report completo del singolo team** al gruppo: KR, pesi del periodo chiuso, risultati e non misurabili, rischi, iniziative, obiettivi minimo/massimo, nota e stato di completezza. Raccogli consenso collettivo sulla versione mostrata. Se negato, conserva la bozza e risolvi le obiezioni; non inviare.

Per quel team chiedi una **nuova conferma finale di invio**, distinta dal consenso alle modifiche e dalle conferme degli altri team. Dichiara che l'invio mette il report in revisione e registra automaticamente `stable` per gli eventuali candidati OTO idonei, con il coach come autore, senza mostrarne i dati individuali. Solo dopo un sì esplicito chiama `workshops_submitTeamReport` per il report corrente. Rileggi l'inventario e comunica lo stato restituito. Un report bloccato non impedisce di lavorare sulle altre bozze, ma non va dichiarato inviato. Per una bozza ripresa, rileggi progress e dati attuali prima di nuove proposte; non riutilizzare vecchie conferme.

## 5. Consegna operativa

Dopo gli invii, per ogni team presente leggi **tutte** le pagine di `workshops_listTeamCheckins`; conta solo le righe con `overdue: true` e consegna il numero verificato delle iniziative attive con check-in scaduto. Una pagina vuota non conclude l'inventario finché `isDone` non è vero. Elenca separatamente le nuove iniziative concordate durante il workshop e chiedi al team di seguirne l'esecuzione. Non svolgere i check-in scaduti al posto dei team in questa seduta. Concludi con stato del report per team, eventuali bozze bloccate e follow-up.

Per campi e flussi dettagliati usa [gli strumenti del report coach](../linkhub-report-coach/reference-mcp-tools.md) e [il protocollo evidenze](../linkhub-report-coach/indicator-evidence.md).
