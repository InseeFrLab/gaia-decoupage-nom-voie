from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class RemoveTypeFromLibUseCase:
    """
    Supprime un type détecté de label_preproc et décale les positions
    de tous les types détectés situés après lui.
    """

    def execute(self, infovoie: InfoVoie, pos_start: int, pos_end: int) -> InfoVoie:
        nb_mots = pos_end - pos_start + 1

        # Retirer les mots du label prétraité
        infovoie.label_preproc = (
            infovoie.label_preproc[:pos_start] + infovoie.label_preproc[pos_end + 1 :]
        )

        # Décaler les positions des types situés après la suppression
        infovoie.types_and_positions = {
            key: (s - nb_mots if s > pos_end else s, e - nb_mots if e > pos_end else e)
            for key, (s, e) in infovoie.types_and_positions.items()
        }

        return infovoie
