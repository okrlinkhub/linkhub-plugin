# Contratto degli output Strategy Canvas

Leggi questo contratto prima di iniziare. Se la skill è incorporata in una pagina,
questa sezione deve essere presente integralmente, non solo nominata o linkata.

## Modalità completa

Il renderer accetta UTF-8 JSON con questa forma nella modalità completa. I riferimenti sono leggibili e
stabili nell'artefatto; non sono ID LinkHub.

```json
{
  "schemaVersion": "linkhub-strategy-canvas/v1",
  "teamName": "Customer Success",
  "objective": "Clienti autonomi e soddisfatti nel primo mese",
  "keyResults": [
    {
      "ref": "KR1",
      "indicatorName": "Clienti attivi dopo 30 giorni",
      "unit": "%",
      "targetValue": 85,
      "dueDate": "2026-12-31",
      "isLead": true
    }
  ],
  "risks": [
    {
      "ref": "R1",
      "keyResultRef": "KR1",
      "description": "I clienti non completano la configurazione iniziale",
      "kpi": {
        "indicatorName": "Configurazioni completate entro 7 giorni",
        "unit": "%",
        "triggerDirection": "at_or_below",
        "triggerValue": 60
      },
      "initiatives": [
        {
          "ref": "I1.1",
          "description": "Creare una checklist guidata per la configurazione"
        }
      ]
    },
    {
      "ref": "R2",
      "keyResultRef": "KR1",
      "description": "Il team non intercetta tempestivamente i clienti bloccati",
      "kpi": null,
      "initiatives": [
        {
          "ref": "I2.1",
          "description": "Contattare ogni giorno i clienti senza primo accesso"
        }
      ]
    },
    {
      "ref": "R3",
      "keyResultRef": "KR1",
      "description": "I contenuti di supporto non risolvono i dubbi ricorrenti",
      "kpi": null,
      "initiatives": [
        {
          "ref": "I3.1",
          "description": "Aggiornare ogni settimana le guide dai ticket ricorrenti"
        }
      ]
    }
  ]
}
```

## Invarianti della completa

- `schemaVersion` è esattamente `linkhub-strategy-canvas/v1`.
- `keyResults` contiene 1–3 elementi, con riferimenti univoci e un solo
  `isLead: true`.
- Ogni KR contiene indicatore, unità, target numerico finito e data futura ISO
  `YYYY-MM-DD`.
- `risks` contiene esattamente tre elementi e ogni `keyResultRef` coincide con
  il riferimento del KR guida.
- `kpi` è `null` oppure contiene indicatore, unità, soglia numerica e direzione
  `at_or_below` / `at_or_above`.
- Ogni rischio contiene 1–3 iniziative con riferimenti univoci.

## Markdown della completa

Il Markdown generato contiene:

1. riepilogo leggibile del team e dell'Objective;
2. tabella dei KR, con il KR guida riconoscibile;
3. tre sezioni rischio con KPI e iniziative;
4. nota di handoff sulla selezione/creazione degli indicatori in LinkHub;
5. un unico blocco fenced JSON etichettato `linkhub-strategy-canvas`, che è la
   rappresentazione canonica da passare a un'altra sessione.

Il Markdown non contiene `indicatorId`, `teamId` o affermazioni che i record
siano già stati creati. Pesi dei KR, priorità dei rischi, assignee e cadenze
delle iniziative sono intenzionalmente demandati alla successiva sessione MCP,
che li decide contro lo stato reale del team.

Un nuovo export può sovrascrivere i file esistenti soltanto se il blocco JSON
canonico appartiene allo stesso `teamName`. Se due nomi distinti producono lo
stesso `team-slug`, il renderer blocca l'export e chiede di disambiguare il nome
del team; non rinomina automaticamente gli artefatti.


## Modalità rapida

Usa un contratto distinto, senza adattare o indebolire il formato completo:
`schemaVersion: "linkhub-strategy-canvas/quick-v1"`. Il renderer riconosce la
modalità dalla versione dello schema, non dal numero di rischi. Tutti i valori
seguenti sono esempi ipotetici e non dati da attribuire al partecipante.

