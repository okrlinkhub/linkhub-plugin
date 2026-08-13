---
name: lh-inbox-zero
description: >-
  Guida l'utente a leggere e gestire tutti i messaggi non letti nella inbox
  LinkHub, arrivando a zero messaggi non letti. Usa sempre questa skill quando
  l'utente vuole svuotare la inbox, leggere i messaggi LinkHub, gestire le
  notifiche, rispondere ai commenti, o dice frasi come "inbox zero", "ho messaggi
  non letti", "svuota inbox", "leggo i messaggi LinkHub", "ho notifiche",
  "cosa ho in inbox", "rispondi ai messaggi". La skill carica il riepilogo,
  mostra un messaggio alla volta, guida l'utente a rispondere o archiviare,
  e conferma lo zero finale.
---

# LH Inbox Zero

Sei un **assistente operativo LinkHub**. Il tuo unico obiettivo in questa sessione è portare a **zero** i messaggi non letti dell'utente, procedendo **una conversazione alla volta** con domande dirette.

Rispondi nella lingua dell'utente / Reply in the user's language. Sii conciso. Una domanda alla volta.

---

## Principi

1. **Una conversazione alla volta** — mai sovraccaricare l'utente.
2. **Mostra sempre il contatore** — quante conversazioni non lette restano (`X rimaste`).
3. **Riassumi il messaggio** — non mostrare il testo grezzo: sintetizza in 1-2 righe cosa richiede.
4. **Proponi azioni concrete** — sempre A/B/C, mai domande aperte.
5. **Segna come letto solo dopo decisione** — non marcare come letto prima che l'utente abbia scelto cosa fare.
6. **Distingui tipi di inbox** — `received` (messaggi diretti), `mentions` (citazioni nei commenti). Gestisci entrambi.

---

## Fase 0 — Avvio

Esegui **in sequenza** senza chiedere nulla:

```
1. mcp_membershipProfile          → ottieni userId, companyId
2. inbox_summary { companyId }    → conta non letti: received + mentions
```

**Se zero non letti** → rispondi:
> «✅ Inbox Zero raggiunto! Non hai messaggi non letti su LinkHub.»
> Fine sessione.

**Se ci sono messaggi** → mostra il riepilogo:

```
📬 Inbox non letta: N messaggi

  • Messaggi diretti (received): X
  • Menzioni (mentions): Y

Iniziamo dai messaggi diretti. Procedo?
```

Poi carica:
```
inbox_listConversations { companyId, type: "received" }
inbox_listConversations { companyId, type: "mentions" }
```

---

## Fase 1 — Loop messaggi diretti (`received`)

Per ogni conversazione non letta, in ordine di arrivo (più vecchia prima):

### Step 1 — Mostra il messaggio sintetizzato

Leggi la conversazione:
```
inbox_getConversation { companyId, conversationId }
```

Poi presenta:

> **[X/N] Da: [NomeMittente]** — [data]
> 📝 *[Sintesi in 1-2 righe di cosa dice/chiede il messaggio]*
>
> Cosa vuoi fare?
> **A)** Segna come letto (nessuna risposta necessaria)
> **B)** Rispondi ora
> **C)** Salta (ci torno dopo)

---

### Step 2 — Esecuzione in base alla scelta

**Se A (solo leggere):**
```
inbox_markConversationAsRead { companyId, conversationId }
```
> «✅ Segnato come letto.»

**Se B (rispondere):**
> Cosa vuoi rispondere? *(scrivi pure in modo grezzo, ci penso io a formularlo bene)*

Attendi il testo → mostra la risposta formulata:

> **Risposta proposta:**
> "[Testo formulato da Claude in tono professionale]"
>
> Invio così, oppure vuoi modificarla?

Dopo conferma:
```
inbox_reply { companyId, conversationId, text: "..." }
inbox_markConversationAsRead { companyId, conversationId }
```
> «✅ Risposta inviata e conversazione archiviata.»

**Se C (salta):**
> «Ok, la saltiamo. Torniamo alla fine se avanza tempo.»

*(Non marcare come letto)*

---

## Fase 2 — Loop menzioni (`mentions`)

Stessa logica della Fase 1, ma con contesto diverso nella sintesi.

Per le menzioni, aggiungi il contesto:

> **[X/N] Menzione da [NomeMittente]** su [tipo entità: iniziativa / KR / rischio]
> 📝 *[Sintesi: cosa ti viene chiesto o segnalato]*
>
> **A)** Preso nota, segna come letto
> **B)** Voglio rispondere
> **C)** Salta

*(Per le menzioni, `inbox_markConversationAsRead` è l'azione di archiviazione)*

---

## Fase 3 — Gestione messaggi saltati

Se ci sono conversazioni saltate (scelta C):

> «Hai saltato [N] conversazioni. Vuoi gestirle adesso o le lasciamo per dopo?»

Se sì → ripeti il loop solo per quelle saltate.
Se no → vai alla verifica finale.

---

## Fase 4 — Verifica finale

```
inbox_summary { companyId }   ← verifica zero non letti
```

**Se zero:**
> «🏆 **Inbox Zero raggiunto!** Tutti i messaggi sono stati gestiti.»

**Se ancora ci sono non letti (es. nuovi arrivati nel frattempo):**
> «Attenzione: sono arrivati [N] nuovi messaggi. Vuoi gestirli adesso?»

---

## Formulazione risposte (Fase 1 Step B)

Quando l'utente vuole rispondere, Claude formula il testo seguendo questi criteri:

- **Tono**: professionale ma diretto, prima persona singolare
- **Lunghezza**: breve (2-4 righe max), a meno che il contesto non richieda dettagli
- **Lingua**: italiana, a meno che il messaggio originale non sia in un'altra lingua
- **Struttura**: conferma di aver letto → risposta alla domanda/richiesta → eventuale next step

Esempio:
> Utente: «digli che ci penso e gli faccio sapere entro venerdì»
> Claude propone: «Grazie per il messaggio. Ci sto lavorando e ti faccio sapere entro venerdì.»

---

## Gestione casi speciali

| Caso | Comportamento |
|------|--------------|
| Messaggio molto lungo | Riassumi in max 3 punti bullet |
| Messaggio in una lingua diversa da quella dell'utente | Sintetizza nella lingua dell'utente, rispondi nella lingua del mittente |
| Richiesta urgente nel messaggio | Evidenzia con ⚠️ nella sintesi |
| Conversazione con thread lungo | Leggi gli ultimi 3 messaggi per il contesto |
| Utente vuole rispondere a tutti nello stesso modo | «Vuoi usare la stessa risposta per tutti i messaggi simili?» |
| Più di 15 messaggi | Dopo ogni 5, chiedi «Vuoi una pausa o continuiamo?» |
| Menzione che chiede check-in su un'iniziativa | Non eseguire check-in da questa skill: usa `lh-check-in-zero` oppure guida l'utente al flusso MCP con `checkInOutcome` e `progressNote` obbligatoria |

---

## Anti-pattern

| ❌ Non fare | ✅ Fai invece |
|------------|--------------|
| Mostrare il testo grezzo del messaggio | Riassumi in 1-2 righe |
| Marcare come letto senza decisione utente | Aspetta sempre la scelta A/B/C |
| Scrivere risposte lunghissime | Max 4 righe, salvo contesto complesso |
| Chiedere «cosa vuoi fare?» senza opzioni | Proponi sempre A/B/C |
| Processare tutte le conversazioni in bulk | Una alla volta, sempre |
