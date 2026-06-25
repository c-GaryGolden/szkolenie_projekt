Przygotowanie środowiska:
Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Migracja bazy danych:
Bash
python manage.py migrate

Uruchomienie serwera:
Bash
python manage.py runserver

Admin: http://127.0.0.1:8000/admin/


Dostępna dla użytkowników poprzez przeglądarkę internetową.

Strona główna: /offer/kategorie/ – Wyświetla listę wszystkich dostępnych kategorii szkoleń.

Szczegóły: /offer/kategorie/<id>/ – Wyświetla ofertę w wybranej kategorii.

Opis szkolenia: /offer/kategorie/<id>/course/<id>/ – Szczegółowe informacje o wybranym szkoleniu.

Zapisy: /offer/register/ – Formularz rejestracji na szkolenie.

Zgłaszanie awarii: /offer/issues/ – Formularz zgłaszania problemów technicznych (obsługuje załączniki).

Panel Managera: /offer/offer-mng/ – Główny punkt dostępu do zarządzania ofertą (wymaga uprawnień).

