import importlib, os
from tornado.options import options
importlib.import_module('b2w.settings.' + os.environ.get('ENV', None)) 

from urllib.parse import urlencode


def uri(model, _id, **kwargs):
    route = model.collection().name
    uri = '{0}/{1}'.format(options.host, route)
    if _id:
        uri += '/{0}'.format(_id)
    if kwargs:
        uri += '?{0}'.format(urlencode(kwargs))
    return uri
