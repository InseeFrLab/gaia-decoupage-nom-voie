from voie_classes.voie import Voie
from constants.constant_lists import liste_postag
from utils.utils_for_lists import is_last_position
from utils.nlp_model_singleton import NLPModelSingleton


class AnalyseLinguistique(Voie):
    """
    Analyse la structure grammatico-syntaxique du libellé.
    """
    def postag_before_type(self, type_order):
        """
        Retourne l'étiquette grammatico-syntaxique du mot précédent
        le type.

        Args:
            type_order (int):
                Ordre d'apparition du type dans le libellé.
                1 = 1er, 2 = 2nd...
                -1 = dernier.

        Returns:
            (str)
        """
        if not self.infolib.label_postag:
            self.apply_postagging()
        __, position_type_in_lib_start, __ = self.infolib.order_type_in_lib(type_order)
        return self.infolib.label_postag[position_type_in_lib_start-1]

    def has_adj_det_before_type(self, type_order):
        postag = self.postag_before_type(type_order)
        return postag in liste_postag

    def has_num_before_type(self, type_order):
        postag = self.postag_before_type(type_order)
        return postag == 'NUM'

    def word_before_type(self, type_order):
        __, position_type_in_lib_start, __ = self.infolib.order_type_in_lib(type_order)
        if position_type_in_lib_start or position_type_in_lib_start > 0:
            index_word_before = position_type_in_lib_start - 1
            return self.infolib.label_preproc[index_word_before]

    def word_after_type(self, type_order):
        __, __, position_type_in_lib_end = self.infolib.order_type_in_lib(type_order)
        if (position_type_in_lib_end or
                not is_last_position(self.infolib.label_preproc, position_type_in_lib_end)):
            index_word_after = position_type_in_lib_end + 1
            return self.infolib.label_preproc[index_word_after]

    def apply_postagging(self):
        nlp_model = NLPModelSingleton.getInstance()
        texte = (' ').join(self.infolib.label_preproc).lower()
        doc = nlp_model(texte)
        texte_tokense = []
        for word in doc:
            texte_tokense.append(word.pos_)
        self.infolib.label_postag = texte_tokense
