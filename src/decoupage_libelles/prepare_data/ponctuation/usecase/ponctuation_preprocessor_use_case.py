from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.ponctuation.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase


class PonctuationPreprocessorUseCase:
    PONCTUATIONS = ["-", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"', "«", "»", "*", "/"]

    def __init__(
        self,
        separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = SeparateWordsWithApostropheAndSupressPonctuationUseCase(),
        suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = SuppressPonctuationInWordsUseCase(),
    ):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = separate_words_with_apostrophe_and_supress_ponctuation_use_case
        self.suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = suppress_ponctuation_in_words_use_case

    def execute(self, voie_obj: InfoVoie) -> InfoVoie:
        chaine_decoupee = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(voie_obj.label_raw, PonctuationPreprocessorUseCase.PONCTUATIONS)
        new_label_preproc = self.suppress_ponctuation_in_words_use_case.execute(chaine_decoupee, PonctuationPreprocessorUseCase.PONCTUATIONS)
        voie_obj.label_preproc = new_label_preproc
        return voie_obj
