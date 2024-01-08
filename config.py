class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    FLASK_ENV = 'production'

class TestingConfig(Config):
    TESTING = True
