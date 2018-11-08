import json
from urllib.parse import urlencode
from tornado.testing import AsyncHTTPTestCase, gen_test

from tests.handler import HandlerTestCase, database
from b2w.model.planet import Planet
from b2w.model.movie import Movie


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

    def tearDown(self):
        super().tearDown()
        Movie.collection().drop()

    @gen_test
    async def test_validate_id_in_movie(self):
        body = self.factory('Validate movie Planet')
        body['movie'][0] = '67890'
        error = await self.request('', method='POST', body=urlencode(body))
        self.assertEqual(400, error.response.code)
        self.assertEqual(b'{}', error.response.body)

    @database('Gold')
    async def test_lookup_when_movie_does_not_exist(self, _ids):
        expected = self.factory('Gold ')
        response = await self.request(_ids[0], method='GET')
        result = json.loads(response.body)

        self.assertEqual(200, response.code)
        self.assertEqual(expected['name'], result['name'])
        self.assertEqual(expected['climate'], result['climate'])
        self.assertEqual(expected['terrain'], result['terrain'])
        self.assertEqual([], result['movie'])
        self.assertTrue(result['id'])

    @database('Platinum')
    async def test_lookup_when_movie_exist(self, _ids):
        name = 'Platinum '
        expected = self.factory(name)
        await self.add_valid_movie(_ids[0], name)
        response = await self.request(_ids[0], method='GET')
        result = json.loads(response.body)

        self.assertEqual(200, response.code)
        self.assertEqual(expected['name'], result['name'])
        self.assertEqual(expected['climate'], result['climate'])
        self.assertEqual(expected['terrain'], result['terrain'])
        self.assertEqual(name, result['movie'][0]['name'])
        self.assertTrue(result['movie'][0]['id'])
        self.assertTrue(result['id'])

    async def add_valid_movie(self, planet_id, movie_name):
        movie = Movie(**{"name": movie_name})
        await movie.insert()
        planet = await Planet.find(_id=planet_id)
        planet.movie.append(movie._id)
        await planet.update()
