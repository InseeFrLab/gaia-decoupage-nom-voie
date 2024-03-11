from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase


class ComplImmeubleBeforeTypeUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> InfoVoie:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        voie_to_treat_by_compl = None
        voie_to_treat_two_types = None
        if first_type.is_complement and voie_compl.has_type_in_first_pos and voie_compl.has_type_in_second_pos and second_type.type_name in ComplementFinderUseCase.TYPES_COMPLEMENT_IMMEUBLE:
            # 'IMM RES DU SOLEIL RUE DE BRAS'
            # supprimer le type complement devant et repasser à deux types
            voie_compl.label_preproc = voie_compl.label_preproc[1:]
            del voie_compl.types_and_positions[(first_type.type_name, first_type.occurence)]
            voie_compl.types_and_positions = {cle: (valeur[0] - 1, valeur[1] - 1) for cle, valeur in voie_compl.types_and_positions.items()}
            self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

            voie_to_treat_two_types = voie_compl
        else:
            voie_to_treat_by_compl = voie_compl

        return voie_to_treat_by_compl, voie_to_treat_two_types
