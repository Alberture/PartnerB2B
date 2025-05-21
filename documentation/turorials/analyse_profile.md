# Faire une demande d'analyse d'un profil
Une fois un profil soumis vous pourrez faire la demande d'une analyse pour le profil validé à cet endpoint /api/v1/profiles/{profiles_id}/analyses/ avec un POST et obtiendrez un message de confirmation.

## Exemple avec Postman

![image](https://github.com/user-attachments/assets/385bf441-7f4b-400d-b998-908fb2b96395)

Détails des résultats :
```json
{
    "data": {
        "message": "Vous venez de faire une demande d'analyse pour le profile 437",
        "pk": 50,
        "status": "pending"
    },
    "meta": {
        "timestamp": "2025-05-20T21:34:28.459388",
        "request_id": "355afbf3-4a8f-40fa-8077-ce998e12b328"
    }
}
```

| First Header  | Second Header |
| ------------- | ------------- |
| message| Message de confirmation de demande d'analyse  |
| pk | Identifiant de l'analyse, celui-ci vous permettra de le retrouver  |
| status | L'étape à laquelle est l'analyse |
