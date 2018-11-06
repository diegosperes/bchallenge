from urllib.parse import urlencode
from tornado.testing import AsyncHTTPTestCase, gen_test

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

    @staticmethod
    def factory(name):
        return {
            'name': name,
            'climate': ["5be0622e08301fc814313d48"],
            'terrain': ["1be0663e18876fc814313d49"],
            'movie': ["3be0999e18876fc814313d23"],
        }

    @property
    def model(self):
        return Planet

    @gen_test
    async def test_validate_id_in_climate(self):
        body = planet('Validate climate Planet')
        body['climate'][0] = '12345'
        error = await self.request('', method='POST', body=urlencode(body))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_validate_id_in_terrain(self):
        body = planet('Validate terrain Planet')
        body['terrain'][0] = '54321'
        error = await self.request('', method='POST', body=urlencode(body))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @gen_test
    async def test_validate_id_in_movie(self):
        body = planet('Validate movie Planet')
        body['movie'][0] = '67890'
        error = await self.request('', method='POST', body=urlencode(body))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)
