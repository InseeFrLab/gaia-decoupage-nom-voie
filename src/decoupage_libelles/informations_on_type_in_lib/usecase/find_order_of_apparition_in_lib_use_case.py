from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class FindOrderOfApparitionInLibUseCase:
    def execute(self, infovoie: InfoVoie, type_name: str, occurence: int) -> InformationOnTypeOrdered:
        if infovoie.types_and_positions:
            type_to_find = (type_name, occurence)
            liste_cles = list(infovoie.types_and_positions.keys())

            if type_to_find in liste_cles:
                order_type = liste_cles.index(type_to_find) + 1

                position_start, position_end = infovoie.types_and_positions[type_to_find]

                return InformationOnTypeOrdered(type_name=type_name, order_in_lib=order_type, position_start=position_start, position_end=position_end, occurence=occurence)
