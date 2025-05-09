from django.contrib import admin
from api.models import Partner, Attribute, AttributeChoice, Profile, ProfileAttribute, Analysis, ProfileAttributeDocument, Webhook

# Register your models here.

admin.site.register(Partner)
admin.site.register(Attribute)
admin.site.register(AttributeChoice)
admin.site.register(Profile)
admin.site.register(ProfileAttribute)
admin.site.register(Analysis)
admin.site.register(ProfileAttributeDocument)
admin.site.register(Webhook)