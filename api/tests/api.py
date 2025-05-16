from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import *

class ApiTestCase(APITestCase):
    def setUp(self):
        self.partners = [
            Partner.objects.create(name="admin", limitUsage=1000),
            Partner.objects.create(name="bank", limitUsage=3)
        ]
        self.attributes = [
            Attribute.objects.create(
                name="lastname", 
                displayedName="Nom", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="firstname", 
                displayedName="Prénom", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="email", 
                displayedName="Email", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
                regex='/^[a-zA-Z0-9. _%+-]+@[a-zA-Z0-9',
                validation='regex'
            ),
            Attribute.objects.create(
                name="phone_number", 
                displayedName="Numéro de téléphone", 
                type="string", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
                validation='regex',
                regex=' (?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
            ),
            Attribute.objects.create(
                name="birth_date", 
                displayedName="Date de naissance", 
                type="date", 
                category="personal data", 
                isRequired=True, 
                sensitiveData=False,
            ),
            Attribute.objects.create(
                name="birth_country", 
                displayedName="Pays de naissance", 
                type="choice", 
                category="unique choice", 
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="birth_town", 
                displayedName="Ville de naissance", 
                type="string", 
                category="personal data", 
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="identity_document_type", 
                displayedName="Type de pièce d'identité", 
                type="choice", 
                category="identity document", 
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="identity_document_number", 
                displayedName="Numéro de pièce d'identité", 
                type="string", 
                category="identity document", 
                isRequired=False,
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="billing_address1", 
                displayedName="Adresse de facturation 1", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="billing_address2", 
                displayedName="Adresse de facturation 2", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="billing_zip_code", 
                displayedName="Code postal de facturation", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="billing_town", 
                displayedName="Ville de facturation", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="billing_country", 
                displayedName="Pays de facturation", 
                type="choice", 
                validation='unique choice',
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="delivery_address1", 
                displayedName="Adresse de livraison1", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="delivery_address2", 
                displayedName="Adresse de livraison2", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="delivery_zip_code", 
                displayedName="Code postal de livraison", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="delivery_town", 
                displayedName="Ville de livraison", 
                type="string", 
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="delivery_country", 
                displayedName="Pays de livraison", 
                type="choice", 
                validation='unique choice',
                category="address",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="housing_situation", 
                displayedName="Situation de logement", 
                type="choice", 
                validation='unique choice',
                category="housing situation",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="other_housing_situation", 
                displayedName="Situation de logement autre", 
                type="string", 
                category="housing situation",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="family_situation", 
                displayedName="Situation familiale", 
                type="choice", 
                category="family situation",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="children_number", 
                displayedName="Nombre d'enfants", 
                type="integer", 
                validation='min/max value',
                minValue=0,
                category="children",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="professional_situation", 
                displayedName="Situation professionnelle", 
                type="choice", 
                validation='unique choice',
                category="professional situation",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="product_usage", 
                displayedName="Usage du produit", 
                type="choice", 
                validation='unique choice',
                category="product usage",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="monthly_income", 
                displayedName="Revenu mensuel", 
                type="integer", 
                category="income and expenses",
                isRequired=True, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="monthly_charges", 
                displayedName="Charges mensuel", 
                type="integer", 
                category="income and expenses",
                isRequired=True, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="scholarship_student", 
                displayedName="étudiant boursier", 
                type="boolean", 
                category="diverse",
                isRequired=False, 
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="years_in_current_job", 
                displayedName="Années de poste actuel", 
                type="integer", 
                category="diverse",
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="means_of_movement", 
                displayedName="Moyen de déplacement", 
                type="choice", 
                validation='multiple choice',
                category="diverse",
                sensitiveData=False
            ),
            Attribute.objects.create(
                name="bank_statement", 
                displayedName="Relevé bancaire", 
                type="file", 
                acceptedFormat="pdf",
                category="documents",
                sensitiveData=True
            ),
            Attribute.objects.create(
                name="proof_of_address", 
                displayedName="Justificatif de domicile", 
                type="file", 
                acceptedFormat="pdf",
                category="documents",
                sensitiveData=True
            ),
            
        ]
        self.attribute_choices = [

        ]
        self.attribute_attribute_choice = [

        ]
        