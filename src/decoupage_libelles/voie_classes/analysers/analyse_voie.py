from voie_classes.analysers.analyse_type import AnalyseType
from voie_classes.analysers.analyse_linguistique import AnalyseLinguistique
from voie_classes.analysers.analyse_position import AnalysePosition
from voie_classes.voie import Voie
from voie_classes.informations_on_libelle import InfoLib


class AnalyseVoie:

    def __init__(self, analyse_type: AnalyseType, analyse_linguistique: AnalyseLinguistique, analyse_position: AnalysePosition):
        self.analyse_type = analyse_type
        self.analyse_linguistique = analyse_linguistique
        self.analyse_position = analyse_position

    def executer(self, label_raw: str, infolib: InfoLib):
        # Initialisation de la classe de base Voie
        voie: Voie = Voie(label_raw, infolib)
        self.analyse_position.execute(infolib)
        # Si type en première position et agglomérant alors
        if infolib.type_en_premiere_position and infolib.type_agglomerant:
            # 
        