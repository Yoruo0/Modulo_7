import unittest
from unittest.mock import Mock
from src.views.person_creator_view import PersonCreatorView
from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse

class TestPersonCreatorView(unittest.TestCase):
    def test_handle(self):

        mock_controller = Mock()

        expected_response = {"success": True, "data": "Person Created"}
        mock_controller.create.return_value = expected_response

        view = PersonCreatorView(mock_controller)

        request_body = {"name": "John Doe", "age": 30}
        request = HttpRequest(body=request_body)

        response = view.handle(request)

        mock_controller.create.assert_called_once_with(request_body)

        self.assertIsInstance(response, HttpResponse)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.body, expected_response)

# from src.controllers.interfaces.person_creator_controller import PersonCreatorControllerInterface
# from .http_types.http_request import HttpRequest
# from .http_types.http_response import HttpResponse
# from .person_creator_view import PersonCreatorView

# # --- PASSO 1: Criar a implementação concreta para o teste ---
# class PersonCreatorControllerSpy(PersonCreatorControllerInterface):
#     """
#     Esta classe simula o comportamento do controller real.
#     Chamamos de 'Spy' ou 'Stub' porque ela nos permite verificar a entrada
#     e definir uma saída fixa sem lógica complexa ou banco de dados.
#     """
#     def __init__(self) -> None:
#         self.create_attributes_received = None # Para verificar o que chegou aqui

#     def create(self, person_info: dict) -> dict:
#         self.create_attributes_received = person_info # Armazena para validação
#         return {
#             "success": True,
#             "data": { "name": person_info.get("name"), "id": 123 }
#         }

# # --- PASSO 2: O Teste em si ---
# def test_handle_person_creator():
#     # A. Arrumar (Arrange)
#     # Criamos a dependência manual
#     controller = PersonCreatorControllerSpy()
#     # Instanciamos a View passando essa dependência
#     view = PersonCreatorView(controller)

#     # Criamos uma requisição fictícia
#     request_body = {"name": "Olaf", "age": 30}
#     request = HttpRequest(body=request_body)

#     # B. Agir (Act)
#     response = view.handle(request)

#     # C. Asserir (Assert) - Validação dos resultados

#     # 1. Verificamos se o status code é o esperado (201)
#     assert response.status_code == 201
#     # Isso garante que a View não retornou um dicionário comum ou uma String por erro
#     assert isinstance(response, HttpResponse)

#     # 2. Verificamos se o corpo da resposta está correto
#     assert response.body["success"] is True
#     assert response.body["data"]["name"] == "Olaf"

#     # 3. Verificamos se a View passou os dados corretos para o controller
#     # Isso garante que a 'ponte' entre HTTP e Lógica está funcionando
#     assert controller.create_attributes_received == request_body

#     print("Teste passou com sucesso!")
