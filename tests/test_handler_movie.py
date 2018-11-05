from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.movie import Movie


class MovieHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @property
    def model(self):
        return Movie

    @property
    def data(self):
        return {
            'test_get_model': {'name': 'Big Black Movie'},
            'test_insert_model': {'name': 'Big Blue Movie'},
            'test_update_model': [{'name': 'Big Green Movie'}, {'name': 'Big Purple Movie'}],
            'test_delete_model': {'name': 'Big Red Movie'},
            'test_update_nonexistent_model': {'name': 'Pink Movie'},
            'test_update_with_invalid_id': {'name': 'Brown Movie'},
            'test_update_without_data': {'name': 'Orange Movie'}
        }
