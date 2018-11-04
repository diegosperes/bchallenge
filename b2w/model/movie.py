from b2w.model.base import BaseModel


class Movie(BaseModel):
    @propert
    def data(self):
        return {'name': self.name}
