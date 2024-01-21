FROM python:3.11-alpine

# Ustawiamy zmienną środowiskową
ENV APP_HOME /app

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy lokalny plik requirements.txt do kontenera
COPY ./requirements.txt /app/requirements.txt

# Instalujemy zależności wewnątrz kontenera
RUN pip install -r requirements.txt

# Kopiujemy inne pliki do katalogu roboczego kontenera
COPY . /app

# Ustawiamy bieżący katalog na podkatalog 'alfred'
WORKDIR /app/alfred

# Oznaczamy port, na którym aplikacja działa wewnątrz kontenera
EXPOSE 5000

# Uruchomiamy naszą aplikację wewnątrz kontenera
CMD ["python", "run_alfred.py"]

# Uruchomiamy naszą aplikację wewnątrz kontenera
ENTRYPOINT ["python", "run_alfred.py"]