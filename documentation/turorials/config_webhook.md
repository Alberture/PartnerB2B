# Configuration d'un webhook
Pour configurer un webhook il faut à cet endpoint /api/v1/webhooks/configure/ faire un POST avec le corps de la requête un champ "url" correspondant au webhook que vous souhaitez configurer.

## Exemple avec postman

![image](https://github.com/user-attachments/assets/dc481404-b597-4333-9782-de4fddaf9662)

Détails des résultats :
```json
{
    "data": {
        "message": "Votre url a bien été configurée."
    },
    "meta": {
        "timestamp": "2025-05-21T07:09:55.644447",
        "request_id": "ac35d3b6-60d8-4cf0-ac60-01ef5d8187f1"
    }
}
```

| Champ  | Description |
| ------------- | ------------- |
| message  | message de confirmation  |
