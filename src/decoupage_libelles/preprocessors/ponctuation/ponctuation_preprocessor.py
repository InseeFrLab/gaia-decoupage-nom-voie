from injector import inject

from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib
from preprocessors.ponctuation.separate_words_with_apostrophe_and_supress_ponctuation import SeparateWordsWithApostropheAndSupressPonctuation
from preprocessors.ponctuation.suppress_ponctuation_in_words import SuppressPonctuationInWords


class PonctuationPreprocessor:
    @inject
    def __init__(self, separate_pontuation_and_words_with_apostrophe: SeparateWordsWithApostropheAndSupressPonctuation, suppress_ponctuation_in_words: SuppressPonctuationInWords):
        self.separate_pontuation_and_words_with_apostrophe: SeparateWordsWithApostropheAndSupressPonctuation = separate_pontuation_and_words_with_apostrophe
        self.suppress_ponctuation_in_words: SuppressPonctuationInWords = suppress_ponctuation_in_words

    def execute(self, voie_obj: Voie, ponctuations: list) -> Voie:
        chaine_decoupee = self.separate_pontuation_and_words_with_apostrophe.execute(voie_obj.label_raw, ponctuations)
        new_label_preproc = self.suppress_ponctuation_in_words.execute(chaine_decoupee, ponctuations)
        voie_obj.infolib = InfoLib(new_label_preproc)
        return voie_obj
