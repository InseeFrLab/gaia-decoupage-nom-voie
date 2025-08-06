pip install -r requirements.txt
# pip install spacy-curated-transformers==2.0.0 --no-deps
python -m unittest
unzip data/fr_dep_news_trf-3.8.0-py3-none-any.zip -d data/fr_dep_news_trf-3.8.0/
rm data/fr_dep_news_trf-3.8.0-py3-none-any.zip
cd src/