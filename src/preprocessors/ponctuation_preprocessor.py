import re

from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib


class PonctuationPreprocessor():

    def __init__(
            self,
            voie_obj: Voie,
            ponctuations: list):
        self.voie_obj = voie_obj
        self.ponctuations = ponctuations
        self.new_voie_traitee = None
        self.new_label_preproc = None

    def separate_ponctuation_and_words_with_apostrophe(self):
        voie = self.voie_obj.label_raw
        # séparer le libellé en liste de mots
        new_voie = voie.split(' ')
        # séparer en deux les mots avec apostrophe
        new_voie = [mot.split("'") for mot in new_voie]
        new_voie = [mot for item in new_voie for mot in item]
        new_voie = [segment for mot in new_voie for segment in re.split(r'(\d+)', mot) if segment]
        # retirer les ponctuations seules et les espaces en trop
        self.new_voie_traitee = [item for item in new_voie if (item not in self.ponctuations and
                                                               item != "")]

    def suppress_ponctuation_in_words(self):
        # retirer la ponctuation contenue dans un mot
        self.new_label_preproc = self.new_voie_traitee[:]
        for j, mot in enumerate(self.new_voie_traitee):
            mot_sep = re.split(r"([-.,;:!?(){}*/])", mot)
            mot_sep = [ss for ss in mot_sep if ss.strip()]
            new_mot = ('').join([ss for ss in mot_sep if ss not in self.ponctuations])
            self.new_label_preproc[j] = new_mot

    def run(self):
        self.separate_ponctuation_and_words_with_apostrophe()
        self.suppress_ponctuation_in_words()
        infolib = InfoLib(self.new_label_preproc)
        self.voie_obj.infolib = infolib
        return self.voie_obj
