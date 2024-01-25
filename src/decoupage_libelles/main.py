# -*- coding: utf-8 -*-
import logging
from injector import Injector, inject

from config.logger_configuration import LoggerConfiguration
from config.settings_configuration import settings


class Classe2:
    def executer(self):
        logging.info("injection ok")


class LancementTest:
    @inject
    def __init__(self, classe2: Classe2):
        self.classe2: Classe2 = classe2

    def executer(self):
        self.classe2.executer()


def print_settings():
    logging.info(f"chemin_fichier_majic: {settings.chemin_fichier_majic}")
    logging.info(f"chemin_referentiel_types_voies: {settings.chemin_referentiel_types_voies}")
    logging.info(f"chemin_sortie: {settings.chemin_sortie}")


def run():
    LoggerConfiguration().configure_console_handler()
    logging.info("Programme de découpage des libellés de voies")
    print_settings()
    injector = Injector()
    lancementTest: LancementTest = injector.get(LancementTest)
    lancementTest.executer()

    # Lecture du fichier contenant du référentiel des types de voies
    # Nettoyage et enrichissement des types de voies
    # Lecture du fichier Majic
    # Transformation des données
    # Ecriture du fichier majic


if __name__ == "__main__":
    run()
