from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.terrain import Terrain


class TerrainHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @property
    def model(self):
        return Terrain

    @property
    def data(self):
        return {
            'test_get_model': {'name': 'Redvalvet Terrain'},
            'test_insert_model': {'name': 'Blue Terrain'},
            'test_update_model': [{'name': 'Green Terrain'}, {'name': 'Purple Terrain'}],
            'test_delete_model': {'name': 'Red Terrain'},
            'test_update_nonexistent_model': {'name': 'Pink Terrain'},
            'test_update_with_invalid_id': {'name': 'Brown Terrain'},
            'test_update_without_data': {'name': 'Orange Terrain'}
        }
