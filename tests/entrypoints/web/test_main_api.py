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
    libelle_data = {"libelle": "Rue de la Paix"}
    # When
    response = client.post("/analyse-libelles-voies", json=libelle_data)
    # Then
    assert response.status_code == 200
    assert response.json() == {"reponse": {"libelle": "Rue de la Paix"}}
