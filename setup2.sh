python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download fr_dep_news_trf
python -m unittest
pip install -U pip setuptools wheel
pip install -U 'spacy[cuda118,transformers,lookups]'
cd src/