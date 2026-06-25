from django.db import models

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    kolejnosc = models.IntegerField(default=1, verbose_name="Kolejność")
    publikuj = models.BooleanField(default=True, verbose_name="Publikuj")
    kategoria_nadrzedna = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, 
        related_name='podkategorie', verbose_name="Kategoria nadrzędna"
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa

class Szkolenie(models.Model):
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, related_name='szkolenia', verbose_name="Kategoria")
    tytul = models.CharField(max_length=200, verbose_name="Tytuł szkolenia")
    opis = models.TextField(verbose_name="Opis")
    numer = models.CharField(max_length=50, verbose_name="Numer szkolenia")
    cena = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Cena")
    liczba_godzin = models.IntegerField(verbose_name="Liczba godzin")
    kolejnosc = models.IntegerField(default=1, verbose_name="Kolejność")
    publikuj = models.BooleanField(default=True, verbose_name="Publikuj")

    class Meta:
        verbose_name = "Szkolenie"
        verbose_name_plural = "Szkolenia"

    def __str__(self):
        return self.tytul

class Rejestracja(models.Model):
    szkolenie = models.ForeignKey(Szkolenie, on_delete=models.CASCADE, verbose_name="Szkolenie")
    imie = models.CharField(max_length=100, verbose_name="Imię")
    nazwisko = models.CharField(max_length=100, verbose_name="Nazwisko")
    email = models.EmailField(verbose_name="Adres E-mail")
    zgoda_rodo = models.BooleanField(default=False, verbose_name="Zgoda RODO")

    class Meta:
        verbose_name = "Rejestracja"
        verbose_name_plural = "Rejestracje"

    def __str__(self):
        return f"{self.imie} {self.nazwisko} - {self.szkolenie.tytul}"

class ZgloszenieProblemu(models.Model):
    MODUL_CHOICES = [
        ('oferta', 'Moduł Oferty Szkoleniowej'),
        ('rejestracja', 'Moduł Rejestracji i Zapisów'),
        ('panel', 'Panel Zarządzania (Manager)'),
        ('api', 'Interfejs API'),
        ('inne', 'Inne / Niezidentyfikowane'),
    ]

    autor = models.CharField(max_length=150, verbose_name="Autor zgłoszenia (Imię/Email)")
    temat = models.CharField(max_length=200, verbose_name="Temat zgłoszenia")
    tresc = models.TextField(verbose_name="Treść – opis problemu")
    modul = models.CharField(max_length=50, choices=MODUL_CHOICES, default='inne', verbose_name="Wybór modułu aplikacji")
    zalacznik = models.ImageField(upload_to='problemy_zalaczniki/', null=True, blank=True, verbose_name="Opcjonalny załącznik graficzny")
    data_zgloszenia = models.DateTimeField(auto_now_add=True, verbose_name="Data i godzina zgłoszenia")

    class Meta:
        verbose_name = "Zgłoszenie problemu"
        verbose_name_plural = "Zgłoszenia problemów"

    def __str__(self):
        return f"[{self.get_modul_display()}] {self.temat} - {self.autor}"

class SzablonWiadomosci(models.Model):
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa szablonu")
    tresc = models.TextField(verbose_name="Treść szablonu (HTML)")

    class Meta:
        verbose_name = "Szablon wiadomości"
        verbose_name_plural = "Szablony wiadomości"

    def __str__(self):
        return self.nazwa
