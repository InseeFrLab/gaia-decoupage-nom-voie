import re
from typing import List


class SynonymsDilatationUseCase:
    TYPE_VOIE_SYNONYMS = {
        "ANC CHEM":"ANCIEN CHEMIN",
        "ANCIEN CHEM":"ANCIEN CHEMIN",
        "ANC CHEMIN":"ANCIEN CHEMIN",
        "ANC PL":"ANCIENNE PLACE",
        "ANC RTE":"ANCIENNE ROUTE",
        "ANC ROUTE":"ANCIENNE ROUTE",
        "ANCIENNE RTE":"ANCIENNE ROUTE",
        "ANC VOIE":"ANCIENNE VOIE",
        "C R":"CHEMIN RURAL",
        "GDE PCE":"GRAND PLACE",
        "GRANDE PLACE":"GRAND PLACE",
        "GDE ALLEE":"GRANDE ALLEE",
        "GDE AV":"GRANDE AVENUE",
        "GRAND RUE":"GRANDE RUE",
        "GDE RUE":"GRANDE RUE",
        "GR RUE":"GRANDE RUE",
        "HABITATION A LOYER MODERE":"HLM",
        'PARC D ACTIVITES': 'ZONE D ACTIVITES',
        "PT CHEM":"PETIT CHEMIN",
        "PTE RUE":"PETITE RUE",
        "RTE DEPARTEMENTALE":"ROUTE DEPARTEMENTALE",
        'RTE NATIONALE': 'ROUTE NATIONALE',
        'VX CHEMIN': 'VIEUX CHEMIN',
        'VX CHEM': 'VIEUX CHEMIN',
        'VX CHE': 'VIEUX CHEMIN',
        'ZONE ACTIVITES': 'ZONE D ACTIVITES',
        'ZONE AMENAGEMENT CONCERTE': 'ZONE D AMENAGEMENT CONCERTE',
        'ZONE DAMENAGEMENT CONCRETE': 'ZONE D AMENAGEMENT CONCERTE',
        'ZONE DAMENAGEMENT DIFFERE': 'ZONE D AMENAGEMENT DIFFERE',
        'ZONE AMENAGEMENT DIFFERE': 'ZONE D AMENAGEMENT DIFFERE',
        "ZONE DACTIVITES ECONOMIQUES": "ZONE D ACTIVITES ECONOMIQUES",
        "ZONE ACTIVITES ECONOMIQUES": "ZONE D ACTIVITES ECONOMIQUES",
    }

    # TYPE_VOIE_ACRONYMS = {
        # "ABE":"ABBAYE",
        # "AER":"AERODROME",
        # "AERG":"AEROGARE",
        # "AERP":"AEROPORT",
        # "AGL":"AGGLOMERATION",
        # "ALL":"ALLEE",
        # "ACH":"ANCIEN CHEMIN",
        # "APL":"ANCIENNE PLACE",
        # "ART":"ANCIENNE ROUTE",
        # "AR":"ANCIENNE RUE",
        # "ANV":"ANCIENNE VOIE",
        # "ANGL":"ANGLE",
        # "AUT":"AUTOROUTE",
        # "AVE":"AVENUE",
        # "AV":"AVENUE",
        # "BRE":"BARRIERE",
        # "BCH":"BAS CHEMIN",
        # "BSN":"BASSIN",
        # "BSTD":"BASTIDE",
        # "BASTION":"BASTION",
        # "BER":"BERGE",
        # "BCLE":"BOUCLE",
        # "BD":"BOULEVARD",
        # "BRG":"BOURG",
        # "BRC":"BRECHE",
        # "BRTL":"BRETELLE",
        # "CALL":"CALLE",
        # "CALLADA":"CALLE",
        # "CAMI":"CAMIN",
        # "CGNE":"CAMPAGNE",
        # "CPG":"CAMPING",
        # "CAN":"CANAL",
        # "CARR":"CARRE",
        # "CAU":"CARREAU",
        # "CAR":"CARREFOUR",
        # "CAE":"CARRIERA",
        # "CARE":"CARRIERE",
        # "CASR":"CASERNE",
        # "CST":"CASTEL",
        # "CEIN":"CEINTURE",
        # "CTRE":"CENTRE",
        # "CCAL":"CENTRE COMMERCIAL",
        # "CCIAL":"CENTRE COMMERCIAL",
        # "CHL":"CHALET",
        # "CHP":"CHAMP",
        # "CHAMPS":"CHAMP",
        # "CHPS":"CHAMP",
        # "CHAP":"CHAPELLE",
        # "CHI":"CHARMILLE",
        # "CHA":"CHASSE",
        # "CHT":"CHATEAU",
        # "CHS":"CHAUSSEE",
        # "CHE":"CHEMIN",
        # "CHEMINEMENT":"CHEMIN",
        # "CC":"CHEMIN COMMUNAL",
        # "CD":"CHEMIN DEPARTEMENTAL",
        # "CF":"CHEMIN FORESTIER",
        # "CR":"CHEMIN RURAL",
        # "CHV":"CHEMIN VICINAL",
        # "CHEM":"CHEMIN",
        # "CLS":"CLOS",
        # "CTR":"CONTOUR",
        # "COR":"CORNICHE",
        # "CORO":"CORON",
        # "COTT":"COTTAGE",
        # "CLR":"COULOIR",
        # "CRS":"COURS",
        # "CIVE":"COURSIVE",
        # "CRX":"CROIX",
        # "DARCE":"DARSE",
        # "DARS":"DARSE",
        # "DEG":"DEGRE",
        # "DSC":"DESCENTE",
        # "DEVI":"DEVIATION",
        # "DIG":"DIGUE",
        # "DOM":"DOMAINE",
        # "DRA":"DRAILLE",
        # "ECA":"ECART",
        # "ECL":"ECLUSE",
        # "EGL":"EGLISE",
        # "EMBR":"EMBRANCHEMENT",
        # "EMP":"EMPLACEMENT",
        # "ENV":"ENCLAVE",
        # "ENC":"ENCLOS",
        # "ESC":"ESCALIER",
        # "ESPA":"ESPACE",
        # "ESP":"ESPLANADE",
        # "ETNG":"ETANG",
        # "FDG":"FAUBOURG",
        # "FG":"FAUBOURG",
        # "FRM":"FERME",
        # "FD":"FOND",
        # "FON":"FONTAINE",
        # "FOR":"FORET",
        # "FORM":"FORUM",
        # "FOS":"FOSSE",
        # "GAL":"GALERIE",
        # "GBD":"GRAND BOULEVARD",
        # "GRC":"GRAND CLOS",
        # "GPL":"GRAND PLACE",
        # "GRA":"GRANDE ALLEE",
        # "GAV":"GRANDE AVENUE",
        # "GR":"GRANDE RUE",
        # "GREV":"GREVE",
        # "GRI":"GRILLE",
        # "GPE":"GROUPE",
        # "GPT":"GROUPEMENT",
        # "HAB":"HABITATION",
        # "HLG":"HALAGE",
        # "HLE":"HALLE",
        # "HAM":"HAMEAU",
        # "HCH":"HAUT CHEMIN",
        # "HTR":"HAUTEUR",
        # "HIP":"HIPPODROME",
        # "HOT":"HOTEL",
        # "ILE":"ILE",
        # "ILO":"ILOT",
        # "IMP":"IMPASSE",
        # "JARD":"JARDIN",
        # "JTE":"JETEE",
        # "LEVE":"LEVEE",
        # "LICE":"LICES",
        # "LIEUDIT":"LIEU DIT",
        # "LDT":"LIEU DIT",
        # "LD":"LIEU DIT",
        # "LIGN":"LIGNE",
        # "LOT":"LOTISSEMENT",
        # "MAIS":"MAISON",
        # "MAR":"MARCHE",
        # "MRN":"MARINA",
        # "MTE":"MONTEE",
        # "MNE":"MORNE",
        # "MLN":"MOULIN",
        # "MOUL":"MOULIN",
        # "MUS":"MUSEE",
        # "NTE":"NOUVELLE ROUTE",
        # "PAL":"PALAIS",
        # "PAEC":"PARC D ACTIVITES ECONOMIQUES",
        # "PKG":"PARKING",
        # "PRV":"PARVIS",
        # "PAS":"PASSAGE",
        # "PN":"PASSAGE A NIVEAU",
        # "PASS":"PASSE",
        # "PLE":"PASSERELLE",
        # "PAT":"PATIO",
        # "PCH":"PETIT CHEMIN",
        # "PTSEN":"PETIT SENTIER",
        # "PTA":"PETITE ALLEE",
        # "PAE":"PETITE AVENUE",
        # "PIM":"PETITE IMPASSE",
        # "PRT":"PETITE ROUTE",
        # "PTR":"PETITE RUE",
        # "PR":"PETITE RUE",
        # "PHAR":"PHARE",
        # "PIST":"PISTE",
        # "PLA":"PLACA",
        # "PL":"PLACE",
        # "PTTE":"PLACETTE",
        # "PLCI":"PLACIS",
        # "PLAG":"PLAGE",
        # "PLN":"PLAINE",
        # "PLAN":"PLAN",
        # "PLT":"PLATEAU",
        # "PNT":"POINTE",
        # "PONT":"PONT",
        # "PCHE":"PORCHE",
        # "PTE":"PORTE",
        # "PORQ":"PORTIQUE",
        # "POST":"POSTE",
        # "POT":"POTERNE",
        # "PRQ":"PRESQU ILE",
        # "PROM":"PROMENADE",
        # "QU":"QUAI",
        # "QUA":"QUARTIER",
        # "QRT":"QUARTIER",
        # "RAC":"RACCOURCI",
        # "RAID":"RAIDILLON",
        # "RPE":"RAMPE",
        # "RNG":"RANGEE",
        # "RVE":"RAVINE",
        # "REM":"REMPART",
        # "RES":"RESIDENCE",
        # "ROC":"ROCADE",
        # "RPT":"ROND POINT",
        # "RDE":"RONDE",
        # "RTD":"ROTONDE",
        # "RTE":"ROUTE",
        # "RD":"ROUTE DEPARTEMENTALE",
        # "RN":"ROUTE NATIONALE",
        # "R":"RUE",
        # "RLE":"RUELLE",
        # "RULT":"RUELLETTE",
        # "RUET":"RUETTE",
        # "RUIS":"RUISSEAU",
        # "SENTE":"SENTIER",
        # "SEN":"SENTIER",
        # "SQ":"SQUARE",
        # "STDE":"STADE",
        # "STA":"STATION",
        # "TRN":"TERRAIN",
        # "TSSE":"TERRASSE",
        # "TER":"TERRE",
        # "TPL":"TERRE PLEIN",
        # "TRT":"TERTRE",
        # "TRAB":"TRABOULE",
        # "TRA":"TRAVERSE",
        # "TUN":"TUNNEL",
        # "VALLON":"VALLEE",
        # "VALL":"VALLEE",
        # "VAL":"VALLEE",
        # "VEN":"VENELLE",
        # "VIAD":"VIADUC",
        # "VTE":"VIEILLE ROUTE",
        # "VR":"VIEILLE RUE",
        # "VCHE":"VIEUX CHEMIN",
        # "VLA":"VILLA",
        # "VLG":"VILLAGE",
        # "VLGE":"VILLAGE",
        # "VILLAG":"VILLAGE",
        # "VGE":"VILLAGE",
        # "VIL":"VILLE",
        # "VOI":"VOIE",
        # "VC":"VOIE COMMUNALE",
        # "VOIR":"VOIRIE",
        # "VOUT":"VOUTE",
        # "VOY":"VOYEUL",
        # "ZUP":"ZONE A URBANISER EN PRIORITE",
        # "ZAR":"ZONE ARTISANALE",
        # "ZA":"ZONE D ACTIVITES",
        # "ZAE":"ZONE D ACTIVITES ECONOMIQUES",
        # "ZAC":"ZONE D AMENAGEMENT CONCERTE",
        # "ZAD":"ZONE D AMENAGEMENT DIFFERE",
        # "ZI":"ZONE INDUSTRIELLE",
        # "PAV":"PAVILLON",
        # "IMM":"IMMEUBLE",
        # "BAT":"BATIMENT",
        # "APRT":"APPARTEMENT",
        # "APT":"APPARTEMENT",
        # "APPRT":"APPARTEMENT",
        # "APPT":"APPARTEMENT",
        # "LGT":"LOGEMENT",
        # "LOG":"LOGEMENT",
        # "ENT":"ENTREE"
        # }

    EXTRA_SYNONYMS = {
        "ST":"SAINT",
        "STE":"SAINTE",
        "STS":"SAINTS",
        "STES":"SAINTES",
        "GD":"GRAND",
        "GDE":"GRANDE",
        "GDS":"GRANDS",
        "GDES":"GRANDES",
        "PTS":"PETITS",
        "PTES":"PETITES",
        "GEN":"GENERAL",
        "MAL":"MARECHAL",
        "LT":"LIEUTENANT",
        "CDT":"COMMANDANT",
        "DR":"DOCTEUR",
        "HT":"HAUT",
        "HTE":"HAUTE",
        "HTS":"HAUTS",
        "HTES":"HAUTES",
        "PDT":"PRESIDENT",
        "SGT":"SERGENT"
        }

    def execute(self, label_preproc: List[str]) -> List[str]:
        label_preproc = (' ').join(label_preproc)
        for acronym, full_form in SynonymsDilatationUseCase.TYPE_VOIE_SYNONYMS.items():
            label_preproc = re.sub(rf'\b{acronym}\b', full_form, label_preproc, flags=re.IGNORECASE)        

        # for acronym, full_form in SynonymsDilatationUseCase.TYPE_VOIE_ACRONYMS.items():
        #     label_preproc = re.sub(rf'\b{acronym}\b', full_form, label_preproc, flags=re.IGNORECASE)        

        for acronym, full_form in SynonymsDilatationUseCase.EXTRA_SYNONYMS.items():
            label_preproc = re.sub(rf'\b{acronym}\b', full_form, label_preproc, flags=re.IGNORECASE)        

        label_preproc_dilated = label_preproc.split(' ')

        return label_preproc_dilated
