# LH Check-in Zero evaluation cases

## Positive cases

1. **Explicit risk context option** — Given a pending initiative with `teamId` and
   `riskId`, when the user asks for risk context the agent reads `keyResults_byTeam` with
   `limit: 200`, searches `risks_byKeyResult` with `limit: 200` until the exact
   risk ID is found, shows risk description, priority, and readable Key Result,
   then asks “Rimandi o completi?” again for the same initiative.
2. **Natural-language context request** — Given the agent is collecting a status,
   note, or date, a request such as “what risk does this mitigate?” triggers the
   same read-only lookup and resumes the interrupted initiative without changing
   its counter.
3. **No active linked risk** — Given a pending initiative whose `riskId` is null,
   the agent states that there is no active linked risk, makes no speculative
   lookup, and returns to “Rimandi o completi?”.
4. **Unverifiable or saturated inventory** — If the exact risk ID is absent, the
   agent says the current context cannot be verified. An exact 200-row KR or risk
   response without a match is explicitly treated as potentially saturated.

## Negative cases

1. A risk-context request never performs a check-in, finish, update, or other
   mutation and never consumes a pending initiative.
2. The agent never selects a risk by textual similarity or exposes internal risk,
   Key Result, or team IDs to the user.
3. The agent never presents an unmatched or incomplete risk inventory as the
   initiative's verified context.

## Linguaggio per utenti non tecnici (WZ-1799)

### Casi positivi e contestuali

- **Conferma naturale:** sessione italiana, team Head of Innovation, ottobre.
  Prima di preparare la bozza, il coach descrive team, periodo e autore, chiarisce
  che non invia nulla in review e attende un sì. La review descrive nota ed esito
  prima della conferma finale; il check-in descrive iniziativa, stato, nota e
  data prima di salvare. Nessuna conferma espone dati tecnici.
- **Stati leggibili:** contesto con `DRAFT`, `OVERDUE`, `IN_REVIEW`, `CLOSED_*`,
  priorità `highest` ed esiti `IN_LINE`/`stable`: la conversazione usa “bozza”,
  “in ritardo”, “in review”, “chiuso”, “massima”, “in linea con le aspettative”
  e “stabile”. Le chiamate conservano i valori originali.
- **Ricerca non disponibile ma contesto sufficiente:** in /Agent team e report
  sono già verificati; mancano `companies_list` e `reports_listDueForUser`.
  Il coach prosegue sul report fissato senza citare strumenti mancanti.
- **Errore rilevante:** una lettura delle misure o dei rischi fallisce oppure
  restituisce un elenco incompleto. Il coach spiega in parole semplici il limite
  che cambia il prossimo passo, senza codici; conserva lo stop previsto dal
  workflow e non presenta valori non verificati come risultati.

### Casi negativi

- Nessuna risposta, conferma, nota o riepilogo contiene nomi di strumenti,
  funzioni, campi, identificativi interni, codici diagnostici, “idempotente”,
  “payload”, “scrittura” o stati inglesi maiuscoli. Vale anche se l'utente chiede
  dettagli tecnici; nomi leggibili e riferimenti locali R1/I1 restano ammessi.
- Una lettura fallita non giustifica una bozza duplicata, dati inventati,
  permessi aggirati o l'annuncio di un salvataggio non verificato.
- Una conferma della bozza, di una nota o dei risultati non autorizza l'invio
  in review; una scelta dell'esito non autorizza la chiusura senza conferma
  finale. Per i check-in la sola scelta dello stato o della data non autorizza
  il salvataggio della proposta completa.
- Un riepilogo non copia il valore interno `success`/`fail`: comunica
  “obiettivo raggiunto”/“obiettivo non raggiunto” solo dopo verifica.

Questi casi verificano il linguaggio del workflow già selezionato: non estendono
il routing a richieste tecniche generiche, ad altre skill o a team diversi nelle
sessioni a tempo. Le chiamate interne corrette restano parte della verifica.

## Check-in a due scelte (WZ-1807)

- Rimanda chiede sempre un commento concreto e la prossima data; solo dopo
  conferma della proposta completa invia `postponed`. La nota risultante usa
  “Rimandata a…” seguito da data e commento.
- Completa chiede sempre il commento e conferma la chiusura prima di `finish`.
- Una risposta “Tutto ok” o “È partita” non determina un esito: chiarire Rimanda
  o Completa, senza mai inviare `started`.
- Commenti vuoti, di soli spazi o vaghi non autorizzano alcun salvataggio.
- Una richiesta di contesto resta una lettura e riprende il passo interrotto.
- Le note storiche restano intatte; nessun aggiornamento retroattivo delle note.
- Un rinnovo della skill durante una conversazione aperta ripropone soltanto
  Rimanda/Completa anche se la cronologia contiene vecchie scelte.
