from decoupage_libelles.informations_on_libelle_voie.usecase.nlp_model_singleton import NLPModelExecution
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class ApplyPostaggingUseCase:
    def __init__(self, nlp_model_execution: NLPModelExecution = NLPModelExecution()) -> None:
        self.nlp_model_execution = nlp_model_execution

    def execute(self, infovoie: InfoVoie) -> InfoVoie:
        if not infovoie.label_postag:
            texte = " ".join(infovoie.label_preproc).lower()
            doc = self.nlp_model_execution.execute(texte)

            # Utiliser une compréhension de liste pour extraire les pos_
            infovoie.label_postag = [word.pos_ for word in doc]
        return infovoie
