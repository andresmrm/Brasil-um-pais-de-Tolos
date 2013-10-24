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

import unittest
import transaction

from pyramid import testing

from .models import DBSession
from .jogo import SistemaPreJogo

#class TestMyView(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        DBSession.configure(bind=engine)
#        Base.metadata.create_all(engine)
#        with transaction.manager:
#            model = MyModel(name='one', value=55)
#            DBSession.add(model)
#
#    def tearDown(self):
#        DBSession.remove()
#        testing.tearDown()
#
#    def test_it(self):
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info['one'].name, 'one')
#        self.assertEqual(info['project'], 'bpt')
#
#class TutorialViewTests(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#
#    def tearDown(self):
#        testing.tearDown()
#
#    def test_hello_world(self):
#        from tutorial import hello_world
#
#        request = testing.DummyRequest()
#        response = hello_world(request)
#        self.assertEqual(response.status_code, 200)


class Teste(unittest.TestCase):

    def inicializar_jogo(self):
        self.sist= SistemaPreJogo()
        self.sist.criar_jogo("jogoTeste","1")
        self.sist.colocar_jogador_jogo("jogoTeste","1")
        #self.sist.ret_jogador("legalzao").automatico = True
        self.sist.iniciar_jogo("jogoTeste")

        self.jogo = self.sist.ret_jogo("jogoTeste")
        #self.jogador = self.sist.ret_jogador("1")

    def ident_carta(self, tipo_carta):
        for iden, carta in self.jogo.baralho.items():
            if carta.imagem[:-4] == tipo_carta:
                return iden, carta
        self.fail()

    def dar_carta(self, nome_jogador, tipo_carta):
        jogador = self.sist.ret_jogador(nome_jogador)
        iden = self.ident_carta(tipo_carta)[0]
        jogador.mao.append(iden)

    def jogar_carta(self, nome_jogador, tipo_carta, param=None):
        jogador = self.sist.ret_jogador(nome_jogador)
        iden = self.ident_carta(tipo_carta)[0]
        resp = jogador.jogar_carta(iden, param)
        self.assertEqual(resp[:2], "Ok")

    def pegar_dinheiro(self, nome_jogador):
        jogador = self.sist.ret_jogador(nome_jogador)
        resp = jogador.pegar_dinheiro()
        self.assertEqual(resp[:2], "Ok")

    def pegar_carta(self, nome_jogador):
        jogador = self.sist.ret_jogador(nome_jogador)
        resp = jogador.mais_carta()
        self.assertEqual(resp[:2], "Ok")


class EfeitoPegarMaisCartas(Teste):
    def setUp(self):
        self.config = testing.setUp()

        self.inicializar_jogo()
        #self.carta_testada = self.ident_carta("esporte9")
        self.carta_testada = "esporte9"
        self.dar_carta("1", self.carta_testada)

        jogador = self.sist.ret_jogador("1")
        jogador.dinheiro = 100

    def tearDown(self):
        testing.tearDown()

    def teste_normal(self):
        self.jogar_carta("1", self.carta_testada)
        jogador = self.sist.ret_jogador("1")
        tam_mao1 = len(jogador.mao)
        self.pegar_carta("1")
        tam_mao2 = len(jogador.mao)
        self.assertEqual(tam_mao2-tam_mao1, 2)

    def teste_mao_quase_cheia(self):
        self.pegar_carta("1")
        jogador = self.sist.ret_jogador("1")
        tam_mao1 = len(jogador.mao)
        self.pegar_carta("1")
        tam_mao2 = len(jogador.mao)
        self.assertEqual(tam_mao2-tam_mao1, 1)
