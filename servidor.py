#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2012 Qerereque
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

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from slimish_jinjaBR import SlimishExtension

from jogo import *


class BPT(Flask):
    jinja_options = Flask.jinja_options
    jinja_options['extensions'].append(SlimishExtension)


CONTROLADOR = None
app = BPT(__name__)
app.debug = True


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
        if tipo == 'C':
            return jog.jogar_carta(iden)
        if tipo == 'D':
            return jog.pegar_dinheiro()
        if tipo == 'M':
            return jog.mais_carta()

        return "ERRO: Jogada nao identificada!" 

    def nova_pagina(self):
        jogadores = self.ret_jogadores()
        baralho = self.jogo.baralho
        return render_template('jogo.slim',jogadores=jogadores,baralho=baralho)

    def nova_atualizacao(self, jogador, cod, num):
        ret = self.ret_atualizacao(jogador, cod, num)
        if ret == "0":
            return ret
        else:
            j = self.ret_jogadores()
            b = self.jogo.baralho
            pa = render_template('mao.slim',jogadores=j,baralho=b)
            ret["mao"] = pa
            pa = render_template('mesas.slim',jogadores=j,baralho=b)
            ret["mesas"] = pa
            return jsonify(ret)


CONTROLADOR = Controlador()


# PREPARACAO
@app.route('/login')
def pagina_login():
    return render_template('login.slim',encoding = 'utf-8')

@app.route('/lobby')
def lobby():
    return "blah"


# JOGO
@app.route('/')
def nova_pagina():
    return CONTROLADOR.nova_pagina()

@app.route('/jogada', methods=['POST'])
def nova_jogada():
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    jogada = request.form["jogada"]
    return CONTROLADOR.executar(jogador, cod, jogada)

@app.route('/atualizar', methods=['POST'])
def enviar_atualizacao():
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    num = request.form["num_jogada"]
    return CONTROLADOR.nova_atualizacao(jogador, cod, num)

@app.route('/baralho', methods=['GET'])
def enviar_baralho():
    cartas = {} 
    for c in CONTROLADOR.jogo.baralho:
        cartas[c]  = CONTROLADOR.jogo.baralho[c].__dict__ 
    return jsonify(cartas)

if __name__  == '__main__':
    app.run()
