python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python -m unittest
mc cp s3/travail/projet-ml-moteur-identification-gaia/open_data/fr_dep_news_trf-3.7.0.zip data/
unzip data/fr_dep_news_trf-3.7.0.zip -d data/
rm data/fr_dep_news_trf-3.7.0.zip
cd src/