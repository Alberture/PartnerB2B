# JWT
JWT utilise un système d'access et refresh token. Un access token est un token permettant de vous authentifier et utiliser notre API, ce dernier ne dure que 1 heure.
Le refresh token intervient pour générer un autre access token et dure 1 semaine

## Access Token
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

| Champ  | Description |
| ------------- | ------------- |
| access | Ce champ corresponsd à l'access token qui vous permettra de vous identifier |
| refresg  | Ce champ correspond au refresh token qui vous permettra de renouveller votre access token  |

### Exemple avec postman

![image](https://github.com/user-attachments/assets/48dfc887-e7a6-44d4-ad1e-be9fb1a973ab)
![image](https://github.com/user-attachments/assets/f25dea34-bb00-4c48-a111-77f5412a619c)


Appuyez sur "Send" et vous obtiendez le résultat vu plus tôt.

## Refresh Token

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
| Champ  | Description |
| ------------- | ------------- |
| access | Ce champ corresponsd à l'access token qui vous permettra de vous identifier |

### Exemple avec postman

![image](https://github.com/user-attachments/assets/32c42cdf-771d-47af-93d7-b2b56f5b175b)
![image](https://github.com/user-attachments/assets/66f920be-4520-411a-9cab-b5c37eaa043a)
Appurez sur "Send" et vous obtendrez un résultat comme celui au dessus.

## S'authentifier

Pour s'authentifier il suffit de mettre dans les headers votre access token à chaque fois que vous réalisez une requête.

### Exemple avec postman

![image](https://github.com/user-attachments/assets/a815b0ae-72f3-4b8e-b9b0-58e8fe1905a7)
![image](https://github.com/user-attachments/assets/348d5af6-dbfe-4718-a8e3-5ce499acbaaf)


Si les 2 token venaient à expirer il faut de nouveau envoyer la clef API comme nous l'avons fait pour l'access token. A l'exception de ces 2 endpoints vous devrez être identifié pour avoir accès aux autres.
