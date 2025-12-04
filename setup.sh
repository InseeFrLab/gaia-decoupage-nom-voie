pip install -r requirements.txt
# pip install spacy-curated-transformers==2.0.0 --no-deps # utile si une dépendance a un conflit et qu'on installe en amont une version qui fonctionne
python -m unittest

# Nom du modèle dans dépôt Nexus
nom_modele="spacy/fr_dep_news_trf"
# Téléchargement du modèle
curl "https://nexus.insee.fr/repository/huggingface-hosted/${nom_modele}/model.tar.gz" --output "model.tar.gz"
# Dezipp du dossier
mkdir -p fr_dep_news_trf-3.8.0/fr_dep_news_trf/fr_dep_news_trf-3.8.0/
tar -xzf model.tar.gz -C fr_dep_news_trf-3.8.0/fr_dep_news_trf/fr_dep_news_trf-3.8.0/
# Suppression modele zippé
rm model.tar.gz

cd src/