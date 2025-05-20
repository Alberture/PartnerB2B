from django.urls import reverse
from django.test import Client

from rest_framework.test import APITestCase

from api.models import *

from PIL import Image

class ApiTestCase(APITestCase):
    def setUp(self):
        self.partners = {
            "admin":Partner.objects.create(name="admin", limitUsage=1000, activationStatus="success"),
            "bank":Partner.objects.create(name="bank", limitUsage=3, activationStatus="success"),
            "real_estate_agency":Partner.objects.create(name="real estate agency", limitUsage=3),
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
                validation="unique choice", 
                category="personal data", 
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
                isRequired=True, 
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

        self.profiles = {
            Profile.objects.create(partner=self.partners['bank'], status="complete") : [
                ProfileAttribute.objects.create(attribute=self.attributes['firstname'], profile=Profile.objects.get(partner=self.partners['bank']), value="Jean-Luck"),
                ProfileAttribute.objects.create(attribute=self.attributes['lastname'], profile=Profile.objects.get(partner=self.partners['bank']), value="Sithi"),
                ProfileAttribute.objects.create(attribute=self.attributes['email'], profile=Profile.objects.get(partner=self.partners['bank']), value="sithijeanluck@gmail.com"),
                ProfileAttribute.objects.create(attribute=self.attributes['birth_date'], profile=Profile.objects.get(partner=self.partners['bank']), value="2005-07-21"),
                ProfileAttribute.objects.create(attribute=self.attributes['monthly_income'], profile=Profile.objects.get(partner=self.partners['bank']), value="0"),
                ProfileAttribute.objects.create(attribute=self.attributes['monthly_charges'], profile=Profile.objects.get(partner=self.partners['bank']), value="0"),
                ProfileAttribute.objects.create(attribute=self.attributes['phone_number'], profile=Profile.objects.get(partner=self.partners['bank']), value="0768057143"),
                ProfileAttribute.objects.create(attribute=self.attributes['scholarship_student'], profile=Profile.objects.get(partner=self.partners['bank']), value="True"),
                ProfileAttribute.objects.create(attribute=self.attributes['professional_situation'], profile=Profile.objects.get(partner=self.partners['bank']), value="étudiant"),
            ],
            Profile.objects.create(partner=self.partners['real_estate_agency'], status="complete") : [
                ProfileAttribute.objects.create(attribute=self.attributes['firstname'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="Cyril"),
                ProfileAttribute.objects.create(attribute=self.attributes['lastname'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="Perosino"),
                ProfileAttribute.objects.create(attribute=self.attributes['email'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="cyrilperosino@gmail.com"),
                ProfileAttribute.objects.create(attribute=self.attributes['birth_date'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="2002-07-21"),
                ProfileAttribute.objects.create(attribute=self.attributes['monthly_income'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="0"),
                ProfileAttribute.objects.create(attribute=self.attributes['monthly_charges'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="0"),
                ProfileAttribute.objects.create(attribute=self.attributes['phone_number'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="0768057143"),
                ProfileAttribute.objects.create(attribute=self.attributes['scholarship_student'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="True"),
                ProfileAttribute.objects.create(attribute=self.attributes['professional_situation'], profile=Profile.objects.get(partner=self.partners['real_estate_agency']), value="étudiant"),
            ],
            Profile.objects.create(partner=self.partners['bank']): []
        }

        self.request_body_for_create_profile = {
            "attributes": {
                "firstname": "Jean-Luck",
                "lastname": "Sithi",
                "email": "sithijeanluck@gmail.com",
                "birth_date": "2005-07-21",
                "monthly_income": 0,
                "monthly_charges": 0,
                "phone_number": "0768057143",
                "scholarship_student": "True",
                "professional_situation": "étudiant",
                "delivery_address1": "3 rue truc"
            }
        }

        Analysis.objects.create(profile=Profile.objects.get(pk=1))
        Analysis.objects.create(profile=Profile.objects.get(pk=2))
    
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
        self.authenticate('bank')
        
        url = reverse('metadata')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 11)

    def test_cant_create_profile_with_missing_attributes(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        request_body = {
            "attributes": {
                "firstname": "Jean-Luck"
            }
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'][0], 'Missing required attributes.')

    def test_cant_create_profile_with_invalid_attribute_name(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        self.request_body_for_create_profile['attributes']['firname'] = "Jean-Luck"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Attribute Not Found')  
    
    def test_cant_create_profile_without_activated_api_key(self):

        self.authenticate('real_estate_agency')
        url = reverse('profiles-list')
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Not Allowed')

    def test_cant_create_profile_with_a_choice_that_does_not_exist_for_an_attribute(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        self.request_body_for_create_profile['attributes']['professional_situation'] = "invalid choice"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'][0], 'Choice does not exist.')
    
    def test_cant_create_profile_with_multiple_choices_for_an_attribute_with_unique_choice_validation(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        self.request_body_for_create_profile['attributes']['professional_situation'] = ["étudiant", "salarié"]
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'][0], 'Choice must be unique')    
    
    def test_cant_create_profile_with_invalid_regex_for_attribute_with_regex_validation(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        self.request_body_for_create_profile['attributes']['phone_number'] = "1234567890"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Regex match invalid')   

    def test_cant_create_profile_with_invalid_value_type_for_an_attribute(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        #invalid integer
        self.request_body_for_create_profile['attributes']['monthly_income'] = "monthly_income"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Type Error')   
        #invalid date
        self.request_body_for_create_profile['attributes']['birth_date'] = "9999-99-99"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400) 
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Type Error')   
        #invalid date format
        self.request_body_for_create_profile['attributes']['birth_date'] = "01/01/2020"
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400)   
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Type Error')   

    def test_cant_create_profile_with_missing_conditionally_required_attributes(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        request_body = {
            "attributes": {attribute: value for attribute, value in self.request_body_for_create_profile['attributes'].items() if attribute != "scholarship_student"}
        }
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 400)  
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'][0], 'Missing required attributes.')  

    def test_cant_create_profile_with_invalid_interval_value(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        self.request_body_for_create_profile['attributes']['children_number'] = -1
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.data.get('data'))
        self.assertEqual(response.data['error']['message'], 'Invalid value')   

    def test_create_valid_profile(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        response = self.client.post(url, self.request_body_for_create_profile, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data.get('data'))
        self.assertEqual(response.data['data']['status'], 'draft')
        self.assertEqual(response.data['data']['profileattribute_set'][0]['value'], 'Jean-Luck')
        self.assertEqual(response.data['data']['profileattribute_set'][1]['value'], 'Sithi')

    def test_create_valid_profile_without_external_reference(self):
        self.authenticate('bank')
        url = reverse('profiles-list')
        request_body = {attribute: value for attribute, value in self.request_body_for_create_profile.items() if attribute != "externalReference"}
        response = self.client.post(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data.get('data'))

    def test_partner_can_retrieve_their_profiles_only(self):
        self.authenticate('bank')
        url = reverse('profiles-detail', kwargs={"pk": 1})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['profileattribute_set'][0]['value'], 'Jean-Luck')
        self.assertEqual(response.data['data']['profileattribute_set'][1]['value'], 'Sithi')
        
        url = reverse('profiles-detail', kwargs={"pk": 2})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
    
    def test_partner_can_update_their_profiles_only(self):
        self.authenticate('bank')

        url = reverse('profiles-detail', kwargs={"pk": 1})
        request_body = {
            "attributes":{
                "firstname": "Hugo"
            }
        }
        response = self.client.patch(url, request_body, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.data['data']['profileattribute_set'][0]['value'], "Hugo")
        
        url = reverse('profiles-detail', kwargs={"pk": 2})
        response = self.client.patch(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_partner_can_delete_their_profiles_only(self):
        self.authenticate('bank')

        url = reverse('profiles-detail', kwargs={"pk": 1})
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['message'], 'Le profil à bien été supprimé.')

        url = reverse('profiles-detail', kwargs={"pk": 2})
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
    
    def test_partner_can_submit_their_profiles_only(self):
        self.authenticate('bank')
        url = reverse('profiles-submit', kwargs={"pk": 1})
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        url = reverse('profiles-detail', kwargs={"pk": 1})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.data['data']['status'], "complete")

        url = reverse('profiles-submit', kwargs={"pk": 2})
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
    
    def test_partner_can_create_analysis_for_their_submitted_profiles_only(self):
        self.authenticate("bank")
        url = reverse('profiles-create-analysis', kwargs={"pk": 1})
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['message'], "Vous venez de faire une demande d'analyse pour le profile 1")
        self.assertEqual(response.data['data']['status'], "pending")

        url = reverse('profiles-create-analysis', kwargs={"pk": 3})
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error']['message'], 'Profile not submitted')

        url = reverse('profiles-create-analysis', kwargs={"pk": 2})
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
    
    def test_partner_can_retrieve_analysis_of_their_profiles_only(self):
        self.authenticate("bank")
        url = reverse('analysis-detail', kwargs={"pk": 1})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['status'], 'pending')

        url = reverse('analysis-detail', kwargs={"pk": 2})
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        
    def authenticate(self, partner_name):
        url = reverse('token')
        response = self.client.post(url, {"apiKey": self.partners[partner_name].apiKey})
        access_token = response.data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)