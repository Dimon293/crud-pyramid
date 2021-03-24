from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from cc_starter.models.meta import db_session, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    db_session.configure(bind=engine)
    Base.metadata.bind = engine

    with Configurator(settings=settings) as config:
        config.include('.routes')
        config.include('.models')
        config.scan('.views')
    return config.make_wsgi_app()