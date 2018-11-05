import tornado.ioloop
import tornado.web

from b2w.handler.movie import MovieHandler
from b2w.handler.climate import ClimateHandler
from b2w.handler.terrain import TerrainHandler


def make_app():
    return tornado.web.Application([
        (r"/movie[/]?(\w+)?", MovieHandler),
        (r"/climate[/]?(\w+)?", ClimateHandler),
        (r"/terrain[/]?(\w+)?", TerrainHandler),
    ])
