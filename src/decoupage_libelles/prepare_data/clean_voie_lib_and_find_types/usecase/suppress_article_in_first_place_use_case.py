from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib


class SuppressArticleInFirstPlaceUseCase:
    def __init__(self, order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib()):
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case

    def execute(self, voie: InfoVoie) -> InfoVoie:
        first_word = voie.label_preproc[0]
        type_ordered_first = self.order_type_in_lib_use_case.execute(voie, 1)
        first_type_in_second_pos = True if type_ordered_first and type_ordered_first.position_start == 1 else False
        if first_type_in_second_pos and first_word in ['LE', 'LA', 'L', 'LES']:
            new_label_preproc = voie.label_preproc[1:]
            voie.label_preproc = new_label_preproc

            new_types_and_positions = {}
            for key, value in voie.types_and_positions.items():  # a tester
                deb, fin = value
                new_types_and_positions[key] = (deb-1, fin-1)
            voie.types_and_positions = new_types_and_positions

            # new_label_raw = voie.label_raw[len(first_word)+1:]
            # voie.label_raw = new_label_raw

        return voie
