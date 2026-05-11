from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.finders.voie_fictive.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from decoupage_libelles.preprocessing.pipeline.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase


class HandleNoTypeComplUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_compl_use_case: AssignLibComplUseCase = AssignLibComplUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_compl_use_case: AssignLibComplUseCase = assign_lib_compl_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = suppress_article_in_first_place_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        self.suppress_article_in_first_place_use_case.execute(voie_compl)
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        if first_type.is_in_middle_position and not first_type.has_adj_det_before:
            if first_type.word_after in VoieFictiveFinderUseCase.LISTE_FICTIVE or first_type.is_escalier_or_appartement:
                # 'LE TILLET BAT A'
                # lib + compl
                return self.assign_lib_compl_use_case.execute(voie_compl)
            else:
                # 'LE TILLET BAT ERNEST RENAN'
                # compl + type + lib
                return self.assign_compl_type_lib_use_case.execute(voie_compl, first_type)

        else:
            if first_type.is_escalier_or_appartement:
                # 'APPARTEMENT JEAN LAMOUR'
                # lib
                return self.assign_lib_use_case.execute(voie_compl)
            else:
                # 'BAT JEAN LAMOUR'
                # type + lib
                return self.assign_type_lib_use_case.execute(voie_compl, first_type)
