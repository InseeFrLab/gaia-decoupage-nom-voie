from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class DetectCodifiedTypesUseCase:
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        for code_type in type_finder_object.type_data.codes:
            lib_type = type_finder_object.type_data.code2lib[code_type]
            if code_type in type_finder_object.voie_sep:
                pos_type = [i for i, mot in enumerate(type_finder_object.voie_sep) if mot == code_type]
                for position in pos_type:
                    positions = (position, position)
                    types_detected = [type_lib for type_lib, __ in type_finder_object.voie_big.types_and_positions.keys()]
                    if lib_type not in types_detected:
                        type_finder_object.voie_big.types_and_positions[(lib_type, 1)] = positions
                    else:
                        type_finder_object.voie_big.types_and_positions[(lib_type, 2)] = positions
        return type_finder_object
