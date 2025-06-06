# Soumettre un document à un profile
Pour ajouter un document à un profile il faut à cet endpoint /api/v1/profiles/{profiles_id}/documents/ faire un POST avec le corps de la requête en form-data avec un champ "file" qui corresponse au fichier et "attribute" qui correspond à l'attribut.
=======
# Soumettre d'un profil
Vous pouvez soumettre un fichier à cet endpoint /api/v1/profiles/{profiles_id}/documents/ avec un POST contenant votre fichier et le nom de l'attribut

## Exemple avec postman

![image](https://github.com/user-attachments/assets/938fb36f-8b39-4d5a-8740-8a2d600f8e1c)

Détails des résultats :
```json
{
    "data": {
        "pk": 41,
        "status": "pending",
        "downloadedAt": "2025-05-21T07:43:53.905907Z",
        "type": "pdf"
    },
    "meta": {
        "timestamp": "2025-05-21T07:43:53.952490",
        "request_id": "b6ea958a-3ae3-4910-b247-d8d58bb8d97a"
    }
}
```

| Champ  | Description |
| ------------- | ------------- |
| pk  | Identifiant du document, il vous permettra de retrouver le document  |
| status  | Status de validation du document  |
| downloadedAt  | Date d'envoie du document  |
| type  | type de fichier  |


Automatiquement pour un attribut dans la catégorie "document" on procédera à la vérification de taille maximale et les formats acceptés (informations visibles dans les metadata).
