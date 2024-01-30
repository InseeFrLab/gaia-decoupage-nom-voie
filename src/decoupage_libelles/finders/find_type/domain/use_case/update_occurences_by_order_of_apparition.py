from finders.find_type.domain.model.type_finder_object import TypeFinderObject


class UpdateOccurencesByOrderOfApparition:

    def execute(self,
                 type_finder_object: TypeFinderObject) -> TypeFinderObject:
            type_finder_object.infolib.sort_types_by_position()
            sorted_keys = type_finder_object.infolib.types_and_positions.keys()

            new_types_and_positions = {}
            occurrences = {}

            for key in sorted_keys:
                type_voie = key[0]
                if type_voie in occurrences:
                    occurrences[type_voie] += 1
                else:
                    occurrences[type_voie] = 1

                new_key = (type_voie, occurrences[type_voie])
                new_types_and_positions[new_key] = type_finder_object.infolib.types_and_positions[key]

            type_finder_object.infolib.types_and_positions = new_types_and_positions
            return type_finder_object