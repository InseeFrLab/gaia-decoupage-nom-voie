from injector import inject

from finders.find_type.domain.model.type_finder_object import TypeFinderObject
from finders.find_type.domain.usecase.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case import DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase

class RemoveWrongDetectedCodesUseCase:
    @inject
    def __init__(self, determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case: DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase):
        self.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case: DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase = determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        # Supprime les types codifiés détectés à tord
        # (ex : ANC CHEM --> ANCIEN CHEMIN et CHEMINEMENT)
        for i in range(1, len(type_finder_object.voie_big.types_and_positions)):
            dict_two_types = {}

            type_i, position_start_i, position_end_i = type_finder_object.voie_big.order_type_in_lib(i)
            type_i1, position_start_i1, position_end_i1 = type_finder_object.voie_big.order_type_in_lib(i+1)

            dict_two_types[type_i] = (position_start_i, position_end_i)
            dict_two_types[type_i1] = (position_start_i1, position_end_i1)

            type_min, type_max = self.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case.execute(type_i, type_i1)

            position_start_min, __ = dict_two_types[type_min]
            position_start_max, position_end_max = dict_two_types[type_max]

            if position_start_min in list(range(position_start_max, position_end_max + 1)):
                del type_finder_object.voie_big.types_and_positions[(type_min, 1)]

        return type_finder_object