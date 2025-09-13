from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(CustomUser)
admin.site.register(Alert)
admin.site.register(GeoZone)
admin.site.register(Itinerary)
