from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher

if __name__ == "__main__":
    launcher = TypeVoieDecoupageLauncher()
    
    voies_a_decouper = [
        "RUE HOCHE",
        "CHE DES SEMAPHORES",
        "HLM AV KLEBER BAT B",
        "LES HARDONNIERES",
        "APPARTEMENT JEAN LAMOUR",
    ]

    resultats = launcher.execute(voies_a_decouper)

    for r in resultats:
        print(r.label_origin, r.type_assigned, r.label_assigned, r.compl_assigned)
