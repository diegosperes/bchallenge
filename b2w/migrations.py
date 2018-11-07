import json
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from b2w.model.planet import Planet
from b2w.model.terrain import Terrain
from b2w.model.climate import Climate
from b2w.model.movie import Movie


terrains = set()
climates = set()
planets = []
movies = set()


async def get_value(url):
    response = await AsyncHTTPClient().fetch(url)
    result = json.loads(response.body)
    return result['title']


async def append(_set, values, url=False):
    result = []
    values = values.split(',') if type(values) is str else values
    for value in values:
        value.strip()
        if url:
            value = await get_value(value)
        value = value.strip()
        _set.add(value)
        result.append(value)
    return result


async def find_id(model, value):
    try:
        return (await model.find(name=value))._id
    except TypeError:
        pass


async def run():
    next_url = 'https://swapi.co/api/planets/'
    while next_url:
        response = await AsyncHTTPClient().fetch(next_url)
        result = json.loads(response.body)
        for planet in result['results']:
            terrain = await append(terrains, planet['terrain'])
            climate = await append(climates, planet['climate'])
            movie = await append(movies, planet['films'], url=True)
            document = {'name': planet['name'], 'terrain': terrain, 'climate': climate, 'movie': movie}
            planets.append(document)
        next_url = result['next']

    for terrain in terrains:
        await Terrain(name=terrain).insert()

    for climate in climates:
        await Climate(name=climate).insert()

    for movie in movies:
        await Movie(name=movie).insert()

    for planet in planets:
        planet['terrain'] = [await find_id(Terrain, terrain) for terrain in planet['terrain']]
        planet['climate'] = [await find_id(Climate, climate) for climate in planet['climate']]
        planet['movie'] = [await find_id(Movie, movie) for movie in planet['movie']]
        await Planet(**planet).insert()


if __name__ == '__main__':
    loop = IOLoop.current()
    loop.run_sync(run)
