from informations_on_libelle_voie.domain.usecase.nlp_model_singleton import NLPModelSingleton
from informations_on_libelle_voie.domain.model.infovoie import InfoVoie

class ApplyPostaggingUseCase:
    def execute(self, infovoie: InfoVoie) -> InfoVoie:
        if not infovoie.label_postag:
            nlp_model = NLPModelSingleton.getInstance()
            texte = (' ').join(infovoie.label_preproc).lower()
            doc = nlp_model(texte)
            texte_tokense = []
            for word in doc:
                texte_tokense.append(word.pos_)
            infovoie.label_postag = texte_tokense
        
        return infovoie