from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class SeparateComplementaryPartUseCase:
    def execute(self, voie: InfoVoie) -> InfoVoie:
        voie_upper = voie.label_origin.upper()
        split_on_underscore = voie_upper.split(" - ")
        split_hashtag = voie_upper.split("#")

        if len(split_on_underscore) > 1:  # 'R DES NOYERS - SITE-BEAUPLAN'
            voie.label_raw = split_on_underscore[0]
            voie.complement = split_on_underscore[1]

        if voie_upper.count("#") == 2:  # 'R DU VAL DE SEVRE #49179#'
            voie.label_raw = split_hashtag[0]
            voie.complement = split_hashtag[1]

        if "(" in voie_upper and ")" in voie_upper and voie_upper.index("(") < voie_upper.index(")"):  # 'R DES NOYERS (SITE-BEAUPLAN)'
            voie.label_raw = voie_upper.split("(")[0].strip()
            voie.complement = voie_upper.split("(")[1].split(")")[0].strip()

        if not voie.label_raw:
            voie.label_raw = voie_upper

        return voie
