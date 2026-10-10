# Esempio dialogo Coach Report (WZ-1871)

I dati sono illustrativi. Ogni esito presuppone chiamate riuscite e rilettura;
non usare questi valori in una sessione reale. Team e periodo sono fissati.

## Bozza

**Coach:** La bozza del report di ottobre per Head of Innovation è pronta.
Abbiamo 60 minuti per completarla e inviarla in review.

## Richiesta multipla e annullamento

**Utente:** Riapri “Processo ricorrente OPT Previmedical” e spostala al 12/10/2026.

Il Coach legge lo stato precedente, riapre, rilegge, cambia la data e rilegge
ancora, tutto nello stesso turno e senza bottoni di conferma.

**Coach:** Fatto: riaperta “Processo ricorrente OPT Previmedical” e data prevista
12/10/2026. Se vuoi annullare, dimmelo.

**Utente:** Annulla.

**Coach:** Fatto: ripristinati completamento e data precedenti. Se vuoi cambiare
qualcosa, dimmelo.

## Valori proposti una volta

**Coach:** L'ultimo valore disponibile è 92%, al 31/08/2026. Per il prossimo
periodo propongo obiettivo minimo 90% e massimo 100%; aggiorneranno anche gli
obiettivi del KR attivo e la previsione del 31/10/2026. Quali valori applico?

**Utente:** Metti 60 e 90.

**Coach:** Fatto: salvati minimo 60% e massimo 90%, anche nel KR attivo e nella
previsione collegata. Se vuoi annullare, dimmelo.

## Eliminazione richiesta

**Utente:** Elimina R1, “ritardo negli sviluppi concordati”.

**Coach:** Fatto: eliminato R1, “ritardo negli sviluppi concordati”. Posso
ricrearlo dai dati precedenti se me lo chiedi; storico e collegamenti potrebbero
non essere recuperati.

## Prima misurazione

Con `isFirstTracking: true`, chiedi solo risultato misurato o motivo di
non misurabilità, poi usa `reports_previewTrackedResult` senza minimo/massimo.
Prima del salvataggio presenta il risultato, l’intervallo, il punteggio e la
classificazione restituiti dalla preview, con la fonte e l’eventuale nota.
Poi salva gli obiettivi restituiti senza chiedere un’altra conferma.

**Utente:** Abbiamo auditato con successo il 60%.

**Coach:** Fatto: registrato il 60%; gli obiettivi calcolati dal sistema sono
minimo 60% e massimo 78%. Se vuoi correggere il risultato, dimmelo.

## Nota e invio

**Coach:** Propongo questa nota: “I tempi di risposta migliorano; resta da
gestire il collaudo del fornitore”. Quale testo salvo?

**Utente:** Ok, poi invia.

**Coach:** Fatto: nota salvata. Se vuoi cambiarla, dimmelo.

Il Coach rilegge `reports_getSubmitContext`, prepara `reports_submit` e lascia
al server l'unica anteprima finale con Sì/Modifica. L'intenzione precedente
«poi invia» non sostituisce il sì successivo all'anteprima completa.

**Utente:** Sì.

**Coach:** Il report è stato inviato in review e non è più modificabile da te.

## Limiti

Una lettura incompleta, valori mancanti o permessi negati non autorizzano
salvataggi inventati. Descrivi il limite senza dettagli tecnici. Non dichiarare
successo per un gruppo applicato solo in parte.
