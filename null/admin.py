from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Reservation)
admin.site.register(Time)
admin.site.register(ImageFile)
