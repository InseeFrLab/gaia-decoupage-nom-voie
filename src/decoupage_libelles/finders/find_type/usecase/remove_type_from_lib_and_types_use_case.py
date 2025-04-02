from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class RemoveTypeFromLibAndTypesUseCase:
    def execute(self, infovoie: InfoVoie, position_start_min: int, position_end_min: int) -> InfoVoie:
        # Supprimer de la liste preproc le type codifié
        before_type_min = infovoie.label_preproc[:position_start_min]
        after_type_min = infovoie.label_preproc[position_end_min + 1 :]

        infovoie.label_preproc = before_type_min + after_type_min

        # Supprimer du dictionnaire le type codifié et décaler les positions
        nb_words_in_type_min = position_end_min - position_start_min + 1
        new_types_and_positions = infovoie.types_and_positions
        for type_lib, positions in list(infovoie.types_and_positions.items()):
            position_start, position_end = positions
            if position_start > position_end_min:
                position_start -= nb_words_in_type_min
                position_end -= nb_words_in_type_min
                new_types_and_positions[type_lib] = (position_start, position_end)

        infovoie.types_and_positions = new_types_and_positions
        return infovoie
