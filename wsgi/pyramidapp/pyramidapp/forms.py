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

import deform
import colander
from deform import Form

from .models import DBSession, BdJogador


def record_to_appstruct(self):
    form =  formulador(FormRegistrar,('Registrar',))
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])

def merge_session_with_post(session, post):
    for key,value in post:
        setattr(session, key, value)
    return session

def formulador(form, botoes):
    f = {"form":Form(form(),buttons=botoes).render()}
    return f

def verif_nome_unico(nome):
    dbsession = DBSession()
    j = dbsession.query(BdJogador).filter_by(nome=nome).first()
    if j == None:
        return True
    else:
        return False


class FormLogin(colander.MappingSchema):
    nome = colander.SchemaNode(colander.String(),
                        description='Digite seu nome de usuário')
    senha = colander.SchemaNode(
                        colander.String(),
                        validator=colander.Length(min=5, max=100),
                        widget=deform.widget.PasswordWidget(size=20),
                        description='Digite sua senha')

class FormRegistrar(colander.MappingSchema):
    nome = colander.SchemaNode(colander.String(),
                        validator=colander.Function(verif_nome_unico,"Nome existe"),
                        description='Digite seu nome de usuário')
    senha = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(min=5),
                widget=deform.widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
    #email = colander.SchemaNode(
                #colander.String(),
                #validator=colander.Email('Email inválido'))

class FormEditar(colander.MappingSchema):
    senha = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(min=5),
                widget=deform.widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
#    email = colander.SchemaNode(
#                colander.String(),
#                validator=colander.Email('Email inválido'))
