from sqlalchemy.exc import NoResultFound
from src.models.sqlite.entities.people import PeopleTable
from src.models.sqlite.entities.pets import PetsTable
from src.models.sqlite.interfaces.people_repository import PeopleRepositotyInterface

class PeopleRepository(PeopleRepositotyInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def insert_person(self, first_name: str, last_name:str, age:int, pet_id:int) -> None:
        with self.__db_connection as database:
            try:
                person_data = PeopleTable(
                    first_name = first_name,
                    last_name = last_name,
                    age = age,
                    pet_id = pet_id
                )
                database.session.add(person_data)
                database.session.commit()
            except Exception as excepion:
                database.session.rollback()
                raise excepion

    def get_person(self, person_id: int) -> PeopleTable | None:
        with self.__db_connection as database:
            try:
                person = (
                    database.session
                    .query(PeopleTable)
                    .outerjoin(PetsTable, PetsTable.id == PeopleTable.id)
                    .filter(PeopleTable.id == person_id)
                    .with_entities(
                        PeopleTable.first_name,
                        PeopleTable.last_name,
                        PetsTable.name.label("pet_name"),
                        PetsTable.type.label("pet_type")
                    )
                    .one()
                )
                return person

            except NoResultFound:
                return None
