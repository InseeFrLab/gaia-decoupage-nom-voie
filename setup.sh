pip install -r requirements.txt
unzip data/fr_dep_news_trf-3.7.0.zip -d data/
rm data/fr_dep_news_trf-3.7.0.zip
python -m unittest
cd src/