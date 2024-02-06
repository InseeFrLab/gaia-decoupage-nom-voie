from voie.informations_on_libelle import InfoLib
from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class OrderTypeInLib:
     
    def execute(self, infolib: InfoLib, type_order: int) -> InformationOnTypeOrdered:
            """
            Retourne le type et la position de début et de fin du type
            dans le libellé sachant son ordre d'apparition dans le libellé.

            Args:
                type_order (int):
                    Ordre d'apparition du type dans le libellé.
                    1 = 1er, 2 = 2nd...
                    -1 = dernier.

            Returns:
                type_to_find (str) :
                    Le type recherché.
                type_position_in_lib_start (int) :
                    La position de début du type dans la liste de mots du libellé preprocessé.
                type_position_in_lib_end (int) :
                    La position de fin du type dans la liste de mots du libellé preprocessé.
            """
            nb_types_detected = len(infolib.types_and_positions)
            if not infolib.types_and_positions or nb_types_detected < type_order:
                return None

            if type_order >= 1:  # 1er ou plus
                position = type_order - 1
            elif type_order == -1:  # dernier
                position = type_order

            types_sorted = sorted(infolib.types_and_positions.items(), key=lambda item: item[1])
            types_sorted = [(type_voie, positions) for (type_voie, __), positions in types_sorted]

            type_to_find, positions = types_sorted[position]
            type_position_in_lib_start, type_position_in_lib_end = positions

            type_ordered = InformationOnTypeOrdered(type_name=type_to_find,
                                                    order_in_lib=type_order,
                                                    position_start=type_position_in_lib_start,
                                                    position_end=type_position_in_lib_end)

            return type_ordered