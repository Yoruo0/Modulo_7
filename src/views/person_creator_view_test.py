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
