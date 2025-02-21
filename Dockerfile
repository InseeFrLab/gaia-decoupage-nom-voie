FROM inseefrlab/onyxia-python-pytorch:py3.12.6

ENV TIMEOUT=3600

ENV PROJ_LIB=/opt/conda/share/proj

# set api as the current work dir
WORKDIR /api

COPY requirements.txt requirements.txt
COPY src/decoupage_libelles /api/decoupage_libelles
COPY data /api/dat
# install all the requirements
RUN wget -P data/ https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.7.0.zip &&\
    unzip data/fr_dep_news_trf-3.7.0.zip -d data/ &&\
    rm data/fr_dep_news_trf-3.7.0.zip &&\
    pip install --no-cache-dir --upgrade -r requirements.txt &&\
    cd src/

RUN apt-get update && apt-get install -y unzip wget && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    wget -P api/data/ https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.7.0.zip && \
    unzip api/data/fr_dep_news_trf-3.7.0.zip -d api/data/ && \
    rm api/data/fr_dep_news_trf-3.7.0.zip

# Exposer le port 8000 pour FastAPI
EXPOSE 8000

# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "decoupage_libelles.entrypoints.web.main_api:app",  "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "3600"]