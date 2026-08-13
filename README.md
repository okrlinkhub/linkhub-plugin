# LinkHub per ChatGPT e Codex

Questo repository distribuisce privatamente il plugin LinkHub ai clienti autorizzati. Il bundle è
raggiungibile tramite link, ma dati e operazioni restano protetti dall'accesso OAuth e dalle
autorizzazioni del singolo account LinkHub.

## Requisiti

- ChatGPT desktop aggiornato, con accesso a ChatGPT Work o Codex.
- Codex CLI disponibile nel terminale.
- Un account LinkHub attivo.

## Installazione

Sostituisci `<versione>` con il tag indicato da LinkHub, per esempio `v0.1.0`.

```bash
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref <versione>
codex plugin add linkhub@linkhub-private
```

Riavvia ChatGPT desktop, apri una nuova chat e seleziona LinkHub dalla directory dei plugin. Alla
prima connessione completa l'accesso OAuth con il tuo account LinkHub.

Puoi iniziare con uno di questi prompt:

- `Guidami nel report mensile del mio team.`
- `Spiegami l'andamento di un indicatore.`
- `Mostrami cosa richiede attenzione in LinkHub.`

## Aggiornamento

LinkHub pubblica ogni versione come tag immutabile. Per passare a un nuovo tag, sostituisci
`<nuova-versione>` con la versione comunicata:

```bash
codex plugin marketplace remove linkhub-private
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref <nuova-versione>
codex plugin add linkhub@linkhub-private
```

Dopo l'aggiornamento, usa una nuova chat per caricare skill e strumenti aggiornati.

## Disinstallazione

```bash
codex plugin remove linkhub
codex plugin marketplace remove linkhub-private
```

Per revocare anche l'accesso ai dati, scollega LinkHub dalle impostazioni delle app di ChatGPT e
dalle integrazioni del tuo account LinkHub.

Se l'installazione o la connessione non riesce, consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
