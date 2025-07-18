from django.contrib import admin
from .models import Producer, Farm, Harvest, Crop

admin.site.register(Producer)
admin.site.register(Farm)
admin.site.register(Harvest)
admin.site.register(Crop)
