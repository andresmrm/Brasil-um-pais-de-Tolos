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

class SistemaChat():
    """Reúne e gerencia as salas de chat"""

    def __init__(self):
        self.salas = {}

    def criar_sala(self, nome):
        """Cria uma sala de nome 'nome'"""
        sala = self.salas.get(nome)
        if not sala:
            self.salas[nome] = SalaChat(nome)
        else:
            print("Erro(criar_sala - SistemaChat): Sala %s ja existe", nome)

    def adi_msg(self, nome_sala, nome_jogador, msg):
        """Adiciona a mensagem 'msg' à sala de nome 'nome_sala' sendo
        'nome_jogador' o autor"""
        sala = self.salas.get(nome_sala)
        if sala:
            return sala.adi_msg(nome_jogador, msg)
        else:
            print("Erro(adi_msg - SistemaChat): Sala %s nao existe", nome_sala)

    def ret_msgs(self, nome, quant=20):
        """Retorna 'quant' mensagens da sala de nome 'nome'"""
        sala = self.salas.get(nome)
        if sala:
            return sala.ret_msgs(quant)
        else:
            print("Erro(ret_msg - SistemaChat): Sala %s nao existe", nome)
            return []

    def fechar_sala(self, nome):
        """Fecha a sala de nome 'nome'"""
        sala = self.salas.get(nome)
        if sala:
            self.salas.pop(nome)
        else:
            print("Erro(fechar_sala - SistemaChat): Sala %s nao existe", nome)


class SalaChat():
    """Guarda o nome de uma sala e suas mensagens"""

    def __init__(self, nome):
        self.nome = nome
        self.msgs = []

    def adi_msg(self, jog, msg):
        """Adiciona uma mensagem à sala e returna o número de mensagens nessa
        sala"""
        self.msgs.append("%s: %s" % (jog, msg))
        return len(self.msgs)

    def ret_msgs(self, quant):
        """Returna as 'quant' últimas mensagens dessa sala"""
        return self.msgs[-quant:]
