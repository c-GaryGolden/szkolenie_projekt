import os
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Kategoria, Szkolenie, Rejestracja, ZgloszenieProblemu, SzablonWiadomosci
from .forms import KategoriaForm, SzkolenieForm, RejestracjaForm, ProblemForm

# ==================== OFERTA PANEL (WYMAGA LOGOWANIA) ====================

@login_required
def panel_glowny(request):
    return render(request, 'offer/panel_manager.html')

@login_required
def categ_lst(request):
    kat = list(Kategoria.objects.values_list('nazwa', flat=True))
    return HttpResponse(f"<h3>Lista kategorii (Mng):</h3> {kat}")

@login_required
def course_lst(request):
    szk = list(Szkolenie.objects.values_list('tytul', flat=True))
    return HttpResponse(f"<h3>Lista szkoleń (Mng):</h3> {szk}")

@login_required
def categ_add(request):
    if request.method == 'POST':
        form = KategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_glowny')
    else:
        form = KategoriaForm()
    return render(request, 'offer/form_generic.html', {'form': form, 'tytul': 'Dodaj Kategorię'})

@login_required
def course_add(request):
    if request.method == 'POST':
        form = SzkolenieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_glowny')
    else:
        form = SzkolenieForm()
    return render(request, 'offer/form_generic.html', {'form': form, 'tytul': 'Dodaj Szkolenie'})


# ==================== OFERTA PUBLICZNA & FORMS ====================

def kategorie_lista(request):
    kategorie = Kategoria.objects.filter(publikuj=True, kategoria_nadrzedna__isnull=True).order_by('kolejnosc')
    return render(request, 'offer/kategorie_lista.html', {'kategorie': kategorie})

def szkolenia_lista_w_kat(request, kategoria):
    kat = get_object_or_404(Kategoria, pk=kategoria)
    szkolenia = Szkolenie.objects.filter(kategoria=kat, publikuj=True).order_by('kolejnosc')
    return render(request, 'offer/szkolenia_lista.html', {'kategoria': kat, 'szkolenia': szkolenia})

def szkolenie_opis(request, kateg, id):
    szkolenie = get_object_or_404(Szkolenie, pk=id)
    return render(request, 'offer/szkolenie_opis.html', {'szkolenie': szkolenie})

def rejestracja_form(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'offer/sukces.html', {'message': 'Zapisano pomyślnie!'})
    else:
        form = RejestracjaForm()
    return render(request, 'offer/form_generic.html', {'form': form, 'tytul': 'Formularz rejestracji'})

def zgloszenie_problemu(request):
    if request.method == 'POST':
        # KLUCZOWE: request.FILES musi tu być, aby obsłużyć załącznik graficzny!
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'offer/sukces.html', {'message': 'Zgłoszenie problemu zostało wysłane pomyślnie.'})
    else:
        form = ProblemForm()
    return render(request, 'offer/form_generic.html', {'form': form, 'tytul': 'Zgłoś błąd systemu'})


# ==================== OSTATECZNE UKŁAD ENDPOINTÓW API ====================

# /formTemplates -> Odczyt z pliku JSON struktury formularza
def api_form_templates(request):
    file_path = os.path.join(settings.BASE_DIR, 'form_definition.json')
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"form": "Rejestracja", "fields": ["imie", "nazwisko", "email"]}, f)
    with open(file_path, 'r', encoding='utf-8') as f:
        return JsonResponse(json.load(f))

# /messageTemplates -> Odczyt z bazy danych, zwrot formatu HTML
def api_message_templates(request):
    szablon, _ = SzablonWiadomosci.objects.get_or_create(
        nazwa="Domyślny", 
        defaults={"tresc": "<html><body><h1>Szablon z bazy danych HTML</h1></body></html>"}
    )
    return HttpResponse(szablon.tresc, content_type="text/html")

# /categories -> Kategorie zapisane NA STAŁE w kodzie funkcji widoku (Wymaganie!)
def api_categories_hardcoded(request):
    statyczne_kategorie = [
        {"id": 501, "nazwa": "Zahardkodowana Kategoria A", "kolejnosc": 1},
        {"id": 502, "nazwa": "Zahardkodowana Kategoria B", "kolejnosc": 2}
    ]
    return JsonResponse({"categories": statyczne_kategorie})

# /courses -> Odczyt JSON z tabeli BD
def api_courses(request):
    return JsonResponse({"courses": list(Szkolenie.objects.values())})

# /registers -> Odczyt JSON z tabeli BD (Lista osób)
def api_registers(request):
    return JsonResponse({"registers": list(Rejestracja.objects.values())})

# /register/ -> Odczyt JSON z tabeli BD jednej osoby (pierwszej z brzegu lub przez ?id=)
def api_register_detail(request):
    user_id = request.GET.get('id')
    
    # Jeśli użytkownik podał ?id=X, szukaj tego ID. Jeśli nie, weź pierwszy rekord z brzegu.
    if user_id:
        reg = Rejestracja.objects.filter(pk=user_id).first()
    else:
        reg = Rejestracja.objects.first()
        
    # Jeśli tabela jest całkowicie pusta lub nie ma takiego ID:
    if not reg:
        return JsonResponse({
            "error": "Brak rekordów w bazie danych. Dodaj najpierw użytkownika przez formularz lub panel admina."
        }, status=404)
        
    return JsonResponse({
        "id": reg.id, 
        "imie": reg.imie, 
        "nazwisko": reg.nazwisko, 
        "email": reg.email
    })

# /problemReport -> TRYB ZAPIS do bazy danych z żądania zewnętrznego
@csrf_exempt
def api_problem_report_save(request):
    if request.method == 'POST':
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        obj = ZgloszenieProblemu.objects.create(
            autor=data.get('autor', 'System API'),
            temat=data.get('temat', 'Błąd automatyczny'),
            tresc=data.get('tresc', 'Opis problemu wygenerowany przez API'),
            modul=data.get('modul', 'api')
        )
        return JsonResponse({"status": "saved", "id": obj.id}, status=201)
    return JsonResponse({"error": "Metoda POST wymagana"}, status=405)

# /problems -> Odczyt JSON z bazy danych + PEŁNE WYMAGANIE LAB-29
def api_problems_list(request):
    # LAB-29 realizowane w jednym zapytaniu ORM:
    # 1. Pobieranie + 2. Filtrowanie + 3. Dopasowanie do wzorca (__icontains) + 4. Sortowanie + 5. Limit ([:5])
    queryset = ZgloszenieProblemu.objects.filter(
        modul='api',
        temat__icontains='błąd'
    ).order_by('-data_zgloszenia')[:5]
    
    return JsonResponse({"problems": list(queryset.values())})
