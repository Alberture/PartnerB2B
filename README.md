# PartnerB2B

## Objectifs de l'API
Cette API a pour objectif d'évaluer la fiabilité d'un client pour la réalisation de l'emprunt d'un bien ou un crédit, pour cela l'API va recevoir des données sur un client et retourner à la fin de l'analyse un score qui évaluera le facteur de confiance.

# Authentification

## Obtenir une clef API
Pour obtenir une clef API il faut faire une demande auprès de Alberture.

## JWT
JWT utilise un système d'access et refresh token. Un access token est un token permettant de vous authentifier et utiliser notre API, ce dernier ne dure que 1 heure.
Le refresh token intervient pour générer un autre access token et dure 1 semaine

Pour obtenir un access token il faut envoyer (POST) votre clef API à cet endpoint /api/v1/auth/token/ avec le corps de la requête en JSON et contenant 
```json
{
  "apiKey": VOTRE_CLEF_API
}
```
et obtiendrez une réponse resemblant à 
```json
{
    "data": {
        "access": VOTRE_ACCESS_TOKEN,
        "refresh": VOTRE_REFRESH_TOKEN",
        "access_expire": "2025-05-20T13:08:18",
        "refesh_expire": "2025-05-27T12:08:18"
    },
    "meta": {
        "timestamp": "2025-05-20T12:08:18.338840",
        "request_id": "84455385-e154-4908-94ff-05aa8560b5b8"
    }
}
```

Pour pouvoir refresh l'access token (c'est à dire renouveller l'access token si ce dernier a expiré) il suffit d'envoyer (POST) le refresh token à cet endpoint /api/v1/auth/token/refresh/ avec le corps 
de la requête en JSON et contenant 
```json
{
  "refresh": VOTRE_REFRESH_TOKEN
}
```
et obtiendrez une réponse resemblant à 
```json
{
    "data": {
        "access": VOTRE_NOUVEAU_ACCESS_TOKEN,
        "access_expires": "2025-05-20T13:34:27"
    },
    "meta": {
        "timestamp": "2025-05-20T12:34:27.372911",
        "request_id": "387b9e56-b55f-4223-8ba5-86f496154674"
    }
}
```

Si les 2 token venaient à expirer il faut de nouveau envoyer la clef API comme nous l'avons fait pour l'access token. A l'exception de ces 2 endpoints vous devrez être identifié pour avoir accès aux autres.

# Utilisation
## Liste des attributs
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

## Création de profils
Pour créer un profile vous devez envoyer une requête POST à cet endpoints api/v1/profiles/ avec le corps de la requeête contenant 
```json
{
    "attributes": {
      "NOM_ATTRIBUT": "VALEUR_ATTRIBUT",
      "NOM_ATTRIBUT": "VALEUR_ATTRIBUT",
      "NOM_ATTRIBUT": "VALEUR_ATTRIBUT",
      ...
    },
    "externalReference": "REFERENCE" #optional
}
```
vous obtiendrez le profil crée avec les details.
```json
{
    "data": {
        "pk": 446,
        "status": "draft",
        "createdAt": "2025-05-20T09:27:59.193674Z",
        "profileattribute_set": [
            {
                "attribute": {
                    "name": "NOM_ATTRIBUT"
                },
                "value": "VALEUR_ATTRIBUT"
            },
            {
                "attribute": {
                    "name": "NOM_ATTRIBUT"
                },
                "value": "VALEUR_ATTRIBUT"
            }
        ]
    },
    "meta": {
        "timestamp": "2025-05-20T09:28:00.064073",
        "request_id": "32f449be-62e9-4747-a7d4-16385e07fb8d"
    }
}
```
## Soumettre d'un profil
Vous pouvez soumettre un profil à cet endpoint /api/v1/profiles/{profiles_id}/submit/ avec un POST et obtiendrez un message de confirmation comme ci-dessous
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

## Faire une demande d'analyse d'un profil
Une fois un profil soumis vous pourrez faire la demande d'une analyse pour le profil validé à cet endpoint /api/v1/profiles/{profiles_id}/analyses/ avec un POST et obtiendrez un message de confirmation.
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

## Soumettre un document à un profile
Pour ajouter un document à un profile il faut à cet endpoint /api/v1/profiles/{profiles_id}/documents/ faire un POST avec le corps de la requête en form-data avec un champ "file" qui corresponse au fichier et "attribute" qui correspond à l'attribut.

## Configuration d'un webhook
Pour configurer un webhook il faut à cet endpoint /api/v1/webhooks/configure/ faire un POST avec le corps de la requête contenant 
```json
{
  "url": "VOTRE_URL"
}
```
Vous devrez obtenir un message de confirmation comme quoi ce dernier a été configuré.
