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

Pour obtenir un access token il faut envoyer votre clef API à cet endpoint /api/v1/auth/token/ avec le corps 
de la requête en JSON et contenant 
```
json
{
  "apiKey": VOTRE_CLEF_API
}
```
et obtiendrez une réponse resemblant à 
```
json
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

Pour pouvoir refresh l'access token il suffit d'envoyer le refresh token à cet endpoint /api/v1/auth/token/refresh/ avec le corps 
de la requête en JSON et contenant 
```
json
{
  "refresg": VOTRE_REFRESH_TOKEN
}
```
et obtiendrez une réponse resemblant à 
```
json
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


# Utilisation
## Liste des attributs
## Création de profils
## Modifier un profil
## Supprimer un profil
## Soumettre d'un profil
## Faire une demande d'analyse d'un profil
## Voir les détails d'une analyse
## Configuration d'un webhook
## Consultation d'un webhook
## Suppression d'un webhook
