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
