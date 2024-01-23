from typing import Optional


class InfoLib():
    def __init__(
            self,
            label_preproc: list,
            types_and_positions: Optional[dict] = {},
            label_postag: Optional[list] = None,
            ):
        """
        label_preproc (list):
            Libellé de voie preprocessé.
        types_and_positions (dict):
            Types de voie détectés, leur occurence dans le libellé
            et leur position de début et de fin dans le libellé.
            Optionnel : si non renseigné alors il vaut {}.
        label_postag (list):
            Etiquetage morpho-syntaxique du libellé de voie.
            Par défaut None.
        """
        self.label_preproc = label_preproc
        self.types_and_positions = types_and_positions
        self.label_postag = label_postag

    def __eq__(
            self,
            resultat,
            ):
        """
        Teste s'il y a égalité avec l'objet resultat.

        Args:
            resultat (InfoLib)

        Returns:
            (bool)
        """
        return (self.label_preproc == resultat.label_preproc and
                self.types_and_positions == resultat.types_and_positions and
                self.label_postag == resultat.label_postag)

    def nb_types_detected(self):
        return len(self.types_and_positions)

    def has_duplicates(self):
        for __, occurence in self.types_and_positions.keys():
            if occurence > 1:
                return True

    def types_detected(self):
        return [type_lib for type_lib, __ in self.types_and_positions.keys()]

    def sort_types_by_position(self):
        self.types_and_positions = dict(sorted(
                        self.types_and_positions.items(),
                        key=lambda x: x[1][0]
                        ))

    def get_word(self, position: int):
        if len(self.label_preproc) > position:
            return self.label_preproc[position]

    def get_words_between(self, position_start: int, position_end: Optional[int] = None):
        if position_end:
            if len(self.label_preproc) >= position_end:
                return self.label_preproc[position_start:position_end]
        else:
            if len(self.label_preproc) > position_start:
                return self.label_preproc[position_start:]

    def type_after_type(self, type_lib, occurence):
        self.sort_types_by_position()
        list_of_keys = list(self.types_and_positions.keys())
        index_type = list_of_keys.index((type_lib, occurence))
        if index_type < len(list_of_keys)-1:
            type_after = list_of_keys[index_type+1]
            return type_after

    def order_type_in_lib(self, type_order):
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
        if (not self.types_and_positions or
                self.nb_types_detected() < type_order):
            return None, None

        if type_order >= 1:  # 1er ou plus
            position = type_order-1
        elif type_order == -1:  # dernier
            position = type_order

        types_sorted = sorted(self.types_and_positions.items(),
                              key=lambda item: item[1])
        types_sorted = [(type_voie,
                         positions) for (type_voie, __), positions in types_sorted]

        type_to_find, positions = types_sorted[position]
        type_position_in_lib_start, type_position_in_lib_end = positions
        return type_to_find, type_position_in_lib_start, type_position_in_lib_end

    def __repr__(self):
        return f"InfoLib(libelle_preproc={self.label_preproc}, \
types_and_positions={self.types_and_positions}, \
label_postag={self.label_postag})"
