pip install -r requirements.txt
python -m unittest
wget -P data/ https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.7.0.zip
unzip data/fr_dep_news_trf-3.7.0.zip -d data/
rm data/fr_dep_news_trf-3.7.0.zip
cd src/