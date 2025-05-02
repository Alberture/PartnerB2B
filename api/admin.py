from django.contrib import admin
from api.models import Partner, Attribute, AttributeChoice, Profile, ProfileAttribute

# Register your models here.

admin.site.register(Partner)
admin.site.register(Attribute)
admin.site.register(AttributeChoice)
admin.site.register(Profile)
admin.site.register(ProfileAttribute)