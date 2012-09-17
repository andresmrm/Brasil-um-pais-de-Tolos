from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)


    config.add_static_view('deform_static', 'deform:static')


    config.add_route('home', '/')
    config.add_route('login', 'login')
    config.add_route('teste', '')
    config.add_route('atualizar', 'atualizar')
    config.add_route('baralho', 'baralho')
    config.add_route('jogada', 'jogada')
    config.add_route('form', 'form')
    config.add_route('criar_perfil', 'registrar')
    config.add_route('editar_perfil', 'editar_perfil/{nome}')
    config.add_route('ver_perfil', 'ver_perfil/{nome}')
    config.scan()
    return config.make_wsgi_app()
