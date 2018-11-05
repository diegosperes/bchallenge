from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.climate import Climate


class ClimateHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @property
    def model(self):
        return Climate

    @property
    def data(self):
        return {
            'test_get_model': {'name': 'Redvalvet Climate'},
            'test_insert_model': {'name': 'Blue Climate'},
            'test_update_model': [{'name': 'Green Climate'}, {'name': 'Purple Climate'}],
            'test_delete_model': {'name': 'Red Climate'},
            'test_update_nonexistent_model': {'name': 'Pink Climate'},
            'test_update_with_invalid_id': {'name': 'Brown Climate'},
            'test_update_without_data': {'name': 'Orange Climate'}
        }
