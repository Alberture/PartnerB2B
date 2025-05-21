# Création de profils
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