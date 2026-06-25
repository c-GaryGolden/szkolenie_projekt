from django.contrib import admin
from .models import Kategoria, Szkolenie, Rejestracja, ZgloszenieProblemu, SzablonWiadomosci

# Rejestracja modeli w panelu admina
admin.site.register(Kategoria)
admin.site.register(Szkolenie)
admin.site.register(Rejestracja)
admin.site.register(ZgloszenieProblemu)
admin.site.register(SzablonWiadomosci)
