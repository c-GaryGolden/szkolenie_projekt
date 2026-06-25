from django import forms
from .models import Kategoria, Szkolenie, Rejestracja, ZgloszenieProblemu

class KategoriaForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = ['nazwa', 'kolejnosc', 'publikuj', 'kategoria_nadrzedna']

class SzkolenieForm(forms.ModelForm):
    class Meta:
        model = Szkolenie
        fields = ['kategoria', 'tytul', 'opis', 'numer', 'cena', 'liczba_godzin', 'kolejnosc', 'publikuj']

class RejestracjaForm(forms.ModelForm):
    class Meta:
        model = Rejestracja
        fields = ['szkolenie', 'imie', 'nazwisko', 'email', 'zgoda_rodo']
        widgets = {
            'zgoda_rodo': forms.CheckboxInput(attrs={'required': True})
        }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = ZgloszenieProblemu
        fields = ['autor', 'temat', 'tresc', 'modul', 'zalacznik']
