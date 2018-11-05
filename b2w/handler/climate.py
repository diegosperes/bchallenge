from b2w.handler.base import Handler
from b2w.model.climate import Climate


class ClimateHandler(Handler):

    @property
    def model(self):
        return Climate
