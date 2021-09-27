from django.contrib import admin
from finliveapp import models
# Register your models here.

admin.site.register(models.AccountOrganization)
admin.site.register(models.Organization)
admin.site.register(models.UserAccount)


