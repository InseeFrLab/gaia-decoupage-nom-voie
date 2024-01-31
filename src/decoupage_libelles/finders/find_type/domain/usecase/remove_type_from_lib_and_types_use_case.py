from voie_classes.informations_on_libelle import InfoLib


class RemoveTypeFromLibAndTypesUseCase:

    def execute(self,
                infolib: InfoLib, 
                position_start_min: int,
                position_end_min: int):
        # Supprimer de la liste preproc le type codifié
        before_type_min = infolib.label_preproc[:position_start_min]
        after_type_min = infolib.label_preproc[position_end_min+1:]

        infolib.label_preproc = before_type_min + after_type_min

        # Supprimer du dictionnaire le type codifié et décaler les positions
        nb_words_in_type_min = position_end_min - position_start_min + 1

        for type_lib, positions in list(infolib.types_and_positions.items()):
            position_start, position_end = positions
            if position_start > position_end_min:
                position_start -= nb_words_in_type_min
                position_end -= nb_words_in_type_min
                infolib.types_and_positions[type_lib] = (position_start,
                                                        position_end)
        return infolib