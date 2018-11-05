from b2w.handler.base import Handler
from b2w.model.movie import Movie


class MovieHandler(Handler):

    @property
    def model(self):
        return Movie
