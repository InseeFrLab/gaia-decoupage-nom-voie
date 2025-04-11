from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class UpdateOccurencesByOrderOfApparitionUseCase:
    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        type_finder_object.voie_big.types_and_positions = dict(sorted(type_finder_object.voie_big.types_and_positions.items(), key=lambda x: x[1][0]))
        sorted_keys = type_finder_object.voie_big.types_and_positions.keys()

        new_types_and_positions = {}
        occurrences = {}

        for key in sorted_keys:
            type_voie, __ = key
            if type_voie in occurrences:
                occurrences[type_voie] += 1
            else:
                occurrences[type_voie] = 1

            new_key = (type_voie, occurrences[type_voie])
            new_types_and_positions[new_key] = type_finder_object.voie_big.types_and_positions[key]

        type_finder_object.voie_big.types_and_positions = new_types_and_positions
        return type_finder_object
