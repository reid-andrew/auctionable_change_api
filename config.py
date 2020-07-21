import os
basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


# import .env variables for DB connection
# TODO: Unify these ENV variables by pulling from different dot files
def get_env_db_url(env_setting):
    if env_setting == "development":
        POSTGRES_USER = get_env_variable("DEV_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("DEV_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("DEV_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("DEV_POSTGRES_DB")
    elif env_setting == "testing":
        POSTGRES_USER = get_env_variable("TESTING_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("TESTING_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("TESTING_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("TESTING_POSTGRES_DB")
    elif env_setting == "production":
        POSTGRES_USER = get_env_variable("PROD_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("PROD_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("PROD_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("PROD_POSTGRES_DB")

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    # SECRET = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BUNDLE_ERRORS = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    BUNDLE_ERRORS = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
