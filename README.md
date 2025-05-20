# PartnerB2B

## Objectifs de l'API
Cette API a pour objectif de soumettre des données concernant les clients de partenaires
souhaitant évaluer la confiance d'un client pour réaliser un emprunt (immobilier , crédit, etc....)

# Authentification

## Obtenir une clef API
Pour obtenir une clef API il faut faire une demande auprès de Aberture.

## JWT
JWT utiliser un système d'access et refresh token. Un access token est un token permettant 
de vous authentifier et utiliser notre API et ne dure que 1 heure.
Le refresh token intervient pour générer un autre access token et dure 1 semaine

Pour obtenir un access token il faut envoyer (POST) votre clef API à cet endpoint /api/v1/auth/token/ avec le corps 
de la requête en JSON et contenant 
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

Pour pouvoir refresh l'access token il suffit d'envoyer (POST) le refresh token à cet endpoint /api/v1/auth/token/refresh/ avec le corps 
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

Si les 2 token venaient à expirer il faut de nouveau envoyer la clef API comme nous l'avons fait pour l'access token.
A l'exception de ces 2 endpoints vous devrez être identifié pour avoir accès aux autres.

# Utilisation
## Liste des attributs
Avant de créer des profils vous devez prendre connaissance des attributs disponible pour un profil.
Ces derniers sont disponibles à cet endpoint /api/v1/metadata/ avec GET
vous obtiendrez la liste de tous les attributs et les catégories auxquels ils appartiennent.

