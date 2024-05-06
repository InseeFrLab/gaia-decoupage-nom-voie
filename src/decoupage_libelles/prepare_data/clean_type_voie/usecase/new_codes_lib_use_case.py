import pandas as pd


class NewCodesLibUseCase:
    NEW_CODES = [
        {"CODE": "ZAE", "LIBELLE": "ZONE D'ACTIVITES ECONOMIQUES"},
        {"CODE": "GRA", "LIBELLE": "GRANDE ALLEE"},
        {"CODE": "APL", "LIBELLE": "ANCIENNE PLACE"},
        {"CODE": "ANV", "LIBELLE": "ANCIENNE VOIE"},
        {"CODE": "GAV", "LIBELLE": "GRANDE AVENUE"},
        {"CODE": "PTS", "LIBELLE": "PETIT SENTIER"},
        {"CODE": "AERP", "LIBELLE": "AEROPORT"},
        {"CODE": "RD", "LIBELLE": "ROUTE DEPARTEMENTALE"},
        {"CODE": "HOT", "LIBELLE": "HOTEL"},
        {"CODE": "PAEC", "LIBELLE": "PARC D ACTIVITES ECONOMIQUES"},
        {"CODE": "ZAR", "LIBELLE": "ZONE ARTISANALE"},
        {"CODE": "GPL", "LIBELLE": "GRAND PLACE"},
        {"CODE": "LD", "LIBELLE": "LIEU DIT"},
        {"CODE": "ABE", "LIBELLE": "ABBAYE"},
        {"CODE": "ANSE", "LIBELLE": "ANSE"},
        {"CODE": "AR", "LIBELLE": "ANCIENNE RUE"},
        {"CODE": "BAL", "LIBELLE": "BALCON"},
        {"CODE": "BASTION", "LIBELLE": "BASTION"},
        {"CODE": "BCH", "LIBELLE": "BAS CHEMIN"},
        {"CODE": "BCLE", "LIBELLE": "BOUCLE"},
        {"CODE": "BOIS", "LIBELLE": "BOIS"},
        {"CODE": "BRC", "LIBELLE": "BRECHE"},
        {"CODE": "BSTD", "LIBELLE": "BASTIDE"},
        {"CODE": "BUTTE", "LIBELLE": "BUTTE"},
        {"CODE": "CALE", "LIBELLE": "CALE"},
        {"CODE": "CARR", "LIBELLE": "CARRE"},
        {"CODE": "CAU", "LIBELLE": "CARREAU"},
        {"CODE": "CCAL", "LIBELLE": "CENTRE COMMERCIAL"},
        {"CODE": "CEIN", "LIBELLE": "CEINTURE"},
        {"CODE": "CGNE", "LIBELLE": "CAMPAGNE"},
        {"CODE": "CHI", "LIBELLE": "CHARMILLE"},
        {"CODE": "CHAP", "LIBELLE": "CHAPELLE"},
        {"CODE": "COLLINE", "LIBELLE": "COLLINE"},
        {"CODE": "COTEAU", "LIBELLE": "COTEAU"},
        {"CODE": "COTT", "LIBELLE": "COTTAGE"},
        {"CODE": "CST", "LIBELLE": "CASTEL"},
        {"CODE": "DEG", "LIBELLE": "DEGRE"},
        {"CODE": "EGL", "LIBELLE": "EGLISE"},
        {"CODE": "ENCEINTE", "LIBELLE": "ENCEINTE"},
        {"CODE": "FORM", "LIBELLE": "FORUM"},
        {"CODE": "GPE", "LIBELLE": "GROUPE"},
        {"CODE": "GPT", "LIBELLE": "GROUPEMENT"},
        {"CODE": "GRI", "LIBELLE": "GRILLE"},
        {"CODE": "HCH", "LIBELLE": "HAUT CHEMIN"},
        {"CODE": "MLN", "LIBELLE": "MOULIN"},
        {"CODE": "MUS", "LIBELLE": "MUSEE"},
        {"CODE": "PAL", "LIBELLE": "PALAIS"},
        {"CODE": "PAT", "LIBELLE": "PATIO"},
        {"CODE": "PERIPHERIQUE", "LIBELLE": "PERIPHERIQUE"},
        {"CODE": "PIM", "LIBELLE": "PETITE IMPASSE"},
        {"CODE": "PN", "LIBELLE": "PASSAGE A NIVEAU"},
        {"CODE": "PRE", "LIBELLE": "PRE"},
        {"CODE": "PRQ", "LIBELLE": "PRESQU ILE"},
        {"CODE": "RAID", "LIBELLE": "RAIDILLON"},
        {"CODE": "RDE", "LIBELLE": "RONDE"},
        {"CODE": "RNG", "LIBELLE": "RANGEE"},
        {"CODE": "STA", "LIBELLE": "STATION"},
        {"CODE": "VR", "LIBELLE": "VIEILLE RUE"},
        {"CODE": "BAT", "LIBELLE": "BATIMENT"},
        {"CODE": "PAV", "LIBELLE": "PAVILLON"},
        {"CODE": "IMM", "LIBELLE": "IMMEUBLE"},
        {"CODE": "GRC", "LIBELLE": "GRAND CLOS"},
        {"CODE": "RN", "LIBELLE": "ROUTE NATIONALE"},
    ]

    def execute(self, type_voie_df: pd.DataFrame) -> pd.DataFrame:
        """
        Ajoute un nouveau code de type de voie au DataFrame.

        Cette méthode crée une nouvelle ligne dans le DataFrame 'type_voie_df'
        pour un code de type de voie qui n'était pas présent dans les données
        originales. Le nouveau code et son libellé correspondant sont définis
        dans le dictionnaire 'new_codes'.

        Après l'ajout, le DataFrame est trié par le code de type de voie pour
        maintenir l'ordre, et l'index est réinitialisé pour une meilleure
        cohérence.
        """
        new_row_df = pd.DataFrame(NewCodesLibUseCase.NEW_CODES)
        type_voie_df = pd.concat([type_voie_df, new_row_df], ignore_index=True).sort_values(by="CODE").reset_index(drop=True)

        return type_voie_df
