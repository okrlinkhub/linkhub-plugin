# LinkHub per ChatGPT e Codex

Questo repository è il mirror pubblico generato dalla sorgente canonica LinkHub. Non viene
modificato manualmente: ogni tag immutabile corrisponde a un deployment production verificato.
Dati e operazioni restano protetti dall'accesso OAuth e dalle autorizzazioni del singolo account.

## Requisiti

- ChatGPT desktop aggiornato, con accesso a ChatGPT Work o Codex.
- Codex CLI disponibile nel terminale.
- Un account LinkHub attivo.

## Installazione

Usa il tag stabile indicato qui sotto.

```bash
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref v0.10.27
codex plugin add linkhub@linkhub-private
```

Riavvia ChatGPT desktop, apri una nuova chat e seleziona LinkHub dalla directory dei plugin. Alla
prima connessione completa l'accesso OAuth con il tuo account LinkHub.

Puoi iniziare con uno di questi prompt:

- `Guidami nel report mensile del mio team.`
- `Guidami nella review di un report già sottomesso.`
- `Chiudiamo la giornata dalle Note delle mie iniziative.`
- `Facciamo il weeklyRecap della mia settimana.`
- `Spiegami l'andamento di un indicatore.`
- `Mostrami cosa richiede attenzione in LinkHub.`
- `Scegliamo le mie 3 iniziative in focus per oggi.`

## Focus quotidiano

- **`focus`** (`/focus`): legge il tuo #whoami e le proposte del giorno e ti aiuta a scegliere
  fino a 3 iniziative in focus, a sostituire quelle completate e, se hai collegato Outlook, a
  bloccare il tempo in calendario.
- **`filtro-impegni`**: quando una chat produce un tuo impegno, propone di tracciarlo come
  iniziativa collegata a un KR oppure, se non ha posto negli OKR, un no in panchina con il motivo.
- **`lh-check-in-zero`** ("chiudo la giornata"): a fine giornata prepara la bozza dei check-in
  dalle Note delle iniziative; tu confermi, sposti o chiudi ciascuno.
- **`lh-weekly-recap`**: a fine settimana rivede chiusure ed effetto sui KR, pulisce la panchina
  e prepara il testo da inoltrare.

Per attivare focus e filtro in ogni chat copia lo snippet di
[`skills/filtro-impegni/snippet-claude-md.md`](plugins/linkhub/skills/filtro-impegni/snippet-claude-md.md)
nel tuo `CLAUDE.md` o nelle istruzioni personalizzate: richiama `me_whoami` all'inizio di ogni
nuova chat e attiva il filtro.

## Aggiornamento

LinkHub pubblica ogni versione come tag immutabile. Per passare a un nuovo tag, sostituisci
`v0.10.27` con la versione comunicata:

```bash
codex plugin marketplace remove linkhub-private
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref v0.10.27
codex plugin add linkhub@linkhub-private
```

Dopo l'aggiornamento, usa una nuova chat per caricare skill e strumenti aggiornati.

## Skill standalone

Gli ZIP allegati alla GitHub Release sono un fallback per gli assistenti che non supportano il
plugin. Sono generati dalla stessa sorgente e riportano la stessa versione e gli stessi checksum;
non vanno mantenuti o modificati separatamente.

## Disinstallazione

```bash
codex plugin remove linkhub
codex plugin marketplace remove linkhub-private
```

Per revocare anche l'accesso ai dati, scollega LinkHub dalle impostazioni delle app di ChatGPT e
dalle integrazioni del tuo account LinkHub.

Se l'installazione o la connessione non riesce, consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