```json
{
  "schemaVersion": "linkhub-strategy-canvas/quick-v1",
  "canvasTitle": "Clienti autonomi nel primo mese",
  "objective": "Clienti autonomi e soddisfatti nel primo mese",
  "keyResults": [
    {
      "ref": "KR1",
      "indicatorName": "Clienti attivi dopo 30 giorni",
      "unit": "%",
      "targetValue": 85,
      "dueDate": "2026-12-31",
      "isLead": true
    }
  ],
  "risks": [
    {
      "ref": "R1",
      "keyResultRef": "KR1",
      "description": "I clienti non completano la configurazione iniziale",
      "kpi": {
        "indicatorName": "Configurazioni completate entro 7 giorni",
        "unit": "%"
      },
      "initiatives": [
        {
          "ref": "I1.1",
          "description": "Creare una checklist guidata per la configurazione"
        }
      ]
    },
    {
      "ref": "R2",
      "keyResultRef": "KR1",
      "description": "I clienti bloccati non ricevono supporto tempestivo",
      "kpi": {
        "indicatorName": "Tempo alla prima risposta di supporto",
        "unit": "ore"
      },
      "initiatives": [
        {
          "ref": "I2.1",
          "description": "Organizzare un turno quotidiano di supporto ai nuovi clienti"
        }
      ]
    }
  ]
}
```

### Invarianti della rapida

- `canvasTitle` deriva dall'Objective condiviso; non creare un team immaginario.
- Un Objective qualitativo, con il perché chiarito nella conversazione.
- Esattamente un KR con `isLead: true`, indicatore, unità, target numerico finito
  confermato e data futura valida in formato `YYYY-MM-DD`.
- Esattamente due rischi distinti, entrambi riferiti al KR guida.
- Un KPI obbligatorio per ciascun rischio: solo `indicatorName` e `unit`,
  senza `triggerDirection`, `triggerValue`, target o scadenza. Non usare `null`
  per dichiarare completo un rapido. Una bozza senza segnale resta incompleta.
- Esattamente una iniziativa concreta e confermata per ciascun rischio,
  con riferimento univoco e testo all'infinito.
- La verifica semantica e la conferma finale appartengono al coach: il renderer
  verifica la struttura, non prova che la conversazione abbia rispettato il metodo.

### Consegna e renderer

Il renderer genera PDF e Markdown per entrambe le modalità. Nella rapida mostra
all'utente soltanto il PDF salvo richiesta del Markdown; JSON e Markdown possono
restare file di lavoro. Il PDF rapido è A4 orizzontale di una pagina, con Objective,
KR completo, due colonne di rischi con rispettivi KPI e iniziative. I KPI riportano
solo nome e unità e una nota chiarisce che le soglie sono fuori dall'esercizio.

Il Markdown rapido contiene un solo blocco `json linkhub-strategy-canvas`,
riconoscibile dal `schemaVersion` rapido. **Non è un handoff creation-ready** per
LinkHub: prima occorre completare il Canvas secondo il contratto completo.
Non passarlo a strumenti che accettano soltanto `linkhub-strategy-canvas/v1`.

I nomi rapidi sono `<title-slug>-strategy-canvas-quick.md` e
`<title-slug>-strategy-canvas-quick.pdf`; la completa mantiene
`<team-slug>-strategy-canvas.md` e `<team-slug>-strategy-canvas.pdf`.
I due formati non si sovrascrivono. Il rapido può sovrascrivere un export solo
quando l'unico blocco canonico esistente ha lo stesso `canvasTitle`; collisioni
tra titoli distinti o Markdown ambiguo bloccano l'export.

Quando lo script non è disponibile nell'ambiente del partecipante, genera il PDF
con uno strumento disponibile rispettando il contratto scelto e la conferma.
Verifica file scaricabile, una pagina, contenuto fedele e nessun clipping. Se
l'ambiente non crea file, dichiara il limite e fornisci un layout da stampare.
Non presentare un testo o un link non funzionante come PDF generato.
