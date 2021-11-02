from django.contrib import admin
from finliveapp import models
from rest_framework_api_key.admin import APIKeyModelAdmin
# Register your models here.

admin.site.register(models.AccountOrganization)
admin.site.register(models.Organization)
admin.site.register(models.UserAccount)
admin.site.register(models.SeedingType)
admin.site.register(models.Gender)
admin.site.register(models.Laboratory)
admin.site.register(models.Breed)
admin.site.register(models.Barn)
admin.site.register(models.MilkingSystem)
admin.site.register(models.Equipment)


@admin.register(models.OrganizationAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


