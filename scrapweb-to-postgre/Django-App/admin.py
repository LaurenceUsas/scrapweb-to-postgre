from django.contrib import admin

from .models import UnitHistory, UnitInformation, RawData

admin.site.register(UnitHistory)
admin.site.register(UnitInformation)
admin.site.register(RawData)