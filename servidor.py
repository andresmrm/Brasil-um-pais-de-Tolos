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
from slimish_jinja import SlimishExtension

from jogo import *


class BPT(Flask):
    jinja_options = Flask.jinja_options
    jinja_options['extensions'].append(SlimishExtension)

app = BPT(__name__)
app.debug = True

J = None

@app.route('/')
def rodar_jogo():
    #j1 = Jogador()
    #j1.nome = "Tolo1"
    #j1.mao = [1,2,3,4]
    #j1.pegar_dinheiro()
    #j1.mesa = { 'vermelho':[1,2,3,4,5,6,7,8,9],
    #            'azul':[1,2],
    #            'amarelo': [1],
    #            'verde': [1],
    #            'laranja': [1,4,6,8],
    #            'roxo':[1]} 
    #j2 = Jogador()
    #j2.nome = "Tolo2"
    #j3 = Jogador()
    #j3.nome = "Tolo3"
    #j3.mesa = { 'vermelho':[1,2,9],}
    #j4 = Jogador()
    #j4.nome = "Tolo4"
    #j5 = Jogador()
    #j5.nome = "Tolo5"
    #jogadores = [ j.__dict__ for j in [j1, j2, j3, j4, j5]]

    j = Jogo()
    global J
    J = j
    j1 = Jogador("Tolo1", j)
    j2 = Jogador("Tolo2", j)
    j3 = Jogador("Tolo3", j)

    j.iniciar()
    j1.mesa = { 'pol':[1,2,3,4,5,6,7,8,9],
                'fic':[1,2],
                'ent': [1],
                'soc': [1],
                'esp': [1,4,6,8],
                'lit':[1]} 

    jogadores = [ jog.__dict__ for jog in j.jogadores.values()]

    return render_template('jogo.slim',jogadores=jogadores,baralho=j.baralho)


@app.route('/jogada', methods=['POST'])
def jogada():
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    jogada = request.form["jogada"]
    return J.executar(jogador, cod, jogada)

@app.route('/baralho', methods=['GET'])
def enviar_baralho():
    cartas = {} 
    for c in J.baralho:
        cartas[c]  = J.baralho[c].__dict__ 
    return jsonify(cartas)

@app.route('/atualizar', methods=['POST'])
def enviar_atualizacao():
    jogador = request.form["jogador"]
    cod = request.form["cod"]
    num = request.form["num_jogada"]
    ret = J.ret_atualizacao(jogador, cod, num)
    if ret == "0":
        return ret
    else:
        jogadores = [ jog.__dict__ for jog in J.jogadores.values()]
        pa = render_template('mao.slim',jogadores=jogadores,baralho=J.baralho)
        ret["mao"] = pa
        return jsonify(ret)

if __name__  == '__main__':
    app.run()
