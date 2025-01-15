import spacy
from decoupage_libelles.config.settings_configuration import settings
import logging
import torch

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
        chemin_modele = settings.chemin_nlp_modele
        try:
            if chemin_modele.endswith('.pt') or chemin_modele.endswith('.pth'):
                model_state_dict = torch.load(chemin_modele, map_location='cpu', weights_only=True)
            else:
                return spacy.load(chemin_modele)
        except Exception as e:
            logging.error(f"Erreur lors du chargement du modèle : {e}")
            raise
