from django.contrib import admin
from .models import Animal
from .models import Equipement
from .models import Image

admin.site.register(Animal)
admin.site.register(Equipement)
admin.site.register(Image)