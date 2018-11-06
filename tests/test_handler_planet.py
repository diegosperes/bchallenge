from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.planet import Planet


def planet(name):
    return {
        'name': name,
        'climate': ["5be0622e08301fc814313d48"],
        'terrain': ["1be0663e18876fc814313d49"],
        'movie': ["3be0999e18876fc814313d23"],
    }


class PlanetHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @property
    def model(self):
        return Planet

    @property
    def data(self):
        return {
            'test_get_model': planet('Black Planet'),
            'test_insert_model': planet('Blue Planet'),
            'test_update_model': [planet('Green Planet'), planet('Purple Planet')],
            'test_delete_model': planet('Red Planet'),
            'test_update_nonexistent_model': planet('Pink Planet'),
            'test_update_with_invalid_id': planet('Brown Planet'),
            'test_update_without_data': planet('Orange Planet')
        }
