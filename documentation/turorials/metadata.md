# Liste des attributs
Avant de créer des profils vous devez prendre connaissance des attributs disponible pour un profil. Ces derniers sont disponibles à cet endpoint /api/v1/metadata/ avec GET vous obtiendrez la liste de tous les attributs et les catégories auxquels ils appartiennent.

## Exemple avec postman

![image](https://github.com/user-attachments/assets/62163241-1f10-4c6d-9f97-c5fdbb960f6f)

Détails des résultats:
```json
{
    "data": {
        "family situation": [
            {
                "pk": 91,
                "name": "family_situation",
                "displayedName": "Situation familiale",
                "type": "choice",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "célibataire"
                    },
                    {
                        "displayedName": "marié_pacsé"
                    },
                    {
                        "displayedName": "séparé_divorcé"
                    }
                ],
                "regex": null,
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            }
        ],
        "documents": [
            {
                "pk": 100,
                "name": "bank_statement",
                "displayedName": "Relevé bancaire",
                "type": "file",
                "isRequired": false,
                "validation": null,
                "sensitiveData": true,
                "attributechoice_set": [],
                "regex": null,
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": "pdf"
            },
            {
                "pk": 101,
                "name": "proof_of_address",
                "displayedName": "Justificatif de domicile",
                "type": "file",
                "isRequired": false,
                "validation": null,
                "sensitiveData": true,
                "attributechoice_set": [],
                "regex": null,
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": "pdf"
            }
        ],
        ...
    },
    "meta": {
        "timestamp": "2025-05-20T13:27:25.746149",
        "request_id": "7ad6fbda-e35a-45d8-b983-fde90770b092"
    }
}
```

| Champ  | Description |
| ------------- | ------------- |
| data  | data va contenir des clef qui correspond aux catégories des attributs qui elles contiendront les attributs dans cette catégorie |
| pk  | identifiant de l'attribut  |
| name  | nom de l'attribut  |
| displayedName  | nom affiché de l'attribut  |
| type  | Type de l'attribut (integer, float, string, file, date, etc...)  |
| isRequired  | Permet de déterminer si cet attribut doit obligatoirement figurer à la création d'un profile  |
| validation  | Donne une indication sur les contraintes de validtion d'un attribut (voir Description des validation pour avoir plus de détails) |
| sensitiveData  | Indicateur de données sensibles  |
| attributechoice_set  | Certains attributs sont de type "choice", ainsi ces derniers possèdent des attribute choice dans ce tableau qui correspondent à un/des choix possible pour cet attribut  |
| sensitiveData  | Indicateur de données sensibles |

## Description des validation

| validation  | Description |
| ------------- | ------------- |
| regex  | La valeur qui va être associé à cet attribut devra match le regex mis en place pour cet attribut (champ regex) |
| unique choice  | Le choix réalisé pour cet attribut devra être unique parmis les choix disponibles  |
| multiple choice  | Le choix réalisé pour cet attribut peut être unique ou multiple parmis les choix disponibles |
| min/max value  | la taille de la chaine de l'attribut ne devra pas dépasser un certain seuil ni aller en dessous d'un minimum ( champs minValue et maxValue) |
| min/max length  | la valeur d'un entier ou décimal ne devra pas dépasser un certain seuil ni aller en dessous d'un minimum (champs minLength et maxLength) |
| min/max date  | la date de l'attribut ne devra pas dépasser une certaine date et être inférieure à une autre date (champs minDate et maxDate) |
