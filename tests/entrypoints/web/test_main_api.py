import logging
from fastapi.testclient import TestClient
from decoupage_libelles.entrypoints.web.main_api import app, initialize_api

# Initialisation du logger pour les tests
logging.basicConfig(level=logging.DEBUG)

# Initialisation de l'API avant les tests
initialize_api()

# Création d'un client de test pour l'API
client = TestClient(app)


def test_analyse_libelles_voies():
    # Given
    list_labels_voies = {"list_labels_voies": ["rue Hoche", "Residence Soleil Rue des cerisiers"]}
    # When
    response = client.post("/analyse-libelles-voies", json=list_labels_voies)
    # Then
    assert response.status_code == 200
    assert response.json() == {
        "reponse": [
            {"rue hoche": {"numero": "", "indice_rep": "", "typeVoie": "rue", "libelleVoie": "hoche", "complementAdresse": " ", "complementAdresse2": ""}},
            {
                "residence soleil rue des cerisiers": {
                    "numero": "",
                    "indice_rep": "",
                    "typeVoie": "rue",
                    "libelleVoie": "des cerisiers",
                    "complementAdresse": "residence soleil",
                    "complementAdresse2": "",
                }
            },
        ]
    }
