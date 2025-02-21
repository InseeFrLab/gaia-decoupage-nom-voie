from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_second_pos_use_case import ComplTypeInFirstOrSecondPosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_middle_pos_use_case import ComplTypeInFirstOrMiddlePosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_last_pos_use_case import ComplTypeInFirstOrLastPosUseCase
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase


class HandleOneTypeComplUseCase:
    def __init__(
        self,
        compl_type_in_first_or_second_pos_use_case: ComplTypeInFirstOrSecondPosUseCase = ComplTypeInFirstOrSecondPosUseCase(),
        compl_type_in_first_or_middle_pos_use_case: ComplTypeInFirstOrMiddlePosUseCase = ComplTypeInFirstOrMiddlePosUseCase(),
        compl_type_in_first_or_last_pos_use_case: ComplTypeInFirstOrLastPosUseCase = ComplTypeInFirstOrLastPosUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
    ):
        self.compl_type_in_first_or_second_pos_use_case: ComplTypeInFirstOrSecondPosUseCase = compl_type_in_first_or_second_pos_use_case
        self.compl_type_in_first_or_middle_pos_use_case: ComplTypeInFirstOrMiddlePosUseCase = compl_type_in_first_or_middle_pos_use_case
        self.compl_type_in_first_or_last_pos_use_case: ComplTypeInFirstOrLastPosUseCase = compl_type_in_first_or_last_pos_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = suppress_article_in_first_place_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.suppress_article_in_first_place_use_case.execute(voie_compl)
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        if voie_compl.has_type_in_first_pos:
            if voie_compl.has_type_in_second_pos:
                return self.compl_type_in_first_or_second_pos_use_case.execute(voie_compl)

            elif voie_compl.has_type_in_last_pos:
                return self.compl_type_in_first_or_last_pos_use_case.execute(voie_compl)

            else:
                return self.compl_type_in_first_or_middle_pos_use_case.execute(voie_compl)

        else:
            # 'BEAU PAVILLON DE LA FORET'
            # lib
            return self.assign_lib_use_case.execute(voie_compl)
