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

## 1. Perimetro e strategia comune

1. **Prima domanda obbligatoria: quale modalità si usa, coach admin in workshop oppure Cluster Leader in analisi individuale?** Dopo la scelta identifica company e Cluster scelto con `mcp_membershipProfile`, `companies_list` e `workshops_discoverCluster`. Verifica identità OAuth e `role` per il coach, oppure `isClusterLeader: true` per la modalità individuale; se il chiamante ha entrambi i ruoli, la scelta esplicita determina il flusso. Distingui i team attivi appartenenti al Cluster dal `clusterLeaderTeam`, che può avere un altro `clusterId`. Se il leader manca o `completeness.potentiallyTruncated` è vero, esplicita l'incompletezza e ferma le conclusioni e le scritture basate sull'inventario.
2. **Solo nella modalità coach:** chiedi quali team sono presenti. Mantieni un elenco presente/assente; i team assenti sono facoltativi. Ogni team presente deve avere una collaborazione verticale pertinente verificata prima di dichiarare completo il workshop. Il consenso collettivo alle modifiche mostrate autorizza quel gruppo di scritture. **Nella modalità Cluster Leader:** lavora da solo sull'intero Cluster, senza scelta dei presenti né obbligo di copertura universale; chiedi conferma al Cluster Leader per le modifiche leggibili.
3. Leggi Objectives e KR del team Cluster Leader e dei team rilevanti con `objectives_byTeam` e `keyResults_byTeam`. Leggi tutte le pagine di `workshops_listCollaborations` fino a `isDone`, senza saltare cursori o scambiare una pagina vuota filtrata per fine elenco. Presenta strategia, indicatori condivisi, collaborazioni verticali/orizzontali già attive e lacune. Ripeti la lettura dopo ogni modifica a KR o KPI: le collaborazioni sono **derivate dall'uso dello stesso indicatore**, non record da creare direttamente.

## 2. Proposta con il Cluster Leader e i team

Valuta miglioramenti della strategia esistente e raggruppa i KR del team Cluster Leader in aree tematiche leggibili. Nella modalità coach trova per ogni team presente almeno una collaborazione verticale pertinente fra un suo KR/KPI e un KR del team Cluster Leader. Nella modalità Cluster Leader analizza e correggi le relazioni che sceglie di trattare, anche se nessun altro è presente. Verifica l'indicatore con `indicators_search`/`indicators_resolve`; non inventare ID, valori, fonti o target. Per ogni relazione valuta esplicitamente:

- se serve nel team Cluster Leader un rischio concreto che usi quell'indicatore come KPI;
- se nel team del Cluster serve creare o modificare un KR collegato allo stesso indicatore;
- se la relazione esistente è già corretta e va solo verificata.

Proponi collaborazioni orizzontali fra due team del Cluster solo quando un rischio concreto giustifica un KPI condiviso. Non creare una relazione cosmetica per raggiungere la copertura. Nella modalità coach, se per un team presente manca una relazione sensata, registra il problema, il motivo e il team interessato; non dichiarare completato il workshop.

Applica i vincoli di `linkhub-strategy-coach`: Objectives qualitativi, 1–3 KR per Objective solo quando misurano dimensioni necessarie, nomi KR come metrica con unità, indicatori misurabili o piano esplicito per renderli misurabili, rischio di assenza dati quando rilevante, iniziative concrete e completabili in circa 30 giorni. Pesi coerenti e somma al 100%; nessun risultato o target inventato. Per un indicatore già usato, verifica la famiglia d'uso ammessa per ciascun team; non creare un conflitto KR/KPI nello stesso team.

## 3. Conferma, scrittura e verifica

Mostra una proposta per team e area: indicatore, relazione verticale/orizzontale, Objective/KR/rischio da creare o modificare, pesi prima/dopo, valori fondati su evidenze, iniziative e conseguenze. Chiedi consenso collettivo nella modalità coach o conferma del Cluster Leader nella modalità individuale. Solo dopo usa gli strumenti OKR esistenti (`objectives_create`/`objectives_update`, `keyResults_create`/`keyResults_update`, `risks_create`/`risks_update`, `initiatives_create`), nell'ordine richiesto dalle dipendenze. Rileggi Objectives, KR e tutte le pagine di collaborazioni dopo le scritture. Una mutation riuscita da sola non prova che la collaborazione sia attiva.

Concludi con una matrice delle relazioni esaminate: team, area, indicatore, relazione verticale verificata, eventuale relazione orizzontale e questioni aperte. Nella modalità coach dichiara completo il workshop solo se ogni team presente ha almeno una collaborazione verticale pertinente verificata e gli inventari sono completi; gli assenti sono follow-up facoltativi. Nella modalità Cluster Leader comunica quali relazioni sono state verificate o corrette e quali restano aperte, senza imporre una copertura di tutti i team.
