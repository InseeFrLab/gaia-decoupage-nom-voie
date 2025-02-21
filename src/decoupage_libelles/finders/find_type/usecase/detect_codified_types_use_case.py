from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class DetectCodifiedTypesUseCase:
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        for code_type in type_finder_object.type_data.codes:
            lib_type = type_finder_object.type_data.code2lib[code_type]
            if code_type in type_finder_object.voie_sep:
                # Trouver les positions de chaque code_type dans voie_sep
                pos_type = [i for i, mot in enumerate(type_finder_object.voie_sep) if mot == code_type]
                for position in pos_type:
                    positions = (position, position)
                    # Vérifier si le lib_type est déjà détecté
                    types_detected = [type_lib for type_lib, __ in type_finder_object.voie_big.types_and_positions.keys()]
                    position_index = 1 if lib_type not in types_detected else 2
                    # Ajouter les positions au dictionnaire types_and_positions
                    type_finder_object.voie_big.types_and_positions[(lib_type, position_index)] = positions
        return type_finder_object
