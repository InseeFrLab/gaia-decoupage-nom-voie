from typing import Optional

from voie_classes.informations_on_libelle import InfoLib


class Voie:
    """ """

    def __init__(
        self,
        label_raw: str,
        infolib: Optional[InfoLib] = None,
    ):
        """
        Constructor.

        Args:
            label_raw (str):
                Libellé de voie dans la base de données.
            infolib (InfoLib):
                Informations sur le libellé.
        """
        self.label_raw = label_raw
        self.infolib = infolib
        self.type_assigned = None
        self.label_assigned = None
        self.compl_assigned = None
        self.num_assigned = None

    def __eq__(
        self,
        resultat,
    ):
        # Tester s'il y a égalité avec l'objet resultat.
        return (
            self.label_raw == resultat.label_raw
            and self.infolib == self.infolib
            and self.type_assigned == resultat.type_assigned
            and self.label_assigned == resultat.label_assigned
            and self.compl_assigned == resultat.compl_assigned
            and self.num_assigned == resultat.num_assigned
        )
