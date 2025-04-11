from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case import DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class RemoveWrongDetectedCodesUseCase:
    def __init__(
        self,
        determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case: DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase = DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
    ):
        self.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case: DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase = (
            determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case
        )
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        # Supprime les types codifiés détectés à tord
        # ANC CHEM --> ANCIEN CHEMIN et CHEMINEMENT --> Ancien chemin et on ne retire rien du libellé
        voie_big = type_finder_object.voie_big
        types_and_positions = voie_big.types_and_positions
        label_preproc = voie_big.label_preproc

        types_to_delete = []
        i = 1
        type_i = None
        while i < len(types_and_positions):
            if not type_i:
                type_i = self.generate_information_on_type_ordered_use_case.execute(voie_big, i)
            type_i1 = self.generate_information_on_type_ordered_use_case.execute(voie_big, i + 1)

            type_i_name = type_i.type_name
            type_i1_name = type_i1.type_name

            if type_i_name != type_i1_name:
                dict_two_types = {
                    type_i_name: (type_i.position_start, type_i.position_end, type_i.occurence),
                    type_i1_name: (type_i1.position_start, type_i1.position_end, type_i1.occurence)
                    }

                type_min, type_max = self.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case.execute(type_i_name, type_i1_name)

                position_start_min, __, occurence_min = dict_two_types[type_min]
                position_start_max, position_end_max, __ = dict_two_types[type_max]

                if (
                    position_start_max <= position_start_min <= position_end_max
                    and label_preproc[position_start_min] in label_preproc[position_start_max : position_end_max + 1]
                ):
                    types_to_delete.append((type_min, occurence_min))
                    if type_i_name == type_max:
                        i += 1
                    else:
                        type_i = type_i1
                        i += 1
                else:
                    type_i = None
                    i += 1
            else:
                type_i = None
                i += 1

        if types_to_delete:
            for type_to_delete in list(set(types_to_delete)):
                del type_finder_object.voie_big.types_and_positions[type_to_delete]

        return type_finder_object
