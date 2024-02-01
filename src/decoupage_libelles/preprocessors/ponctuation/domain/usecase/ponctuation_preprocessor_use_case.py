from injector import inject

from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib
from preprocessors.ponctuation.domain.use_case.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from preprocessors.ponctuation.domain.use_case.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase


class PonctuationPreprocessorUseCase:

    PONCTUATIONS = ['-', '.', ',', ';', ':', '!', '?', '(', ')', '[', ']', '{',
                    '}', "'", '"', '«', '»', '*', '/']

    @inject
    def __init__(self,
                 separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase,
                 suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase):
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = separate_words_with_apostrophe_and_supress_ponctuation_use_case
        self.suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = suppress_ponctuation_in_words_use_case

    def execute(self, voie_obj: Voie) -> Voie:
        chaine_decoupee = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(voie_obj.label_raw, PonctuationPreprocessorUseCase.PONCTUATIONS)
        new_label_preproc = self.suppress_ponctuation_in_words_use_case.execute(chaine_decoupee, PonctuationPreprocessorUseCase.PONCTUATIONS)
        voie_obj.infolib = InfoLib(new_label_preproc)
        return voie_obj
