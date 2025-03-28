from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.ponctuation.usecase.separate_complementary_part_use_case import SeparateComplementaryPartUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.basic_preprocess_words_use_case import BasicPreprocessWordsUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.synonyms_dilatation_use_case import SynonymsDilatationUseCase


class PonctuationPreprocessorUseCase:
    PONCTUATIONS = ["-", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"', "«", "»", "*", "/", "\\", "°", "|", "_"]

    def __init__(
        self,
        separate_complementary_part_use_case: SeparateComplementaryPartUseCase = SeparateComplementaryPartUseCase(),
        basic_preprocess_words_use_case: BasicPreprocessWordsUseCase = BasicPreprocessWordsUseCase(),
        separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = SeparateWordsWithApostropheAndSupressPonctuationUseCase(),
        suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = SuppressPonctuationInWordsUseCase(),
        synonyms_dilatation_use_case: SynonymsDilatationUseCase = SynonymsDilatationUseCase(),
    ):
        self.separate_complementary_part_use_case: SeparateComplementaryPartUseCase = separate_complementary_part_use_case
        self.basic_preprocess_words_use_case: BasicPreprocessWordsUseCase = basic_preprocess_words_use_case
        self.separate_words_with_apostrophe_and_supress_ponctuation_use_case: SeparateWordsWithApostropheAndSupressPonctuationUseCase = separate_words_with_apostrophe_and_supress_ponctuation_use_case
        self.suppress_ponctuation_in_words_use_case: SuppressPonctuationInWordsUseCase = suppress_ponctuation_in_words_use_case
        self.synonyms_dilatation_use_case: SynonymsDilatationUseCase = synonyms_dilatation_use_case

    def execute(self, voie_obj: InfoVoie) -> InfoVoie:
        voie_obj = self.separate_complementary_part_use_case.execute(voie_obj)
        voie_obj = self.basic_preprocess_words_use_case.execute(voie_obj)
        chaine_decoupee = self.separate_words_with_apostrophe_and_supress_ponctuation_use_case.execute(voie_obj.label_raw, PonctuationPreprocessorUseCase.PONCTUATIONS)
        new_label_preproc = self.suppress_ponctuation_in_words_use_case.execute(chaine_decoupee, PonctuationPreprocessorUseCase.PONCTUATIONS)
        label_preproc_dilated = self.synonyms_dilatation_use_case.execute(new_label_preproc)
        voie_obj.label_preproc = label_preproc_dilated
        return voie_obj
