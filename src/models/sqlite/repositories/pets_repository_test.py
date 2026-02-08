from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.exc import NoResultFound
from src.models.sqlite.entities.pets import PetsTable
from .pets_repository import PetsRepository


class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PetsTable)],  # query
                    [
                        PetsTable(name="dog", type="dog"),
                        PetsTable(name="cat", type="cat"),
                    ],  # resultado
                )
            ]
        )

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): pass



def test_list_pets():
    mock_connection = MockConnection()
    repo = PetsRepository(mock_connection)
    response = repo.list_pets()

    mock_connection.session.query.assert_called_once_with(PetsTable)
    mock_connection.session.all.assert_called_once()
    mock_connection.session.filter.assert_not_called()

    assert response[0].name == "dog" # type: ignore

def test_delete_pet():
    mock_connection = MockConnection()
    repo = PetsRepository(mock_connection)

    repo.delete_pets("petName")

    mock_connection.session.query.assert_called_once_with(PetsTable)
    mock_connection.session.filter.assert_called_once_with(PetsTable.name == "petName")
    mock_connection.session.delete.assert_called_once()

def test_list_pets_no_results():
    mock_connection = MockConnectionNoResult()
    repo = PetsRepository(mock_connection)
    response = repo.list_pets()

    mock_connection.session.query.assert_called_once_with(PetsTable)
    mock_connection.session.all.assert_not_called()
    mock_connection.session.filter.assert_not_called()

    assert response == []

def test_delete_pet_error():
    mock_connection = MockConnectionNoResult()
    repo = PetsRepository(mock_connection)

    with pytest.raises(Exception):
        repo.delete_pets("petName")

    mock_connection.session.rollback.assert_called_once()


# from unittest import mock
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.models.sqlite.settings.base import Base
# from src.models.sqlite.entities.pets import PetsTable
# from .pets_repository import PetsRepository

# #1. Criamos um "Fake" real usando SQLite em memória
# class FakeConnection:
#     def __init__(self) -> None:
#         engine = create_engine("sqlite:///:memory:") # Banco rápido em RAM
#         Base.metadata.create_all(engine) # Cria as tabelas reais
#         self.session_factory = sessionmaker(bind=engine)
#         self.session = self.session_factory()

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.session.close()

# #2. Testes focados em comportamento e estado
# def test_list_pets_classic():
#     conn = FakeConnection()
#     #Populamos o estado real
#     conn.session.add(PetsTable(name="dog", type="dog"))
#     conn.session.commit()

#     repo = PetsRepository(conn)
#     response = repo.list_pets()

#     #Diferença: Verificamos o conteúdo, não se chamou .query()
#     assert len(response) == 1
#     assert response[0].name == "dog"

# def test_delete_pet_classic():
#     conn = FakeConnection()
#     conn.session.add(PetsTable(name="petName", type="cat"))
#     conn.session.commit()

#     repo = PetsRepository(conn)
#     repo.delete_pets("petName")

#     #Verificamos se o registro REALMENTE sumiu do banco
#     result = conn.session.query(PetsTable).filter_by(name="petName").first()
#     assert result is None

# def test_delete_pet_error_classic():
#     conn = FakeConnection()
#     repo = PetsRepository(conn)

#     #$Forçamos um erro real: deletar algo que não existe (ou causar erro de constraint)
#     #Nota: No SQLite, deletar o que não existe não gera exceção,
#     #então para testar o rollback, simularíamos um erro de commit.
#     with mock.patch.object(conn.session, 'commit', side_effect=Exception("DB Error")):
#         with pytest.raises(Exception):
#             repo.delete_pets("any")
