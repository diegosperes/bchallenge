from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.terrain import Terrain


class TerrainHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name
        }

    @property
    def model(self):
        return Terrain
