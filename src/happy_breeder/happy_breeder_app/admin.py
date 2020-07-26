from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Breeder)
admin.site.register(Item)
admin.site.register(BreederItemThrough)
admin.site.register(Pet)
admin.site.register(Record)
