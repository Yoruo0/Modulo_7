from src.models.sqlite.entities.pets import PetsTable
from.pet_lister_controller import PetListerController

class MockPetsRepository:
    def list_pets(self):
        return [
            PetsTable(name = "Viper", type = "snake", id = 4),
            PetsTable(name = "Hedwigs", type = "owl", id = 48),
        ]

def test_list_pets():
    controller = PetListerController(MockPetsRepository()) # type: ignore
    response = controller.list()

    expected_response = {
        "data":{
            "type": "Pets",
            "count": 2,
            "attributes": [
                { "name": "Viper", "id":4 },
                { "name": "Hedwigs", "id":48, },
            ]
        }
    }

    assert response == expected_response
