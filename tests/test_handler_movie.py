from tornado.testing import AsyncHTTPTestCase

from base import HandlerTestCase
from b2w.model.movie import Movie


class MovieHandlerTestCase(HandlerTestCase, AsyncHTTPTestCase):

    @staticmethod
    def factory(name):
        return {
            "name": name
        }

    @property
    def model(self):
        return Movie
