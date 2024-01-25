# -*- coding: utf-8 -*-
import logging
from injector import Injector

from config.logger_configuration import LoggerConfiguration
from config.settings_configuration import settings


class LancementTest:
    def executer(self):
        logging.info("injection ok")


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


if __name__ == "__main__":
    run()
