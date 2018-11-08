import importlib, os
from tornado.options import options
importlib.import_module('b2w.settings.' + os.environ.get('ENV', None)) 
