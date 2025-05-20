# PartnerB2B

## Objectifs de l'API
Cette API a pour objectif de soumettre des données concernant les clients de partenaires
souhaitant évaluer la confiance d'un client pour réaliser un emprunt (immobilier , crédit, etc....)

# Authentification

## Obtenir une clef API
Pour obtenir la clef API il faut faire une demande auprès de Aberture.

## JWT
JWT utiliser un système d'access et refresh token. Un access token est un token permettant 
de vous authentifier et utiliser notre API et ne dure que 1 heure.
Le refresh token intervient pour générer un autre access token.

Pour obtenir un refresh token il faut votre clef API à cet endpoint /api/v1/auth/token/ avec le corps 
de la requête contenant
```
{
  "apiKey": VOTRE_CLEF_API
}
```
