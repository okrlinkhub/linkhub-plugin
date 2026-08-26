# Esempio dialogo Coach OKR (estratto)

## Apertura

**Coach:** Ciao! Per iniziare il reporting LinkHub: su quale team stiamo lavorando?

**Utente:** Centro Unico Paziente.

**Coach:** *(reports_listDueForUser → report: null)*
Non c'è ancora un DRAFT per maggio — lo creo ora.

*(reports_createDraft { teamId }) → reportId + slug*

**Coach:** DRAFT creato (`centro-unico-paziente-2026-05`). Progresso **0/4** KR. Da quale Key Result partiamo?

## Evaluate — non misurabile

**Coach:** Per lo **SLA maggio**, hai il dato % ticket entro SLA?

**Utente:** No, non ho dati consolidati.

**Coach:** Segno il KR come **non misurabile** con nota esplicativa e passo al next con default (forecast 90, target 100). Confermi?

**Utente:** Sì.

*(resultTracked_markUnmeasurable → resultNext_skipWithDefaults)*

## Evaluate — indicatore automatico da risolvere

**Utente:** Valutiamo lo SLA assegnato a Davide.

**Coach:** *(indicators_listExplainable { query: "Davide SLA", teamId, usage:
"key_result", limit: 50 } → hasMore: false)* Ho trovato l’istanza LinkHub
`sla-davide`, assegnata a Davide e usata come KR di questo team. La risolvo e
leggo la definizione approvata.

*(indicators_resolve { reference: "sla-davide" } → indicatorId;
indicators_getExplanation → defaultMeasureKey + dimensioni)*

**Coach:** *(indicators_queryEvidence summary senza measureKey → ok: true,
resolvedMeasureKey: "sla_percentage")* Il risultato verificato usa la misura
predefinita `sla_percentage` per l’intervallo del report.

Se un breakdown restituisce `hasMore: true`, il coach ripete la stessa richiesta
con `nextCursor` fino a copertura completa e mostra `dimensionLabel` insieme a
`dimensionId`. Se la dimensione `team` non è approvata, si ferma: non usa
`macro_category` come proxy.

## Evaluate — indicatore con milestone

**Coach:** *(reports_getEvaluateContext → hasMilestones: true; milestones_listByIndicator)*
Per **Avanzamento progetto** risultano 3 milestone: 40% completata, 30% in
scadenza e 30% futura. Il totale verificato da LinkHub è `achievedValue: 40`.
La milestone *Collaudo* risulta ancora aperta: è corretto?

**Utente:** No, completata il 12 agosto.

**Coach:** Propongo questa modifica, senza ancora salvare il risultato del KR:
`milestones_complete { milestoneId: "...", achievedAtIso: "2026-08-12" }`.
Confermi?

**Utente:** Sì.

*(mcp_resolveIsoDate → milestones_complete → milestones_listByIndicator)*

**Coach:** Ora LinkHub restituisce `achievedValue: 70`. Propongo quindi
`resultTracked_upsert` con `actualResultValue: 70`; questa è una scrittura
separata. Confermi?

**Utente:** Sì.

*(resultTracked_upsert → resultNext_skipWithDefaults)*

## Analyze — rischio risolto

**Coach:** *(reports_getAnalyzeContext, dopo il tracciamento del risultato)*
Prima di modificare rischi o passare al Next, questi sono i rischi con priorità
`highest` per *Sviluppi Chiave*:

- *Non completo sviluppi CIO KD-126/KD-129*
- *Dipendenza dal collaudo del fornitore*

Confermi sia che sono i rischi più rilevanti per spiegare il risultato al
reviewer, sia che la priorità `highest` è corretta per entrambi?

**Utente:** Sì. Il primo però è risolto.

**Coach:** `reports_getAnalyzeContext` ha restituito l'identificatore
`riskToRemove._id` per *Non completo sviluppi CIO KD-126/KD-129*. Propongo di
chiuderlo con questo payload esatto:

```text
risks_remove { riskId: riskToRemove._id }
```

Confermi?

**Utente:** Confermo.

*(risks_remove { riskId: riskToRemove._id } → reports_getAnalyzeContext)*

**Coach:** L'elenco aggiornato dei rischi `highest` contiene solo *Dipendenza dal
collaudo del fornitore*. Confermi nuovamente elenco e priorità? Dopo la conferma
lo terrò tra i candidati per la nota al reviewer; restano anche 2 iniziative
collegate da rivedere.

**Utente:** Confermo.

## Iniziativa — assignee + commento

**Coach:** Per *APP AM non testata*: ti assegno l'iniziativa e lasci un commento a Mirko Longo (non è nel team)?

**Utente:** Sì, assegna a me.

*(teams_listMembers → initiatives_create con assignmentCommentReceiverId)*

## Chiusura

**Coach:** Tutti e 4 i KR sono completi. Ecco la **nota al reviewer** che propongo — la modifichi o invio?

Rischi `highest`:

- Dipendenza dal collaudo del fornitore
- Disponibilità limitata del team integrazioni

*(mostra le altre sezioni di reporterNotes; la lista contiene solo i nomi di
massimo 3 rischi confermati)*

**Utente:** Va bene, submit.

*(reports_getSubmitContext → Davide Campofranco, defaultAnswer: "stable")*

**Coach:** Prima dell'invio registro il check-in OTO di Davide come stabile. Payload finale separato:

```json
{
  "reportId": "<reportId>",
  "otoCheckins": [
    { "menteeId": "<davideUserId>", "answer": "stable" }
  ]
}
```

Confermi questo submit definitivo?

**Utente:** Confermo.

*(reports_submit con il payload mostrato)*

**Coach:** Report in **IN_REVIEW**. Il reviewer riceverà email con la nota. Prossimo passo: attendere review o aprire dashboard report.
