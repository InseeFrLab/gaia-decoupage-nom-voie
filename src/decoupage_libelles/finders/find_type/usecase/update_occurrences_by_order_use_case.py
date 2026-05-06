from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class UpdateOccurrencesByOrderUseCase:
    """
    Réordonne et renumérote les occurrences de chaque type canonique
    par ordre d'apparition dans le libellé (position croissante).
    """

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        # Trier par position de début
        sorted_items = sorted(
            type_finder_object.voie_big.types_and_positions.items(),
            key=lambda x: x[1][0],
        )

        new_positions = {}
        counters: dict = {}
        for (canonique, _), positions in sorted_items:
            counters[canonique] = counters.get(canonique, 0) + 1
            new_positions[(canonique, counters[canonique])] = positions

        type_finder_object.voie_big.types_and_positions = new_positions
        return type_finder_object
