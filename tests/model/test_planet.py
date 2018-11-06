from urllib.parse import urlencode
from tornado.testing import AsyncTestCase, gen_test

from tests.model import ModelTestCase
from b2w.model.planet import Planet


class PlanetModelTestCase(ModelTestCase, AsyncTestCase):

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

    def test_get_collection(self):
        self.assertEqual('planet', self.collection.name)
