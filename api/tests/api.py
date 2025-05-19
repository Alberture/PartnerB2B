from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import *
from django.contrib.auth.models import User

class ApiTestCase(APITestCase):
    def setUp(self):
        self.partners = {
            "admin":Partner.objects.create(name="admin", limitUsage=1000),
            "bank":Partner.objects.create(name="bank", limitUsage=3)
        }
        self.attributes = {
            "lastname": Attribute.objects.create(
                name="lastname", 
                displayedName="Nom", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False
            ),
            "firstname": Attribute.objects.create(
                name="firstname", 
                displayedName="Prénom", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False
            ),
            "gender": Attribute.objects.create(
                name="gender", 
                displayedName="Genre", 
                type="choice", 
                validation='unique choice',
                category="personal data", 
                isRequired=False, 
                sensitiveData=False
            ),
            "email": Attribute.objects.create(
                name="email", 
                displayedName="Email", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
                regex=r"^\S+@\S+\.\S+$",
                validation='regex'
            ),
            "phone_number":Attribute.objects.create(
                name="phone_number", 
                displayedName="Numéro de téléphone", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
                validation='regex',
                regex=r"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$",
            ),
            "birth_date":Attribute.objects.create(
                name="birth_date", 
                displayedName="Date de naissance", 
                type="date", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
            ),
            "birth_country":Attribute.objects.create(
                name="birth_country", 
                displayedName="Pays de naissance", 
                type="choice", 
                category="unique choice", 
                isRequired=False, 
                sensitiveData=False
            ),
            "birth_town":Attribute.objects.create(
                name="birth_town", 
                displayedName="Ville de naissance", 
                type="string", 
                category="personal data", 
                isRequired=False, 
                sensitiveData=False
            ),
            "identity_document_type":Attribute.objects.create(
                name="identity_document_type", 
                displayedName="Type de pièce d'identité", 
                type="choice", 
                category="identity document", 
                isRequired=False, 
                sensitiveData=False
            ),
            "identity_document_number":Attribute.objects.create(
                name="identity_document_number", 
                displayedName="Numéro de pièce d'identité", 
                type="string", 
                category="identity document", 
                isRequired=False,
                sensitiveData=False
            ),
            "billing_address1":Attribute.objects.create(
                name="billing_address1", 
                displayedName="Adresse de facturation 1", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "billing_address2":Attribute.objects.create(
                name="billing_address2", 
                displayedName="Adresse de facturation 2", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "billing_zip_code":Attribute.objects.create(
                name="billing_zip_code", 
                displayedName="Code postal de facturation", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "billing_town":Attribute.objects.create(
                name="billing_town", 
                displayedName="Ville de facturation", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "billing_country":Attribute.objects.create(
                name="billing_country", 
                displayedName="Pays de facturation", 
                type="choice", 
                validation='unique choice',
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "delivery_address1":Attribute.objects.create(
                name="delivery_address1", 
                displayedName="Adresse de livraison1", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "delivery_address2":Attribute.objects.create(
                name="delivery_address2", 
                displayedName="Adresse de livraison2", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "delivery_zip_code":Attribute.objects.create(
                name="delivery_zip_code", 
                displayedName="Code postal de livraison", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "delivery_town":Attribute.objects.create(
                name="delivery_town", 
                displayedName="Ville de livraison", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "delivery_country":Attribute.objects.create(
                name="delivery_country", 
                displayedName="Pays de livraison", 
                type="choice", 
                validation='unique choice',
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            "housing_situation":Attribute.objects.create(
                name="housing_situation", 
                displayedName="Situation de logement", 
                type="choice", 
                validation='unique choice',
                category="housing situation",
                isRequired=False, 
                sensitiveData=False
            ),
            "other_housing_situation":Attribute.objects.create(
                name="other_housing_situation", 
                displayedName="Situation de logement autre", 
                type="string", 
                category="housing situation",
                isRequired=False, 
                sensitiveData=False
            ),
            "family_situation":Attribute.objects.create(
                name="family_situation", 
                displayedName="Situation familiale", 
                type="choice",
                category="family situation",
                isRequired=False, 
                sensitiveData=False
            ),
            "children_number":Attribute.objects.create(
                name="children_number", 
                displayedName="Nombre d'enfants", 
                type="integer", 
                validation='min/max value',
                minValue=0,
                category="children",
                isRequired=False, 
                sensitiveData=False
            ),
            "professional_situation":Attribute.objects.create(
                name="professional_situation", 
                displayedName="Situation professionnelle", 
                type="choice", 
                validation='unique choice',
                category="professional situation",
                isRequired=False, 
                sensitiveData=False
            ),
            "product_usage":Attribute.objects.create(
                name="product_usage", 
                displayedName="Usage du produit", 
                type="choice", 
                validation='unique choice',
                category="product usage",
                isRequired=False, 
                sensitiveData=False
            ),
            "monthly_income":Attribute.objects.create(
                name="monthly_income", 
                displayedName="Revenu mensuel", 
                type="integer", 
                category="income and expenses",
                isRequired=True, 
                sensitiveData=False
            ),
            "monthly_charges":Attribute.objects.create(
                name="monthly_charges", 
                displayedName="Charges mensuel", 
                type="integer", 
                category="income and expenses",
                isRequired=True, 
                sensitiveData=False
            ),
            "scholarship_student":Attribute.objects.create(
                name="scholarship_student", 
                displayedName="étudiant boursier", 
                type="boolean", 
                category="diverse",
                isRequired=False, 
                sensitiveData=False
            ),
            "years_in_current_job":Attribute.objects.create(
                name="years_in_current_job", 
                displayedName="Années de poste actuel", 
                type="integer", 
                category="diverse",
                isRequired=False, 
                sensitiveData=False
            ),
            "means_of_movement":Attribute.objects.create(
                name="means_of_movement", 
                displayedName="Moyen de déplacement", 
                type="choice", 
                validation='multiple choice',
                category="diverse",
                isRequired=False, 
                sensitiveData=False
            ),
            "bank_statement":Attribute.objects.create(
                name="bank_statement", 
                displayedName="Relevé bancaire", 
                type="file", 
                acceptedFormat="pdf",
                category="documents",
                isRequired=False, 
                sensitiveData=True
            ),
            "proof_of_address":Attribute.objects.create(
                name="proof_of_address", 
                displayedName="Justificatif de domicile", 
                type="file", 
                acceptedFormat="pdf",
                category="documents",
                isRequired=False, 
                sensitiveData=True
            ),
            
        }
        self.attribute_choices = {
            "M": AttributeChoice.objects.create(displayedName="M", attribute=self.attributes['gender']),
            "F":AttributeChoice.objects.create(displayedName="F", attribute=self.attributes['gender']),
            "autre genre":AttributeChoice.objects.create(displayedName="autre genre", attribute=self.attributes['gender']),
            "CI":AttributeChoice.objects.create(displayedName="CI", attribute=self.attributes['identity_document_type']),
            "passeport":AttributeChoice.objects.create(displayedName="passeport", attribute=self.attributes['identity_document_type']),
            "carte_sejour":AttributeChoice.objects.create(displayedName="carte_sejour", attribute=self.attributes['identity_document_type']),
            "locataire":AttributeChoice.objects.create(displayedName="locataire", attribute=self.attributes['housing_situation']),
            "colocataire":AttributeChoice.objects.create(displayedName="colocataire", attribute=self.attributes['housing_situation']),
            "propriétaire":AttributeChoice.objects.create(displayedName="propriétaire", attribute=self.attributes['housing_situation']),
            "accédant_propriété":AttributeChoice.objects.create(displayedName="accédant_propriété", attribute=self.attributes['housing_situation']),
            "hébergé_gratuit":AttributeChoice.objects.create(displayedName="hébergé_gratuit", attribute=self.attributes['housing_situation']),
            "autre situation d'habilitation":AttributeChoice.objects.create(displayedName="autre situation d'habilitation", attribute=self.attributes['housing_situation']),
            "célibataire":AttributeChoice.objects.create(displayedName="célibataire", attribute=self.attributes['family_situation']),
            "marié_pacsé":AttributeChoice.objects.create(displayedName="marié_pacsé", attribute=self.attributes['family_situation']),
            "séparé_divorcé":AttributeChoice.objects.create(displayedName="séparé_divorcé", attribute=self.attributes['family_situation']),
            "étudiant":AttributeChoice.objects.create(displayedName="étudiant", attribute=self.attributes['professional_situation']),
            "cadre":AttributeChoice.objects.create(displayedName="cadre", attribute=self.attributes['professional_situation']),
            "entrepreneur_chef_entreprise":AttributeChoice.objects.create(displayedName="entrepreneur_chef_entreprise", attribute=self.attributes['professional_situation']),
            "indépendant_libéral":AttributeChoice.objects.create(displayedName="indépendant_libéral", attribute=self.attributes['professional_situation']),
            "fonction_publique":AttributeChoice.objects.create(displayedName="fonction_publique", attribute=self.attributes['professional_situation']),
            "salarié":AttributeChoice.objects.create(displayedName="salarié", attribute=self.attributes['professional_situation']),
            "recherche_emploi":AttributeChoice.objects.create(displayedName="recherche_emploi", attribute=self.attributes['professional_situation']),
            "autre situation professionnelle":AttributeChoice.objects.create(displayedName="autre situation professionnelle", attribute=self.attributes['professional_situation']),
            "études":AttributeChoice.objects.create(displayedName="études", attribute=self.attributes['product_usage']),
            "loisir":AttributeChoice.objects.create(displayedName="loisir", attribute=self.attributes['product_usage']),
            "professionnel":AttributeChoice.objects.create(displayedName="professionnel", attribute=self.attributes['product_usage']),
            "marche":AttributeChoice.objects.create(displayedName="marche", attribute=self.attributes['means_of_movement']),
            "vélo":AttributeChoice.objects.create(displayedName="vélo", attribute=self.attributes['means_of_movement']),
            "auto":AttributeChoice.objects.create(displayedName="auto", attribute=self.attributes['means_of_movement']),
            "moto":AttributeChoice.objects.create(displayedName="moto", attribute=self.attributes['means_of_movement']),   
        }
        self.attribute_attribute_choice = [
            AttributeAttributeChoice.objects.create(attribute=self.attributes["other_housing_situation"], attribute_choice=self.attribute_choices["autre situation d'habilitation"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["scholarship_student"], attribute_choice=self.attribute_choices["étudiant"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["cadre"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["entrepreneur_chef_entreprise"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["indépendant_libéral"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["fonction_publique"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["salarié"]),
            AttributeAttributeChoice.objects.create(attribute=self.attributes["years_in_current_job"], attribute_choice=self.attribute_choices["autre situation professionnelle"]),     
        ]
    
    def test_cant_access_any_endpoint_except_auth_unless_authenticated(self):
        #Create profile
        url = reverse('profiles-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

        #List metadata
        url = reverse('metadata')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        #Retrieve Profile
        url = reverse('profiles-detail', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
               
        #Partial-Update Profile
        url = reverse('profiles-detail', kwargs={'pk':1})
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 401)

        #Delete Profile
        url = reverse('profiles-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
        
        #Submit Profile
        url = reverse('profiles-submit', kwargs={'pk':1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

        #Create Document
        url = reverse('documents-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

        #Retrieve Document
        url = reverse('documents-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        #Create Analysis
        url = reverse('analysis-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

        #Retrieve Analysis
        url = reverse('analysis-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        #Config Webhook
        url = reverse('webhooks-config')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

        #Retrieve Webhook
        url = reverse('webhooks-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

        #Partial-Update Webhook
        url = reverse('webhooks-detail', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

        #Delete Webhook
        url = reverse('webhooks-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

        # Get Access + Refresh token
        url = reverse('token')
        response = self.client.post(url, {"apiKey": self.partners['admin'].apiKey})
        refresh_token = response.data["data"]["refresh"]
        self.assertEqual(response.status_code, 200)

        # Refresh the token
        url = reverse('token_refresh')
        response = self.client.post(url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, 200)   

    def test_metadata(self):
        url = reverse('token')
        response = self.client.post(url, {"apiKey": self.partners['admin'].apiKey})
        access_token = response.data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        
        url = reverse('metadata')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 12)

    def test_create_profile(self):
        url = reverse('token')
        response = self.client.post(url, {"apiKey": self.partners['admin'].apiKey})
        access_token = response.data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        url = reverse('profiles-list')
        #error for missing required attributes
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'][0], 'Missing required attributes.')

        #error for attribute does not exist profile
        request_body = {
            "attributes": {
                "firname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 404) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Attribute Not Found')  

        #error for invalid choice for attribute with choices
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "invalid choice"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Attribute Not Found')  

        #error for multiple choice for attribute with choices with unique choice validation
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": ["étudiant", "salarié"]
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)     

        #error for multiple choice for attribute with choices with unique choice validation
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "means_of_movement": "vélo"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)     

        #error for value does not match an attribute with regex validation
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "1234567890",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400) 

        #error for invalid attribute type
        #integer
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": "monthly_income",
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            },
            "externalReference": "reference"
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        #invalid date
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "9999-99-99",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            },
            "externalReference": "reference"
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        #invalid date format
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "01/01/2020",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            },
            "externalReference": "reference"
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)   

        #error for missing conditionnaly required attribute(s)
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "professional_situation": "étudiant"
            },
            "externalReference": "reference"
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)  

        #valid profile
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant"
            },
            "externalReference": "reference"
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)   

