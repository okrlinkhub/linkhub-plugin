# Esempio dialogo Coach OKR — setup strategico (estratto)

## Apertura

**Coach:** Ciao! Definiamo la strategia OKR iniziale del team. Su quale **company** e **team** lavoriamo?

**Utente:** LinkHub, team Centro Unico Paziente.

**Coach:** *(mcp_membershipProfile → companies_list → teams_listMineByCompany)*
Hai accesso come leader. *(objectives_byTeam → vuoto)*
Il team non ha ancora Objectives. Quante priorità strategiche vuoi impostare oggi?

**Utente:** Tre: qualità assistenza, digitalizzazione pratiche, tempi di risposta.

---

## Intervista — Objective 1

**Coach:** Partiamo da **qualità assistenza**. Perché è prioritaria nei prossimi mesi?

**Utente:** Dobbiamo ridurre errori nelle pratiche e aumentare soddisfazione pazienti.

**Coach:** Come la misureremmo **oggi**? Hai un dato?

**Utente:** Abbiamo il tasso di pratiche corrette al primo invio, già in CRM.

**Coach:** Perfetto — KR **tipo A** misurabile oggi. Proponiamo:
- **Objective:** «Eccellenza nella gestione pratiche paziente»
- **KR:** `Pratiche corrette al primo invio (%)`
- **Peso:** 30% sul totale team. Questo KR dimostra già tutto l'outcome, oppure
  manca una dimensione essenziale?

**Utente:** Manca la soddisfazione dei pazienti, che misuriamo già con il CSAT.

**Coach:** È una dimensione distinta dell'outcome, quindi ha senso un secondo
KR: `Soddisfazione pazienti (CSAT)`, peso 20%. Ci fermiamo a due perché qualità
della pratica e percezione del paziente coprono già l'Objective. Confermi?

**Utente:** Sì. Per il primo forecast 92 e target 95; per il secondo forecast
4,2 e target 4,5.

**Coach:** Hai già entrambi gli indicatori in LinkHub? Mi servono gli
`indicatorId`.

**Utente:** Sì, ecco i due ID.

*(objectives_create → keyResults_create × 2 con weight 30 e 20)*

---

## Rischi — KR tipo A

**Coach:** Anche se i due KR sono già misurabili, definiamo almeno un rischio
per ciascuno. Cosa potrebbe impedire di raggiungere il 95% di pratiche corrette
e il CSAT 4,5?

**Utente:** I controlli avvengono troppo tardi e al questionario rispondono
soprattutto i pazienti già soddisfatti.

**Coach:** Sono due rischi ad alto impatto. Propongo:
1. sul KR pratiche, *«Errori intercettati soltanto dopo l'invio al paziente»*;
2. sul KR CSAT, *«Campione CSAT non rappresentativo dell'esperienza paziente»*.

Per il primo: *«Introdurre entro 30 giorni una checklist pre-invio sulle cinque
anomalie più frequenti»*. Per il secondo: *«Inviare entro 30 giorni il
questionario CSAT a tutti i pazienti entro 24 ore dalla chiusura pratica»*.
Confermi rischi e iniziative?

**Utente:** Confermo.

*(risks_create × 2 → initiatives_create × 2)*

---

## Intervista — Objective 2 (setup misurabilità)

**Coach:** Seconda priorità: **digitalizzazione pratiche**. Metrica disponibile?

**Utente:** No, stiamo ancora definendo cosa tracciare.

**Coach:** Allora KR **tipo B** — misuriamo il **progresso del setup**:
- **Objective:** «Digitalizzazione end-to-end delle pratiche»
- **KR:** `Completamento setup tracking digitalizzazione (%)`
- **Peso:** 30%
- Target 100% entro 30 giorni per avere la prima dashboard. Ti torna?

**Utente:** Sì.

**Coach:** Creo objective e KR. Per l'indicatore `% setup` devi crearlo in UI se non esiste — lo hai?

**Utente:** Appena creato, ecco l'ID.

*(objectives_create → keyResults_create weight 30)*

---

## Rischi — KR tipo B

**Coach:** Sul KR setup digitalizzazione, quali rischi vedi?

**Utente:** IT overloaded e dati sparsi in più tool.

**Coach:** Aggiungo:
1. *«Ritardo nel consolidamento delle fonti dati per la digitalizzazione»* (high)
2. *«Priorità IT insufficiente per completare l'integrazione entro 30 giorni»* (medium)

*(risks_create × 2)*

---

## Iniziative mensili

**Coach:** Per il rischio **fonti dati sparse**, un'azione completabile entro il mese?

**Utente:** Mappare tutte le fonti in un documento con owner.

**Coach:** Proposta iniziativa: *«Documentare entro 30 giorni mappa fonti dati pratiche con owner e frequenza aggiornamento»*. Chi la fa?

**Utente:** Io, con input da Marco (fuori team).

*(teams_listMembers → initiatives_create assignee=utente, checkInDays=30, assignmentCommentReceiverId=Marco)*

---

## Objective 3 + ribilanciamento

**Coach:** Terza priorità **tempi di risposta**. Hai SLA misurabile?

**Utente:** Non ancora — solo stime manuali.

**Coach:** KR tipo B: `Completamento setup SLA risposta ticket (%)`, peso **20%** → totale 100%. Rischi: *«Assenza di baseline SLA affidabile»*. Iniziativa: *«Configurare export giornaliero ticket con timestamp apertura/chiusura»* entro 30 giorni. Procedo?

**Utente:** Sì.

*(objectives_create → keyResults_create → risks_create → initiatives_create)*

---

## Double-check e chiusura

**Coach:** *(objectives_byTeam + keyResults_byTeam)*
Verifica:
- 3 Objectives, 4 KR, pesi **30 + 20 + 30 + 20 = 100%**
- ogni KR ha da 1 a 3 rischi espliciti
- 2 KR tipo B con rischio misurabilità + iniziativa mensile
- 2 KR tipo A con forecast/target confermati e iniziative sui rischi high

**Coach:** Ecco il riepilogo strategico. Al prossimo periodo di reporting usa il **Report Coach** per tracciare i risultati; per i check-in settimanali sulle iniziative usa **Check-in Zero**. Vuoi affinare qualche testo prima di chiudere?

**Utente:** No, grazie.

**Coach:** Strategia impostata. Focus prossimi 30 giorni: completare setup SLA e mappa fonti dati.
