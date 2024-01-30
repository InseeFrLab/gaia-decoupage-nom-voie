from finders.find_type.domain.model.type_finder_object import TypeFinderObject
from utils.type_finder_utils import min_and_max_count_espaces_in_strs

class RemoveWrongDetectedCodes:
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        # Supprime les types codifiés détectés à tord
        # (ex : ANC CHEM --> ANCIEN CHEMIN et CHEMINEMENT)
        for i in range(1, len(type_finder_object.infolib.types_and_positions)):
            dict_two_types = {}

            type_i, position_start_i, position_end_i = type_finder_object.infolib.order_type_in_lib(i)
            type_i1, position_start_i1, position_end_i1 = type_finder_object.infolib.order_type_in_lib(i+1)

            dict_two_types[type_i] = (position_start_i, position_end_i)
            dict_two_types[type_i1] = (position_start_i1, position_end_i1)

            type_min, type_max = min_and_max_count_espaces_in_strs.execute(type_i, type_i1)

            position_start_min, __ = dict_two_types[type_min]
            position_start_max, position_end_max = dict_two_types[type_max]

            if position_start_min in list(range(position_start_max, position_end_max + 1)):
                del type_finder_object.infolib.types_and_positions[(type_min, 1)]

        return type_finder_object