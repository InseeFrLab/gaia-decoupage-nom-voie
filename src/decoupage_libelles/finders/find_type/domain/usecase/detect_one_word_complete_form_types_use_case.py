from finders.find_type.domain.model.type_finder_object import TypeFinderObject


class DetectOneWordCompleteFormTypesUseCase:
    def execute(self,
                type_detect: str,
                type_lib: str,
                type_finder_object: TypeFinderObject) -> TypeFinderObject:
            pos_type = [i for i, mot in enumerate(type_finder_object.voie_sep) if mot == type_lib]
            for pos in pos_type:
                positions = (pos, pos)
                if type_detect not in type_finder_object.infolib.types_detected():
                    type_finder_object.infolib.types_and_positions[(type_detect, 1)] = positions
                else:
                    type_finder_object.infolib.types_and_positions[(type_detect, 2)] = positions
            return type_finder_object