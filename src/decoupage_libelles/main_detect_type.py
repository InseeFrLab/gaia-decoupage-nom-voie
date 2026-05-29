import argparse

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.preprocessing.pipeline.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Détection des types de voie au sein du libellé de voie"
    )

    parser.add_argument(
        "voie_ou_detecter",
        type=str,
        help="Libellé de voie où détecter les types de voie",
    )

    args = parser.parse_args()

    voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = VoieLibPreprocessorUseCase()

    infovoie = InfoVoie(label_origin=args.voie_ou_detecter)
    r = voie_lib_preprocessor_use_case.execute([infovoie])

    print(r[0].types_and_positions)
