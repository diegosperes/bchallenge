from tornado.testing import AsyncTestCase

from tests.model import ModelTestCase
from b2w.model.terrain import Terrain


class TerrainModelTestCase(ModelTestCase, AsyncTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name
        }

    @property
    def model(self):
        return Terrain

    def test_get_collection(self):
        self.assertEqual('terrain', self.collection.name)
