# Utilisation de l'image de base Python officielle
FROM python:3.12-slim

# Mise à jour des listes de paquets et installation de wget
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV TIMEOUT=3600

ENV PROJ_LIB=/opt/conda/share/proj

# set api as the current work dir
WORKDIR /api

COPY requirements.txt requirements.txt
COPY src/decoupage_libelles /api/decoupage_libelles
COPY data /api/data

RUN rm -rf /tmp/*

RUN wget -q -O /tmp/fr_dep_news_trf-3.7.0.zip https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.7.0.zip

RUN unzip /tmp/downloads/fr_dep_news_trf-3.7.0.zip -d /api/data/

RUN rm -rf /tmp

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Exposer le port 8000 pour FastAPI
EXPOSE 8000

# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "decoupage_libelles.entrypoints.web.main_api:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "3600"]