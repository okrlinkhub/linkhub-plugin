# Contratto degli output Strategy Canvas

Il renderer accetta UTF-8 JSON con questa forma. I riferimenti sono leggibili e
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

## Invarianti

- `schemaVersion` è esattamente `linkhub-strategy-canvas/v1`.
- `keyResults` contiene 1–3 elementi, con riferimenti univoci e un solo
  `isLead: true`.
- Ogni KR contiene indicatore, unità, target numerico e data ISO `YYYY-MM-DD`.
- `risks` contiene esattamente tre elementi e ogni `keyResultRef` coincide con
  il riferimento del KR guida.
- `kpi` è `null` oppure contiene indicatore, unità, soglia numerica e direzione
  `at_or_below` / `at_or_above`.
- Ogni rischio contiene 1–3 iniziative con riferimenti univoci.

## Markdown

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
