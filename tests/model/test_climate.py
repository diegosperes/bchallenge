from tornado.testing import AsyncTestCase

from tests.model import ModelTestCase
from b2w.model.climate import Climate


class ClimateModelTestCase(ModelTestCase, AsyncTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name
        }

    @property
    def model(self):
        return Climate

    def test_get_collection(self):
        self.assertEqual('climate', self.collection.name)
