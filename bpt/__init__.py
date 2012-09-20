from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from security import groupfinder

from .models import DBSession, UserFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings,
                          root_factory='.models.RootFactory')
    config.add_static_view('static', 'static', cache_max_age=3600)
    authn_policy = AuthTktAuthenticationPolicy(
        '39hrf3489h3[;32986jofn3][22}1w1!!##f4$', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('deform_static', 'deform:static')


    config.add_route('inicial', '/')
    config.add_route('central', '/central')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('enviar_msg', '/enviar_msg')
    config.add_route('ret_msgs', '/ret_msgs')

    config.add_route('jogo', '/jogo')
    config.add_route('baralho', '/baralho')
    config.add_route('jogada', '/jogada')
    config.add_route('atualizar', '/atualizar')

    config.add_route('criar_perfil', '/registrar')
    config.add_route('ver_perfil', '/ver_perfil/{nome}')
    config.add_route('editar_perfil', '/editar_perfil/{nome}',
                     factory=UserFactory, traverse="/{nome}")

    config.scan()
    return config.make_wsgi_app()
