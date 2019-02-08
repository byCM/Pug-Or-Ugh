from django.contrib import admin

from . import models

# register models here

admin.site.register(models.Dog)
admin.site.register(models.UserDog)
admin.site.register(models.UserPref)

