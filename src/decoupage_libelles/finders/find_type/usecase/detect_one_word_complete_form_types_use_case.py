from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class DetectOneWordCompleteFormTypesUseCase:
    def execute(self, type_detect: str, type_lib: str, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        pos_type = [i for i, mot in enumerate(type_finder_object.voie_sep) if mot == type_lib]
        for pos in pos_type:
            positions = (pos, pos)
            types_detected = [type_lib for type_lib, __ in type_finder_object.voie_big.types_and_positions.keys()]
            position_index = 1 if type_detect not in types_detected else 2
            type_finder_object.voie_big.types_and_positions[(type_detect, position_index)] = positions
        return type_finder_object
