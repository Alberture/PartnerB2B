# Création de profils
Pour créer un profile vous devez envoyer une requête POST à cet endpoints api/v1/profiles/ avec le corps de la requeête contenant une valeur "attributes" qui contient des clef valeur, les clef qui sont le nom des attributs et valeur leur valeur.

## Exemple avec postman

![image](https://github.com/user-attachments/assets/1746c0d5-e4ec-45d9-8d86-94ae7c7c055d)

Détails des résultats :
```json
{
    "data": {
        "pk": 452,
        "status": "draft",
        "createdAt": "2025-05-21T07:15:02.395271Z",
        "profileattribute_set": [
            {
                "attribute": {
                    "name": "firstname"
                },
                "value": "Jean"
            },
            {
                "attribute": {
                    "name": "lastname"
                },
                "value": "Dupond"
            },
            {
                "attribute": {
                    "name": "email"
                },
                "value": "exemple@gmail.com"
            },
            {
                "attribute": {
                    "name": "birth_date"
                },
                "value": "1999-01-01"
            },
            {
                "attribute": {
                    "name": "monthly_income"
                },
                "value": "0"
            },
            {
                "attribute": {
                    "name": "monthly_charges"
                },
                "value": "0"
            },
            {
                "attribute": {
                    "name": "phone_number"
                },
                "value": "+33123456789"
            },
            {
                "attribute": {
                    "name": "scholarship_student"
                },
                "value": "True"
            },
            {
                "attribute": {
                    "name": "professional_situation"
                },
                "value": "étudiant"
            },
            {
                "attribute": {
                    "name": "delivery_address1"
                },
                "value": "3 rue truc"
            },
            {
                "attribute": {
                    "name": "housing_situation"
                },
                "value": "autre situation d'habilitation"
            },
            {
                "attribute": {
                    "name": "other_housing_situation"
                },
                "value": "dans une grotte"
            }
        ]
    },
    "meta": {
        "timestamp": "2025-05-21T07:15:03.365949",
        "request_id": "6729fa15-13c1-43f4-a0da-bd050504f5ca"
    }
}
```

| Champ  | Description |
| ------------- | ------------- |
| pk | Identifiant du profil  |
| status  | Status de création/complétion du profil  |
| createdAt  | Date et heure de création du profil  |
| profileattribute_set  | Correspond à la liste des attributs qui ont été affectés à un profil ainsi que leur valeur associée |

