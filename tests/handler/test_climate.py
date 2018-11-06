from tornado.testing import AsyncHTTPTestCase

from tests.handler import HandlerTestCase
from b2w.model.climate import Climate


class ClimateHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name
        }

    @property
    def model(self):
        return Climate
