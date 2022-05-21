from django.contrib import admin

from doctors.models import Doctor, SpokenLanguage

# Register your models here.
admin.site.register(Doctor)
admin.site.register(SpokenLanguage)