# Risoluzione dei problemi

## LinkHub non compare nella directory

1. Verifica che il marketplace sia presente con `codex plugin marketplace list`.
2. Reinstalla con `codex plugin add linkhub@linkhub-private`.
3. Riavvia ChatGPT desktop e apri una nuova chat.

## L'accesso OAuth non viene proposto

Il plugin standard usa direttamente il server MCP LinkHub. Se la tua versione di ChatGPT richiede
invece una connessione registrata:

1. In ChatGPT apri **Settings → Security and login** e abilita **Developer mode**.
2. Apri la directory dei plugin, premi **+** e registra l'URL MCP fornito da LinkHub.
3. Copia l'identificativo tecnico mostrato nell'URL della connessione.
4. Nella copia locale di questo repository esegui:

   ```bash
   node scripts/configure-chatgpt-connection.mjs <plugin_asdk_app... oppure asdk_app...>
   codex plugin marketplace add .
   codex plugin add linkhub@linkhub-private
   ```

La configurazione resta locale e non deve essere committata o condivisa.

## Accesso negato dopo il login

- Verifica che l'utente sia attivo in LinkHub e appartenga alla company richiesta.
- Ripeti il collegamento OAuth se l'account ChatGPT era connesso a un diverso utente LinkHub.
- Contatta il supporto LinkHub indicando l'ora del tentativo, senza inviare token o credenziali.

## Ripristinare una versione precedente

Rimuovi il marketplace e aggiungilo nuovamente indicando il tag precedente:

```bash
codex plugin marketplace remove linkhub-private
codex plugin marketplace add okrlinkhub/linkhub-plugin --ref <tag-precedente>
codex plugin add linkhub@linkhub-private
```
