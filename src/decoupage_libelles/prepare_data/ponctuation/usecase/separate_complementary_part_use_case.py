from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie

class SeparateComplementaryPartUseCase:

    def execute(self, voie: InfoVoie) -> InfoVoie:
        # split_on_underscore = voie.label_origin.split(" - ")
        # split_hashtag = voie.label_origin.split("#")

        # if len(split_on_underscore) > 1:  # 'R DES NOYERS - SITE-BEAUPLAN'
        #     voie.label_raw = split_on_underscore[0]
        #     voie.complement = split_on_underscore[1]

        # if voie.label_origin.count("#") == 2:  # 'R DU VAL DE SEVRE #49179#'
        #     voie.label_raw = split_hashtag[0]
        #     voie.complement = split_hashtag[1]

        # if "(" in voie.label_origin and ")" in voie.label_origin and voie.label_origin.index("(") < voie.label_origin.index(")"):  # 'R DES NOYERS (SITE-BEAUPLAN)'
        #     voie.label_raw = voie.label_origin.split("(")[0].strip()
        #     voie.complement = voie.label_origin.split("(")[1].split(")")[0].strip()

        if not voie.label_raw:
            voie.label_raw = voie.label_origin

        return voie
