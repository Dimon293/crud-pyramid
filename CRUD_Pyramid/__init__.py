from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()

db_session = scoped_session(sessionmaker())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session.configure(bind=engine)
    Base.metadata.bind = engine

    with Configurator(settings=settings) as config:
        config.include('.user.views')
        config.include('.article.views')

        config.scan('.user.views')
        config.scan('.article.views')
    return config.make_wsgi_app()
