guida_errori = {
    "404": {
        "titolo": "Pagina Non Trovata",
        "causa": "L'URL puntato non esiste più sul server o è stato rinominato",
        "azione": "1. Verifica se l'url nel file .env(O nella scheda di configurazione) è corretto.\n2. Controlla se la pagina è stata rimossa dal cms.\n3. Imposta un Redirect 301 se la pagina ha un nuovo indirizzo"
    },
    "500": {
        "titolo": "Errore interno del server",
        "causa": "Il server ha riscontrato una condizione imprevista.",
        "azione": "1. Controlla i log di errore del server\n2. Verifica eventuali plugin/moduli aggiornati di recente.\n3. Controlla se il database è raggiungibile"
    },
    "SSL_LOW":{
        "titolo": "Certificato in Scadenza",
        "cause": "Il certificato SSL tra meno di 10 giorni",
        "azione": "1. Accedi al provider(es. Let's Encrypt/Cloudflare).\n2. Forza il rinnovo manuale.\n3. Verifica che l'autorinnovamento(cronjob) sia attivo"
    }
}