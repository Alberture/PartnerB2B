# Soumettre d'un profil
Vous pouvez soumettre un profil à cet endpoint /api/v1/profiles/{profiles_id}/submit/ avec un POST et obtiendrez un message.

## Exemple avec postman

![image](https://github.com/user-attachments/assets/63b417cd-6999-4bc0-8a0e-c908c717339f)

Détails des résultats :
```json
{
    "data": {
        "status": "Complet",
        "message": "Ce profil est complet et prêt pour analyse."
    },
    "meta": {
        "timestamp": "2025-05-20T21:32:56.215846",
        "request_id": "3bbbf338-e6d2-43ec-95de-e73e8a844af0"
    }
}
```

| Champ  | Description |
| ------------- | ------------- |
| status  | Status de l'analyse  |
| message  | Message de confirmation  |
