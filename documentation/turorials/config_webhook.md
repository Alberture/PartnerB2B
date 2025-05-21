# Configuration d'un webhook
Pour configurer un webhook il faut à cet endpoint /api/v1/webhooks/configure/ faire un POST avec le corps de la requête contenant 
```json
{
  "url": "VOTRE_URL"
}
```
Vous devrez obtenir un message de confirmation comme quoi ce dernier a été configuré.
