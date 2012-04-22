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
    """Reune e centraliza os elementos do jogo"""

    def __init__(self):
        self.baralho = {}
        self.jogadores = {}
        self.monte = []
        self.jogador_atual = None
        self.num_jogada = 0

    def adi_jogador(self, jog): 
        """Adiciona um jogador a lista de jogadores do jogo"""
        self.jogadores[jog.nome] = jog

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
                          custo=int(atributos['custo']),
                          efeito=atributos['efeito'])
                self.baralho[len(self.baralho)] = c

    def distribuir_cartas(self):
        """Da as primeiras cartas para cada jogador"""
        for j in self.jogadores.values():
            for n in range(NUM_CARTAS_INICIAIS):
                j.adi_carta(self.monte.pop())

    def iniciar(self):
        """Faz as preparacoes iniciais para comecar o jogo"""
        self.montar_baralho()
        self.monte = list(self.baralho.keys())
        random.shuffle(self.monte)
        self.distribuir_cartas()
        self.jogador_atual = self.jogadores.keys()[0]

    def pegar_carta_monte(self):
        """Tira uma carta no monte"""
        if len(self.monte) == 0:
            return None

        return self.monte.pop()

    def prox_jogador(self):
        """Passa a vez de jogar para o proximo jogador"""
        nomes = self.jogadores.keys()
        if self.jogador_atual == nomes[-1]:
            self.jogador_atual = nomes[0]
        else:
            num = nomes.index(self.jogador_atual)
            self.jogador_atual = nomes[num+1]
        self.num_jogada += 1

        # Roda IA caso jogador esteja em modo automatico
        j = self.jogadores[self.jogador_atual]
        if j.automatico == True:
            j.jogada_automatica()




class Jogador():
    """Um jogador"""

    def __init__(self, nome, jogo):
        self.nome = nome
        self.dinheiro = DINHEIRO_INICIAL
        self.mao = []
        self.mesa = {}
        self.pontos = 0
        self.cod = "teste"
        self.jogo = jogo
        self.automatico = False
        jogo.adi_jogador(self)

    def adi_carta(self, carta):
        """Adiciona uma carta a mao do jogador"""
        if len(self.mao) < MAX_CARTAS_MAO:
            self.mao.append(carta)

    def jogar_carta(self, iden):
        """Joga uma carta da mao para a mesa"""
        try:
            iden = int(iden)
        except:
            return "ERRO: Identificador da carta nao e numero valido!"

        if iden not in self.mao:
            return "ERRO: Jogador nao tem essa carta na mao!"

        carta = self.jogo.baralho.get(iden)
        if carta == None:
            return "ERRO: Carta nao existe no baralho!"

        if self.dinheiro < carta.custo:
            return "ERRO: Dinheiro insuficiente para baixar carta!"
        self.dinheiro -= carta.custo

        self.mao.remove(iden)
        if self.mesa.get(carta.naipe) == None:
            self.mesa[carta.naipe] = []
        self.mesa[carta.naipe] += [iden]
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"
            
    def pegar_dinheiro(self):
        """Pega dinheiro da banca"""
        self.dinheiro += 2
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def mais_carta(self):
        """Pega uma carta do monte"""
        if len(self.mao) >= 5:
            return "ERRO: Mao cheia!"

        carta = self.jogo.pegar_carta_monte()
        if carta == None:
            return "ERRO: O monte acabou!"

        self.mao.append(carta)
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def jogada_automatica(self):
        """Faz uma jogada automatica"""
        self.pegar_dinheiro()

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
    j1 = Jogador("Tolo1",j)
    j2 = Jogador("Tolo2",j)
    j3 = Jogador("Tolo3",j)

    j.iniciar()
    j1.pegar_dinheiro()

    for jog in j.jogadores:
        print jog.mao
    print j.monte
