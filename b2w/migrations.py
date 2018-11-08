import json
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from b2w.model.planet import Planet
from b2w.model.movie import Movie
import pymongo


planets = []
movies = {}


async def get_value(url):
    response = await AsyncHTTPClient().fetch(url)
    return json.loads(response.body)


def normalize(values):
    values = values.split(',') if type(values) is str else values
    return [value.strip() for value in values]


async def append_from_url(_dict, values):
    result = []
    values = values.split(',') if type(values) is str else values
    for value in values:
        value = await get_value(value)
        title = value['title']
        movies[title] = value
        result.append(title)
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
            terrain = normalize(planet['terrain'])
            climate = normalize(planet['climate'])
            movie = await append_from_url(movies, planet['films'])
            document = {'name': planet['name'], 'terrain': terrain, 'climate': climate, 'movie': movie}
            planets.append(document)
        next_url = result['next']

    Movie.collection().create_index([("name", pymongo.TEXT)])
    for movie in movies.values():
        movie['name'] = movie['title']
        movie['released'] = movie['release_date']
        movie['producer'] = normalize(movie['producer'])
        await Movie(**movie).insert()

    Planet.collection().create_index([("name", pymongo.TEXT)])
    for planet in planets:
        planet['movie'] = [await find_id(Movie, movie) for movie in planet['movie']]
        await Planet(**planet).insert()


if __name__ == '__main__':
    loop = IOLoop.current()
    loop.run_sync(run)
