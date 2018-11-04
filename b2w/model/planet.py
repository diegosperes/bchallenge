from b2w.model.base import BaseModel


class Planet(BaseModel):
    @property
    def data(self):
        return {'name': self.name, 'climate': self.climate, 'terrain': self.terrain}
