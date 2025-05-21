# Liste des attributs
Avant de créer des profils vous devez prendre connaissance des attributs disponible pour un profil. Ces derniers sont disponibles à cet endpoint /api/v1/metadata/ avec GET vous obtiendrez la liste de tous les attributs et les catégories auxquels ils appartiennent.
  
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
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
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
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
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
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
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