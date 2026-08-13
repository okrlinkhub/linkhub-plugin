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

## Analyze — rischio risolto

**Coach:** Sul KR *Sviluppi Chiave*, il rischio *«Non completo sviluppi CIO KD-126/KD-129»* è ancora aperto?

**Utente:** No, risolto.

**Coach:** Lo chiudo con soft-delete. Restano 2 iniziative collegate — le rivediamo?

*(risks_remove)*

## Iniziativa — assignee + commento

**Coach:** Per *APP AM non testata*: ti assegno l'iniziativa e lasci un commento a Mirko Longo (non è nel team)?

**Utente:** Sì, assegna a me.

*(teams_listMembers → initiatives_create con assignmentCommentReceiverId)*

## Chiusura

**Coach:** Tutti e 4 i KR sono completi. Ecco la **nota al reviewer** che propongo — la modifichi o invio?

*(mostra testo reporterNotes)*

**Utente:** Va bene, submit.

*(reports_submit)*

**Coach:** Report in **IN_REVIEW**. Il reviewer riceverà email con la nota. Prossimo passo: attendere review o aprire dashboard report.
