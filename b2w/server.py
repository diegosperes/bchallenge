import tornado.ioloop
import tornado.web

from b2w.handler.movie import MovieHandler
from b2w.handler.climate import ClimateHandler
from b2w.handler.terrain import TerrainHandler
from b2w.handler.planet import PlanetHandler


def make_app():
    return tornado.web.Application([
        (r"/movie[/]?(\w+)?", MovieHandler),
        (r"/climate[/]?(\w+)?", ClimateHandler),
        (r"/terrain[/]?(\w+)?", TerrainHandler),
        (r"/planet[/]?(\w+)?", PlanetHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
