from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class TypeAfterTypeUseCase:
    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        infovoie.types_and_positions = dict(sorted(infovoie.types_and_positions.items(), key=lambda x: x[1][0]))
        list_of_keys = list(infovoie.types_and_positions.keys())
        index_type = list_of_keys.index((information_on_type_ordered.type_name, information_on_type_ordered.occurence))
        if index_type < len(list_of_keys) - 1:
            type_after = list_of_keys[index_type + 1]
            information_on_type_ordered.type_after = type_after

        return information_on_type_ordered
