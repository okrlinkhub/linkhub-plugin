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
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref v0.6.2
codex plugin add linkhub@linkhub-private
```

Riavvia ChatGPT desktop, apri una nuova chat e seleziona LinkHub dalla directory dei plugin. Alla
prima connessione completa l'accesso OAuth con il tuo account LinkHub.

Puoi iniziare con uno di questi prompt:

- `Guidami nel report mensile del mio team.`
- `Guidami nella review di un report già sottomesso.`
- `Spiegami l'andamento di un indicatore.`
- `Mostrami cosa richiede attenzione in LinkHub.`

## Aggiornamento

LinkHub pubblica ogni versione come tag immutabile. Per passare a un nuovo tag, sostituisci
`v0.6.2` con la versione comunicata:

```bash
codex plugin marketplace remove linkhub-private
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref v0.6.2
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
