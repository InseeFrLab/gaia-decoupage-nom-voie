from injector import inject

from finders.find_type.domain.model.type_finder_object import TypeFinderObject
from finders.find_type.domain.usecase.remove_type_from_lib_and_types_use_case import RemoveTypeFromLibAndTypesUseCase


class RemoveDuplicatesUseCase:
    @inject
    def __init__(self, remove_type_from_lib_and_types_use_case: RemoveTypeFromLibAndTypesUseCase):
        self.remove_type_from_lib_and_types_use_case: RemoveTypeFromLibAndTypesUseCase = remove_type_from_lib_and_types_use_case
    
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        for __, occurence in type_finder_object.voie_big.types_and_positions.keys():
            if occurence > 1:
                has_duplicated_types = True

        if has_duplicated_types:
            types_duplicates = [type_lib for type_lib, occurence in type_finder_object.infolib.types_and_positions if occurence > 1]

            for type_duplicate in types_duplicates:
                dict_two_positions = {'first': type_finder_object.voie_big.types_and_positions[(type_duplicate, 1)],
                                      'second': type_finder_object.voie_big.types_and_positions[(type_duplicate, 2)]}
                dist_positions = dict_two_positions['second'][0] - dict_two_positions['first'][1]

                if dist_positions == 1:
                    type_min_distance = min(dict_two_positions, key=lambda k: dict_two_positions[k][1] - dict_two_positions[k][0])

                    position_start_min, position_end_min = dict_two_positions[type_min_distance]

                    # Supprimer de la liste preproc le type codifié
                    # Supprimer du dictionnaire le type codifié et décaler les positions
                    self.remove_type_from_lib_and_types_use_case.execute(type_finder_object.voie_big,
                                                                position_start_min,
                                                                position_end_min)

                    if type_min_distance == "first":
                        del type_finder_object.voie_big.types_and_positions[(type_duplicate, 1)]
                        type_finder_object.voie_big.types_and_positions[(type_duplicate, 1)] = type_finder_object.voie_big.types_and_positions[(type_duplicate, 2)]
                        del type_finder_object.voie_big.types_and_positions[(type_duplicate, 2)]
                    else:
                        del type_finder_object.voie_big.types_and_positions[(type_duplicate, 2)]
        return type_finder_object