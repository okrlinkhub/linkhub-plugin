---
name: cluster-collaboration
description: >-
  Analizza e modifica le collaborazioni di un Cluster LinkHub con il Cluster
  Leader da solo, oppure facilita un workshop con coach admin company OAuth e
  team presenti. Usa quando si scelgono un Cluster e i suoi indicatori condivisi,
  KR e KPI; nella modalità coach serve coprire ogni team presente.
  Per la strategia iniziale di un singolo team usa linkhub-strategy-coach;
  per i report del Cluster usa coach-cluster-report.
---

# Collaborazioni del Cluster

Rispondi nella lingua dell'utente o del gruppo. Nessuna persona viene impersonata. Leggi prima di scrivere e presenta sempre modifiche comprensibili, effetti e team interessati. Se il consenso è negato, conserva lo stato e riproponi solo dopo una decisione nuova.

All'avvio fai **un solo `tool_search`** con tutti i nomi degli strumenti necessari al percorso scelto: `mcp_membershipProfile`, `companies_list`, `workshops_discoverCluster`, `workshops_listCollaborations`, `objectives_byTeam`, `keyResults_byTeam`, `indicators_search`, `indicators_resolve` e gli strumenti OKR di lettura/scrittura pertinenti, inclusi `risks_byKeyResult`, `risks_create`, `risks_update`, `risks_remove` e `initiatives_byTeam` quando servono. Includi `reviews_listMyClusterTargets` solo se il lavoro comprende anche l'individuazione dei target di review: se fallisce una volta, non riprovare; usa `workshops_discoverCluster` per l'inventario del Cluster e segnala separatamente i target di review non verificati. Non spezzare la ricerca in chiamate successive per gli stessi nomi.

## 1. Perimetro e strategia comune

