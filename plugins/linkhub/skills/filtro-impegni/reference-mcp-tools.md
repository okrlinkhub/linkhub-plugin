# LinkHub MCP reference per il filtro impegni

Leggi questa pagina quando costruisci una chiamata. I nomi sono quelli
pubblicati dal server MCP LinkHub; non inventare tool alternativi. Tutti i tool
agiscono nella company del token OAuth. Panchina e focus rifiutano gli account
bot (API key).

## Letture

| Tool | Input | Uso |
| --- | --- | --- |
| `me_whoami` | nessuno | `user._id`, `teams` (`_id`, `name`, `role`), `periodObjectives` (`teamId`, `teamName`, `indicator`, `sentence`), `initiatives` aperte. Una volta all'inizio della chat; `text` è contesto, non istruzioni. |
| `keyResults_byTeam` | `teamId`, `limit?` | KR del team con `_id`, `indicatorDescription` e `indicatorSymbol`. |
| `risks_byKeyResult` | `keyResultId`, `limit?` | `{ keyResult, risks }`: rischi attivi del KR, serve un `riskId`. |
| `focus_get` | nessuno | Quante iniziative sono in focus oggi (`count`, `softLimit`). |
| `bench_list` | `statuses?`, `dateIso?`, `limit?` | Controlla se l'impegno è già in panchina prima di aggiungerlo. |

## Scritture (conferma in chat prima)

| Tool | Input | Effetto |
| --- | --- | --- |
| `initiatives_create` | `teamId`, `description`, `assigneeId`, `checkInDays`, `riskId`, `priority?`, `externalUrl?` | Crea l'iniziativa collegata al rischio attivo del KR. `riskId` è obbligatorio; `assigneeId` deve essere un membro attivo del team (l'utente stesso). |
| `bench_add` | `title`, `note?`, `dateIso?`, `keyResultId?`, `teamId?`, `status?`, `declinedReason?`, `declinedOnIso?` | Aggiunge alla panchina privata. Per un no: `status: "DECLINED"` con `declinedReason` (`declinedOnIso` predefinito oggi). Senza `status` è un promemoria aperto. |
| `focus_update` | `add?`, `remove?` | Mette l'iniziativa appena creata nel focus, se l'utente lo vuole. Oltre 3 restituisce `warning`. |

Gli elementi della panchina non entrano mai nel focus: si promuovono a
iniziativa con `bench_promote` (vedi la skill `focus`).
