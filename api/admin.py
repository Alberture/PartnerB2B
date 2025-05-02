from django.contrib import admin
from api.models import Partner, Attribute, AttributeChoice

# Register your models here.

admin.site.register(Partner)
admin.site.register(Attribute)
admin.site.register(AttributeChoice)