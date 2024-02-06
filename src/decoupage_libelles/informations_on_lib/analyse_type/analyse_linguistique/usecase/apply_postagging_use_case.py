from informations_on_lib.analyse_type.analyse_linguistique.usecase.nlp_model_singleton import NLPModelSingleton
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib

class ApplyPostaggingUseCase:
    def execute(self, infolib: InfoLib) -> InfoLib:
        nlp_model = NLPModelSingleton.getInstance()
        texte = (' ').join(infolib.label_preproc).lower()
        doc = nlp_model(texte)
        texte_tokense = []
        for word in doc:
            texte_tokense.append(word.pos_)
        infolib.label_postag = texte_tokense
        return infolib