from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase


class KeepTypesWithoutArticleAdjBeforeUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case

    def execute(self, voie: InfoVoie) -> InfoVoie:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=True)

        types_and_positions = voie.types_and_positions.copy()

        for key, (position_start, __) in voie.types_and_positions.items():
            if position_start > 0:
                index_word_before = position_start - 1
                postag_before = voie.label_postag[index_word_before]
                word_before = voie.label_preproc[index_word_before]
                if postag_before in PostagBeforeTypeUseCase.POSTAG and word_before != "A" or word_before in ["DIT", "DITE"]:
                    del types_and_positions[key]

        voie.types_and_positions = types_and_positions

        return voie
