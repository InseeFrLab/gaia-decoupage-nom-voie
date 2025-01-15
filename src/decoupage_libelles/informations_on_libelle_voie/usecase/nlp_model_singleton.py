import spacy
from decoupage_libelles.config.settings_configuration import settings
import logging


class NLPModelExecution:
    def execute(self, texte):
        nlp_model = NLPModelSingleton.getInstance()
        return nlp_model(texte)


class NLPModelSingleton:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @staticmethod
    def _load_model():
        logging.info("Chargement du modèle SpaCy pour le postagging")
        # Code pour charger le modèle NLP
        return spacy.load(settings.chemin_nlp_modele)
