from tornado.options import define, options

define('port', default=8000)
define('host', default='http://localhost:{0}'.format(options.port))
define('mongo_uri', default='mongodb://database:27017/')
define('mongo_database', default='star_wars')
