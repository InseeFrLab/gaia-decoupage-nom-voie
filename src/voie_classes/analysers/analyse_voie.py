from voie_classes.analysers.analyse_type import AnalyseType
from voie_classes.analysers.analyse_linguistique import AnalyseLinguistique
from voie_classes.analysers.analyse_position import AnalysePosition
from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib


class AnalyseVoie(AnalyseType, AnalyseLinguistique, AnalysePosition):
    def __init__(
            self,
            label_raw: str,
            infolib: InfoLib
            ):
        # Initialisation de la classe de base Voie
        Voie.__init__(self, label_raw, infolib)
