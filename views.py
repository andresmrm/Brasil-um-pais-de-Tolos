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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Jogador,
    )

from jogo import *


CONTROLADOR = None


class Controlador():
    """Controla e faz o jogo rodar"""

    def __init__(self):
        self.jogo = None
        self.inicializar()
        print("Montando")

    def inicializar(self):
        self.jogo = Jogo()
        j = self.jogo
        j1 = Jogador("Tolo1", j)
        j2 = Jogador("ZOrnitorrinco Voador", j)
        j2.automatico = True
        j3 = Jogador("Tolo3", j)
        j3.automatico = True

        j.iniciar()
        #j1.mesa = { 'pol':[1,2,3,4,5,6,7,8,9],
        #            'fic':[1,2],
        #            'ent': [1],
        #            'soc': [1],
        #            'esp': [1,4,6,8],
        #            'lit':[1]} 

    def ret_jogadores(self):
        """Retorna uma lista com os dados dos jogadores em dicionarios"""
        jogs = [ jog.__dict__ for jog in self.jogo.jogadores.values()]
        for j in jogs:
            j["tam_mao"] = len(j["mao"])
        return jogs

    def ret_atualizacao(self, nome_jog, cod, num):
        """Retorna dicionario com atualizacoes a serem feitas na interface"""
        try:
            num = int(num)
        except:
            return "ERRO: Numero da jogada nao e numero valido!"

        if num == self.jogo.num_jogada:
            return "0"

        resposta = self.validar_jogador(nome_jog, cod)
        if resposta != True:
            return resposta

        dicio = {}
        dicio["num_jogada"] = self.jogo.num_jogada
        dicio["mao"] = self.jogo.jogadores[nome_jog].mao
        dicio["mesas"] = "A"
        return dicio

    def validar_jogador(self, nome_jog, cod):
        """Verifica se um jogador existe e se seu codigo bate"""
        jog = self.jogo.jogadores.get(nome_jog)
        if jog == None:
            return "ERRO: Jogador nao encontrado!"

        if jog.cod != cod:
            return "ERRO: Codigo nao bate!"

        return True

    def executar(self,nome_jog, cod, jogada):
        """Exucuta uma jogada de um jogador"""
        try:
            if jogada[0] == 'R':
                self.inicializar()
                return "Ok"
        except:
            pass

        resposta = self.validar_jogador(nome_jog, cod)
        if resposta != True:
            return resposta
        jog = self.jogo.jogadores.get(nome_jog)

        if jog.nome != self.jogo.jogador_atual:
            return "ERRO: Nao e a sua vez de jogar!"

        if len(jogada) < 2:
            return "ERRO: Jogada muito curta para processar!"

        tipo, iden = jogada[0], jogada[1:]
        if tipo == 'J':
            return jog.jogar_carta(iden)
        elif tipo == 'C':
            return jog.comprar_carta(iden)
        elif tipo == 'D':
            return jog.descartar_carta(iden)
        elif tipo == 'G':
            return jog.pegar_dinheiro()
        elif tipo == 'M':
            return jog.mais_carta()

        return "ERRO: Jogada nao identificada!" 

    def nova_pagina(self):
        jogadores = self.ret_jogadores()
        descarte = self.jogo.descarte
        baralho = self.jogo.baralho
        return {'jogadores':jogadores, 'descarte':descarte, 'baralho':baralho}

    def nova_atualizacao(self, jogador, cod, num):
        ret = self.ret_atualizacao(jogador, cod, num)
        if ret == "0":
            return ret
        else:
            j = self.ret_jogadores()
            b = self.jogo.baralho
            d = self.jogo.descarte
            pa = render_template('mao.slim',jogadores=j,baralho=b)
            ret["mao"] = pa
            pa = render_template('mesas.slim',jogadores=j,baralho=b, descarte=d)
            ret["mesas"] = pa
            return jsonify(ret)


CONTROLADOR = Controlador()


# PREPARACAO
#@view_config(route_name='login', renderer='login.slim')
#def pagina_login(request):
#    return {}
#
#@view_config(route_name='lobby', renderer='lobby.slim')
#def lobby(request):
#    return {}


# JOGO
@view_config(route_name='home', renderer='jogo.slim')
def nova_pagina(request):
    return CONTROLADOR.nova_pagina()

#@app.route('/jogada', methods=['POST'])
def nova_jogada(request):
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    jogada = request.form["jogada"]
    return CONTROLADOR.executar(jogador, cod, jogada)

#@app.route('/atualizar', methods=['POST'])
def enviar_atualizacao(request):
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    num = request.form["num_jogada"]
    return CONTROLADOR.nova_atualizacao(jogador, cod, num)

#@app.route('/baralho', methods=['GET'])
def enviar_baralho(request):
    cartas = {} 
    for c in CONTROLADOR.jogo.baralho:
        cartas[c] = dict(CONTROLADOR.jogo.baralho[c].__dict__)
        cartas[c].pop("efeito")
        cartas[c].pop("efeito_dados")
    return jsonify(cartas)




#@view_config(route_name='home', renderer='templates/mytemplate.pt')
#def my_view(request):
#    try:
#        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one':one, 'project':'bpt'}
#
#
#@view_config(route_name='teste', renderer='teste.slim')
#def teste(request):
#    return {'one':'1', 'project':'bpt'}
