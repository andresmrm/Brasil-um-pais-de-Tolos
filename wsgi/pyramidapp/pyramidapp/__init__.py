#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2012 Quequeré
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from security import groupfinder

from .models import (
    UserFactory,
    initialize_sql
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # OpenShift Settings
    if os.environ.get('OPENSHIFT_DB_URL'):
        settings['sqlalchemy.url'] = \
            '%(OPENSHIFT_DB_URL)s%(OPENSHIFT_APP_NAME)s' % os.environ
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
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
    config.add_route('sala_central', '/sala/central/')
    config.add_route('atualizar_central', '/sala/central/atualizar')
    config.add_route('sala', '/sala/{nome}/')
    config.add_route('atualizar_sala', '/sala/{nome}/atualizar')
    config.add_route('pronto', '/sala/{nome}/pronto')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('enviar_msg', '/{tipo}/{nome}/enviar_msg')
    config.add_route('ret_msgs', '/{tipo}/{nome}/ret_msgs')

    config.add_route('jogo', '/jogo/{nome}/')
    config.add_route('baralho', '/jogo/{nome}/baralho')
    config.add_route('jogada', '/jogo/{nome}/jogada')
    config.add_route('atualizar_jogo', '/jogo/{nome}/atualizar')
    config.add_route('fim', '/jogo/{nome}/fim')

    config.add_route('rank', '/rank')

    config.add_route('criar_perfil', '/registrar')
    config.add_route('ver_perfil', '/ver_perfil/{nome}')
    config.add_route('editar_perfil', '/editar_perfil/{nome}',
                     factory=UserFactory, traverse="/{nome}")

    config.scan()
    return config.make_wsgi_app()