<div style="height: 300px; overflow: auto;">
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
        "address": [
            {
                "pk": 79,
                "name": "billing_address1",
                "displayedName": "Adresse de facturation 1",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 80,
                "name": "billing_address2",
                "displayedName": "Adresse de facturation 2",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 81,
                "name": "billing_zip_code",
                "displayedName": "Code postal de facturation",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 82,
                "name": "billing_town",
                "displayedName": "Ville de facturation",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 83,
                "name": "billing_country",
                "displayedName": "Pays de facturation",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 84,
                "name": "delivery_address1",
                "displayedName": "Adresse de livraison1",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 85,
                "name": "delivery_address2",
                "displayedName": "Adresse de livraison2",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 86,
                "name": "delivery_zip_code",
                "displayedName": "Code postal de livraison",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 87,
                "name": "delivery_town",
                "displayedName": "Ville de livraison",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 88,
                "name": "delivery_country",
                "displayedName": "Pays de livraison",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [],
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
        "diverse": [
            {
                "pk": 97,
                "name": "scholarship_student",
                "displayedName": "étudiant boursier",
                "type": "boolean",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 98,
                "name": "years_in_current_job",
                "displayedName": "Années de poste actuel",
                "type": "integer",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 99,
                "name": "means_of_movement",
                "displayedName": "Moyen de déplacement",
                "type": "choice",
                "isRequired": false,
                "validation": "multiple choice",
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "marche"
                    },
                    {
                        "displayedName": "vélo"
                    },
                    {
                        "displayedName": "auto"
                    },
                    {
                        "displayedName": "moto"
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
        "housing situation": [
            {
                "pk": 89,
                "name": "housing_situation",
                "displayedName": "Situation de logement",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "locataire"
                    },
                    {
                        "displayedName": "colocataire"
                    },
                    {
                        "displayedName": "propriétaire"
                    },
                    {
                        "displayedName": "accédant_propriété"
                    },
                    {
                        "displayedName": "hébergé_gratuit"
                    },
                    {
                        "displayedName": "autre situation d'habilitation"
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
            },
            {
                "pk": 90,
                "name": "other_housing_situation",
                "displayedName": "Situation de logement autre",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
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
        "professional situation": [
            {
                "pk": 93,
                "name": "professional_situation",
                "displayedName": "Situation professionnelle",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "étudiant"
                    },
                    {
                        "displayedName": "cadre"
                    },
                    {
                        "displayedName": "entrepreneur_chef_entreprise"
                    },
                    {
                        "displayedName": "indépendant_libéral"
                    },
                    {
                        "displayedName": "fonction_publique"
                    },
                    {
                        "displayedName": "salarié"
                    },
                    {
                        "displayedName": "recherche_emploi"
                    },
                    {
                        "displayedName": "autre situation professionnelle"
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
        "children": [
            {
                "pk": 92,
                "name": "children_number",
                "displayedName": "Nombre d'enfants",
                "type": "integer",
                "isRequired": false,
                "validation": "min/max value",
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": 0.0,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            }
        ],
        "identity document": [
            {
                "pk": 77,
                "name": "identity_document_type",
                "displayedName": "Type de pièce d'identité",
                "type": "choice",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "CI"
                    },
                    {
                        "displayedName": "passeport"
                    },
                    {
                        "displayedName": "carte_sejour"
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
            },
            {
                "pk": 78,
                "name": "identity_document_number",
                "displayedName": "Numéro de pièce d'identité",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
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
        "personal data": [
            {
                "pk": 69,
                "name": "lastname",
                "displayedName": "Nom",
                "type": "string",
                "isRequired": true,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 70,
                "name": "firstname",
                "displayedName": "Prénom",
                "type": "string",
                "isRequired": true,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 71,
                "name": "gender",
                "displayedName": "Genre",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "M"
                    },
                    {
                        "displayedName": "F"
                    },
                    {
                        "displayedName": "autre genre"
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
            },
            {
                "pk": 72,
                "name": "email",
                "displayedName": "Email",
                "type": "string",
                "isRequired": true,
                "validation": "regex",
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 74,
                "name": "birth_date",
                "displayedName": "Date de naissance",
                "type": "date",
                "isRequired": true,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 75,
                "name": "birth_country",
                "displayedName": "Pays de naissance",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 76,
                "name": "birth_town",
                "displayedName": "Ville de naissance",
                "type": "string",
                "isRequired": false,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 73,
                "name": "phone_number",
                "displayedName": "Numéro de téléphone",
                "type": "string",
                "isRequired": true,
                "validation": "regex",
                "sensitiveData": false,
                "attributechoice_set": [],
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
        "product usage": [
            {
                "pk": 94,
                "name": "product_usage",
                "displayedName": "Usage du produit",
                "type": "choice",
                "isRequired": false,
                "validation": "unique choice",
                "sensitiveData": false,
                "attributechoice_set": [
                    {
                        "displayedName": "études"
                    },
                    {
                        "displayedName": "loisir"
                    },
                    {
                        "displayedName": "professionnel"
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
        "income and expenses": [
            {
                "pk": 95,
                "name": "monthly_income",
                "displayedName": "Revenu mensuel",
                "type": "integer",
                "isRequired": true,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
                "maxLength": 0,
                "minLength": 0,
                "maxValue": 9.223372036854776e+18,
                "minValue": -9.223372036854776e+18,
                "isEqualTo": null,
                "maxDate": null,
                "minDate": null,
                "maxSize": null,
                "acceptedFormat": null
            },
            {
                "pk": 96,
                "name": "monthly_charges",
                "displayedName": "Charges mensuel",
                "type": "integer",
                "isRequired": true,
                "validation": null,
                "sensitiveData": false,
                "attributechoice_set": [],
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
        ]
    },
    "meta": {
        "timestamp": "2025-05-20T13:27:25.746149",
        "request_id": "7ad6fbda-e35a-45d8-b983-fde90770b092"
    }
}

</div>```
## Création de profils
Pour créer un profile vous devez envoyer une requête POST à cet endpoints api/v1/profiles/ avec le corps de la 
requeête contenant 
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
## Modifier un profil
## Supprimer un profil
## Soumettre d'un profil
## Faire une demande d'analyse d'un profil
## Voir les détails d'une analyse
## Configuration d'un webhook
## Consultation d'un webhook
## Suppression d'un webhook
