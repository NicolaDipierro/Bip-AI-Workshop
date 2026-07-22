FROM python:3.14-slim

WORKDIR /code

# Installazione delle dipendenze di sistema minime per scopi di caching
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e installazione dei requisiti Python
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia del codice sorgente
COPY ./app /code/app

# Esposizione della porta logica (Azure Container Apps mappa la 8000 di default)
EXPOSE 8000

# Avvio del server Uvicorn con worker asincroni
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]