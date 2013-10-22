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

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'logar'),
                (Allow, 'g:admin', ALL_PERMISSIONS),
                (Allow, 'g:moderador', 'moderar'),
                (Allow, 'g:jogador', 'jogar'),
              ]
    def __init__(self, request):
        pass

class UserFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, nome):
        dbsession = DBSession()
        jog = dbsession.query(BdJogador).filter_by(nome=nome).first()
        jog.__parent__ = self
        jog.__name__ = nome
        return jog


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class BdJogador(Base):
    __tablename__ = 'jogadores'
    id = Column(Integer, primary_key=True)
    #id = Column(mysql.BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    nome = Column(Text, unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    partidas = Column(Integer, nullable=False)
    vitorias = Column(Integer, nullable=False)
    saidas = Column(Integer, nullable=False)
    pontos = Column(Integer, nullable=False)

    @property
    def __acl__(self):
        return [
            (Allow, self.nome, 'jogar'),
        ]

    def verif_senha(self, senha):
        return self.senha == senha

    def __init__(self, nome, senha, grupo="g:jogador"):
        self.nome = nome
        self.senha = senha
        self.partidas = 0
        self.vitorias = 0
        self.saidas = 0
        self.pontos = 0


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
