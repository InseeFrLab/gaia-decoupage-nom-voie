from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.remove_type_from_lib_use_case import RemoveTypeFromLibUseCase


class RemoveDuplicatesUseCase:
    """
    Gère le cas "ART ANCIENNE ROUTE" où deux types adjacents sont détectés
    alors que l'un contient l'autre (ex: ROUTE et ANCIENNE ROUTE).

    Quand deux occurrences du même canonique sont détectées à des positions
    consécutives (distance == 1), on supprime la plus courte.
    """

    def __init__(
        self,
        remove_type_from_lib_use_case: RemoveTypeFromLibUseCase = RemoveTypeFromLibUseCase(),
    ):
        self.remove_type_from_lib = remove_type_from_lib_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        positions = type_finder_object.voie_big.types_and_positions
        doublons = {t for t, occ in positions if occ > 1}

        for canonique in doublons:
            pos1 = positions.get((canonique, 1))
            pos2 = positions.get((canonique, 2))
            if pos1 is None or pos2 is None:
                continue

            # Adjacents ?
            if pos2[0] - pos1[1] != 1:
                continue

            # Supprimer le plus court (moins de mots)
            len1 = pos1[1] - pos1[0]
            len2 = pos2[1] - pos2[0]

            if len1 <= len2:
                type_finder_object.voie_big = self.remove_type_from_lib.execute(
                    type_finder_object.voie_big, pos1[0], pos1[1]
                )
                del positions[(canonique, 1)]
                # Renommer l'occurrence 2 en 1
                positions[(canonique, 1)] = positions.pop((canonique, 2))
            else:
                type_finder_object.voie_big = self.remove_type_from_lib.execute(
                    type_finder_object.voie_big, pos2[0], pos2[1]
                )
                del positions[(canonique, 2)]

        return type_finder_object
