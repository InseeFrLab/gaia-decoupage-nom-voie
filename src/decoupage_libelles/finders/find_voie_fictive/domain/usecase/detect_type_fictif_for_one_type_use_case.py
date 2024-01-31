from typing import List

from voie_classes.decoupage_voie import DecoupageVoie
from constants.constant_lists import list_fictive


class DetectTypeFictifForOneTypeUseCase:
    def execute(self,
                voie: DecoupageVoie,
                liste_voie_commun: List[str]):
            # si RUE A on garde type 'RUE' et libellé 'A'. Si il y a qlq chose avant 'RUE',
            # alors ca passe en voie fictive

            for type_voie in liste_voie_commun:
                first_type, __, __ = voie.infolib.order_type_in_lib(1)
                if (first_type == type_voie and
                        voie.has_type_in_penultimate_pos(1) and
                        voie.word_before_type(1) and
                        voie.word_after_type(1) in list_fictive+['L', 'D', 'A']):
                    return voie