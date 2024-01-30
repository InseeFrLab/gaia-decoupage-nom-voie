from injector import inject

from finders.find_type.domain.model.type_finder_object import TypeFinderObject
from finders.find_type.domain.use_case.remove_type_from_lib_and_types import RemoveTypeFromLibAndTypes



class RemoveDuplicates:
    @inject
    def __init__(self, remove_type_from_lib_and_types: RemoveTypeFromLibAndTypes):
        self.remove_type_from_lib_and_types: RemoveTypeFromLibAndTypes = remove_type_from_lib_and_types
    
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        if type_finder_object.infolib.has_duplicates():
            types_duplicates = [type_lib for type_lib, occurence in type_finder_object.infolib.types_and_positions if occurence > 1]

            for type_duplicate in types_duplicates:
                dict_two_positions = {'first': type_finder_object.infolib.types_and_positions[(type_duplicate, 1)],
                                      'second': type_finder_object.infolib.types_and_positions[(type_duplicate, 2)]}
                dist_positions = dict_two_positions['second'][0] - dict_two_positions['first'][1]

                if dist_positions == 1:
                    type_min_distance = min(dict_two_positions, key=lambda k: dict_two_positions[k][1] - dict_two_positions[k][0])

                    position_start_min, position_end_min = dict_two_positions[type_min_distance]

                    # Supprimer de la liste preproc le type codifié
                    # Supprimer du dictionnaire le type codifié et décaler les positions
                    self.remove_type_from_lib_and_types.execute(type_finder_object.infolib,
                                                                position_start_min,
                                                                position_end_min)

                    if type_min_distance == "first":
                        del type_finder_object.infolib.types_and_positions[(type_duplicate, 1)]
                        type_finder_object.infolib.types_and_positions[(type_duplicate, 1)] = type_finder_object.infolib.types_and_positions[(type_duplicate, 2)]
                        del type_finder_object.infolib.types_and_positions[(type_duplicate, 2)]
                    else:
                        del type_finder_object.infolib.types_and_positions[(type_duplicate, 2)]
        return type_finder_object