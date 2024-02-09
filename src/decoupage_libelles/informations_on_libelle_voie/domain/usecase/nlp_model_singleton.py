import fr_dep_news_trf


class NLPModelSingleton:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @staticmethod
    def _load_model():
        print('Chargement du modèle SpaCy pour le postagging')
        # Code pour charger le modèle NLP
        return fr_dep_news_trf.load()
