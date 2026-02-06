import pytest
from src.models.sqlite.settings.connection import db_connection_handler
from .people_repository import PeopleRepository
from .pets_repository import PetsRepository

#db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="Interaction with db")
def test_list_pets():
    repo = PetsRepository(db_connection_handler)
    response = repo.list_pets()
    print()
    print(response)

@pytest.mark.skip(reason="Interaction with db")
def test_delte_pet():
    name = "belinha"
    repo = PetsRepository(db_connection_handler)
    repo.delete_pets(name)

@pytest.mark.skip(reason="Interaction with db")
def test_insert_person():
    fist_name = "test name"
    last_name = "last test"
    age = 79
    pet_id = 2

    repo = PeopleRepository(db_connection_handler)
    repo.insert_person(fist_name, last_name, age, pet_id)

@pytest.mark.skip(reason="Interaction with db")
def test_get_person():
    person_id = 1

    repo = PeopleRepository(db_connection_handler)
    response = repo.get_person(person_id)
    print()
    print(response)
