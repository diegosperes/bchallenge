from b2w.model.base import BaseModel


class Movie(BaseModel):
    @property
    def data(self):
        return {'name': self.name}
