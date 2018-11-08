from tornado.options import define, options

define('port', default=8000)
define('host', default='http://localhost:{0}'.format(options.port))
define('mongo_uri', default='mongodb://localhost:27017/')
define('mongo_database', default='test_database')
