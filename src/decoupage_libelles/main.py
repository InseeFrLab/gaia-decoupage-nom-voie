import argparse

from decoupage_libelles.config.type_voie_decoupage_launcher import (
    TypeVoieDecoupageLauncher,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Découpage d'un libellé de voie"
    )

    parser.add_argument(
        "voie_a_decouper",
        type=str,
        help="Libellé de voie à découper",
    )

    args = parser.parse_args()

    launcher = TypeVoieDecoupageLauncher()

    r = launcher.execute([args.voie_a_decouper])

    print(
        f"Libellé de voie à découper : {r[0].label_origin}\n"
        f"Type de voie : {r[0].type_assigned}\n"
        f"Nom de voie : {r[0].label_assigned}\n"
        f"Complement : {r[0].compl_assigned}"
    )
