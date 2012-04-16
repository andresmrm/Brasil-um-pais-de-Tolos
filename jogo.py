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

import os
import random


DIR_CARTAS = "cartas"
MAX_CARTAS_MAO = 5
NUM_CARTAS_INICIAIS = 2
DINHEIRO_INICIAL = 5


class Jogo():
    """Reune e centraliza o jogo"""

    def __init__(self):
        self.baralho = {}
        self.jogadores = []
        self.monte = []

    def adi_jogador(self, jog): 
        """Adiciona um jogador a lista de jogadores do jogo"""
        self.jogadores.append(jog)

    def montar_baralho(self):
        """Carrega as cartas e monta o monte inicial de cartas"""
        nomes_arqs = os.listdir(DIR_CARTAS)
        for nome in nomes_arqs:
            with open(os.path.join(DIR_CARTAS, nome)) as arq:
                linhas = arq.read().splitlines()
                atributos = {}
                for linha in linhas:
                    tipo, valor = linha.split(":")
                    atributos[tipo.strip()] = valor.strip()
                c = Carta(nome=atributos['nome'],
                          num=atributos['num'],
                          naipe=atributos['naipe'],
                          custo=atributos['custo'],
                          efeito=atributos['efeito'])
                self.baralho[len(self.baralho)] = c

    def distribuir_cartas(self):
        """Da as primeiras cartas para cada jogador"""
        for j in self.jogadores:
            for n in range(NUM_CARTAS_INICIAIS):
                j.adi_carta(self.monte.pop())

    def iniciar(self):
        """Faz as preparacoes iniciais para comecar o jogo"""
        self.montar_baralho()
        self.monte = list(self.baralho.keys())
        random.shuffle(self.monte)
        self.distribuir_cartas()


class Jogador():
    """Um jogador"""

    def __init__(self):
        self.nome = "Tolo"
        self.dinheiro = DINHEIRO_INICIAL
        self.mao = []
        self.mesa = {}
        self.pontos = 0

    def adi_carta(self, carta):
        """Adiciona uma carta a mao do jogador"""
        if len(self.mao) < MAX_CARTAS_MAO:
            self.mao.append(carta)

    def pegar_dinheiro(self):
        """Pega dinheiro da banca"""
        self.dinheiro += 2

class Carta():
    """Uma carta"""

    def __init__(self, nome="Boba", num=1, naipe="Azul", custo=1, efeito=None):
        self.nome = nome
        self.num = num
        self.naipe = naipe
        self.custo = custo
        self.efeito = efeito


if __name__  == '__main__':
    j = Jogo()
    j1 = Jogador()
    j2 = Jogador()
    j3 = Jogador()

    j.adi_jogador(j1)
    j.adi_jogador(j2)
    j.adi_jogador(j3)

    j.iniciar()
    j1.pegar_dinheiro()

    for jog in j.jogadores:
        print jog.mao
    print j.monte
