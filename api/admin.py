from django.contrib import admin
from api.models import Partner, Attribute, AttributeChoice, Profile, ProfileAttribute, Analyse, Document

# Register your models here.

admin.site.register(Partner)
admin.site.register(Attribute)
admin.site.register(AttributeChoice)
admin.site.register(Profile)
admin.site.register(ProfileAttribute)
admin.site.register(Analyse)
admin.site.register(Document)