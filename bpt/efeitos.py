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

class Efeito(object):
    exp = "^Nada acontece$"
    @staticmethod
    def executar(self, dados, dono):
        pass


class DinheiroMaioria(Efeito):
    exp = "^Jogador que tiver mais cartas (?P<tipo>\w+) (?P<naipe>\w+) baixadas na mesa (?P<acao>\w+) (?P<quant>\w+)\$$"
    @staticmethod
    def executar(dados, dono):
        """Da dinheiro para jogador com uma determinada maioria"""
        nome_jog = dono.jogo.maiorias.get(dados["naipe"].lower())
        if nome_jog != None:
            if dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            nomes = nome_jog[1]
            for nome in nomes:
                jog = dono.jogo.jogadores[nome]
                alteracao = int(sinal*int(dados["quant"])/len(nomes))
                jog.dinheiro += alteracao

class AlterarDinheiro(Efeito):
    exp = "^(?P<acao>\w+) (?P<quant>\w+)\$$"
    @staticmethod
    def executar(dados, dono):
        """Altera a quantidade de dinheiro do dono da carta"""
        if dados["acao"] == "perde":
            sinal = -1
        else:
            sinal = 1
        alteracao = int(sinal*int(dados["quant"]))
        dono.dinheiro += alteracao

class JogadorComMaisDinheiro(Efeito):
    exp = "^Caso seja o jogador com mais dinheiro, (?P<acao>\w+) (?P<quant>\w+)\$$"
    @staticmethod
    def executar(dados, dono):
        """Altera a quantidade de dinheiro do dono da carta"""
        if dono.dinheiro == dono.jogo.ret_jog_mais_dinheiro().dinheiro:
            if dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            alteracao = int(sinal*int(dados["quant"]))
            dono.dinheiro += alteracao

class RecebeCartasMonte(Efeito):
    exp = "^Recebe (?P<quant>\w+) cartas do monte$"
    @staticmethod
    def executar(dados, dono):
        """Dono da carta pega X cartas do monte"""
        for i in range(int(dados["quant"])):
            if len(dono.mao) < MAX_CARTAS_MAO:
                carta = dono.jogo.pegar_carta_monte()
                if carta != None:
                    dono.adi_carta(carta)
