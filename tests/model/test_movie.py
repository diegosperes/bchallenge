from tornado.testing import AsyncTestCase

from tests.model import ModelTestCase
from b2w.model.movie import Movie


class MovieModelTestCase(ModelTestCase, AsyncTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name,
            "director": "director",
            "producer": ["producer"],
            "released": "2017-08-09"
        }

    @property
    def model(self):
        return Movie

    def test_get_collection(self):
        self.assertEqual('movie', self.collection.name)