1. **Prima domanda obbligatoria: quale modalità si usa, coach admin in workshop oppure Cluster Leader in analisi individuale?** Dopo la scelta identifica company e Cluster scelto con `mcp_membershipProfile`, `companies_list` e `workshops_discoverCluster`. Verifica identità OAuth e `role` per il coach, oppure `isClusterLeader: true` per la modalità individuale; se il chiamante ha entrambi i ruoli, la scelta esplicita determina il flusso. Distingui i team attivi appartenenti al Cluster dal `clusterLeaderTeam`, che può avere un altro `clusterId`. Se il leader manca o `completeness.potentiallyTruncated` è vero, esplicita l'incompletezza e ferma le conclusioni e le scritture basate sull'inventario.
2. **Solo nella modalità coach:** chiedi quali team sono presenti. Mantieni un elenco presente/assente; i team assenti sono facoltativi. Ogni team presente deve avere una collaborazione verticale pertinente verificata prima di dichiarare completo il workshop. Il consenso collettivo alle modifiche mostrate autorizza quel gruppo di scritture. **Nella modalità Cluster Leader:** lavora da solo sull'intero Cluster, senza scelta dei presenti né obbligo di copertura universale; chiedi conferma al Cluster Leader per le modifiche leggibili.
3. Leggi Objectives e KR del team Cluster Leader e dei team rilevanti con `objectives_byTeam` e `keyResults_byTeam`. Per i forecast citati all'utente usa i valori correnti di `keyResults_byTeam`, mai `forecastValue` di `workshops_listCollaborations`. All'inizio leggi **una volta tutte le pagine** di `workshops_listCollaborations` fino a `isDone`; una pagina vuota non conclude l'elenco. Conserva i cursori di ingresso per la pagina 0 e per ciascun team, associandoli all'ordine restituito da `workshops_discoverCluster` (team leader all'indice 0, poi i team del Cluster). Presenta strategia, indicatori condivisi, collaborazioni verticali/orizzontali già attive e lacune. Le collaborazioni sono **derivate dall'uso dello stesso indicatore**, non record da creare direttamente.

## 2. Proposta con il Cluster Leader e i team

Valuta miglioramenti della strategia esistente e raggruppa i KR del team Cluster Leader in aree tematiche leggibili. Nella modalità coach trova per ogni team presente almeno una collaborazione verticale pertinente fra un suo KR/KPI e un KR del team Cluster Leader. Nella modalità Cluster Leader analizza e correggi le relazioni che sceglie di trattare, anche se nessun altro è presente. Verifica l'indicatore con `indicators_search`/`indicators_resolve`; un indicatore già usato in una relazione orizzontale resta un candidato valido, se la nuova relazione è pertinente e la famiglia d'uso è ammessa. Non inventare ID, valori, fonti o target. Usa `risks_byKeyResult` soltanto sui KR delle relazioni in esame e `initiatives_byTeam` con `riskId` quando serve il contesto di un rischio. Non chiamare `teams_listByCompany` per ricostruire un Cluster già restituito da `workshops_discoverCluster`. Per ogni relazione valuta esplicitamente:

- se serve nel team Cluster Leader un rischio concreto che usi quell'indicatore come KPI;
- se nel team del Cluster serve creare o modificare un KR collegato allo stesso indicatore;
- se la relazione esistente è già corretta e va solo verificata.

Proponi collaborazioni orizzontali fra due team del Cluster solo quando un rischio concreto giustifica un KPI condiviso. Per ogni nuova relazione che richiede un rischio, proponi un **rischio nuovo e specifico** (per esempio PrimoUP, HubSpot, servizi mappati o migrazione nel rispettivo contesto), non un rischio generico riusato fra relazioni. Non creare una relazione cosmetica per raggiungere la copertura. Nella modalità coach, se per un team presente manca una relazione sensata, registra il problema, il motivo e il team interessato; non dichiarare completato il workshop.

Applica i vincoli di `linkhub-strategy-coach`: Objectives qualitativi, 1–3 KR per Objective solo quando misurano dimensioni necessarie, nomi KR come metrica con unità, indicatori misurabili o piano esplicito per renderli misurabili, rischio di assenza dati quando rilevante, iniziative concrete e completabili in circa 30 giorni. Pesi coerenti e somma al 100%; nessun risultato o target inventato. Per un indicatore già usato, verifica la famiglia d'uso ammessa per ciascun team; non creare un conflitto KR/KPI nello stesso team.

## 3. Conferma, scrittura e verifica

Mostra **un solo piano per l'intero Cluster**, organizzato per team e area: indicatore, relazione verticale/orizzontale, Objective/KR/rischio da creare o modificare, pesi prima/dopo, valori fondati su evidenze, iniziative e conseguenze. Distingui esplicitamente **«scollego l'indicatore dal rischio»** da **«elimino il rischio»**. Se la priorità dei rischi nuovi non è già definita, fai **una sola domanda** sulla priorità di default per tutti i rischi nuovi e segnala eventuali eccezioni nel piano. Chiedi un unico consenso collettivo al piano nella modalità coach o un'unica conferma del Cluster Leader nella modalità individuale; torna a chiedere conferma solo per cambiamenti materiali emersi dopo.

Solo dopo usa gli strumenti OKR esistenti (`objectives_create`/`objectives_update`, `keyResults_create`/`keyResults_update`, `risks_create`/`risks_update`, `initiatives_create`), nell'ordine richiesto dalle dipendenze. **«Togliere un KPI» da un rischio significa `risks_update` con `indicatorId: null`**, preservando il rischio e le sue iniziative. Usa `risks_remove` solo se l'utente chiede esplicitamente di eliminare l'intero rischio e lo conferma nel piano: prima della rimozione salva nel contesto della sessione uno snapshot del rischio con ID, KR, priorità, descrizione, indicatore e tutte le iniziative collegate, comprese le concluse (`initiatives_byTeam` con `riskId` e `includeFinished: true`, seguendo `nextCursor` fino a `hasMore: false`). Se lo snapshot è incompleto, non rimuovere il rischio.

Dopo ciascun gruppo di scritture, rileggi i KR/Objective modificati e **solo la pagina 0 e le pagine dei team toccati**, usando i cursori di ingresso salvati; per un team con più pagine continua fino alla pagina del team successivo. Se l'ordine o i cursori non sono più affidabili, aggiorna la scoperta e l'inventario completo prima di concludere. Alla fine della sessione rileggi **una volta tutte le pagine** di `workshops_listCollaborations` fino a `isDone`. Una mutation riuscita da sola non prova che la collaborazione sia attiva. Se una relazione attesa non compare dopo la scrittura, segnala la verifica come incompleta, non dichiararla completata e chiedi un test nell'interfaccia LinkHub.

Concludi con una matrice delle relazioni esaminate: team, area, indicatore, relazione verticale verificata, eventuale relazione orizzontale e questioni aperte. Nella modalità coach dichiara completo il workshop solo se ogni team presente ha almeno una collaborazione verticale pertinente verificata e gli inventari sono completi; gli assenti sono follow-up facoltativi. Nella modalità Cluster Leader comunica quali relazioni sono state verificate o corrette e quali restano aperte, senza imporre una copertura di tutti i team.
