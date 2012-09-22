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

import time


class SistemaPreJogo():

    def __init__(self, sist_chat):
        self.salas = {}
        self.pre_jogs = {}
        self.sist_chat = sist_chat
        
        self.central = 'central'
        self.criar_sala(self.central, None)

    def criar_sala(self, nome, jog):
        r = False
        if self.salas.get(nome) == None:
            self.sist_chat.criar_sala(nome)
            s = SalaPreJogo(nome)
            self.salas[nome] = s
            r = True
        if jog:
            self.colocar_jog_sala(nome, jog)
            r = True
        return r

    def ret_sala(self, nome):
        return self.salas.get(nome)

    def ret_salas(self):
        r = []
        for s in self.salas.values():
            if s.nome != 'central':
                r.append(s)
        return r

    def colocar_jog_sala(self, sala, jog):
        """Coloca um jogador em uma determinada sala"""
        if not sala:
            self.pre_jogs['jog'] = None
            return True

        s = self.salas.get(sala)
        # Verifica se a sala existe
        if not s:
            return False

        j = self.pre_jogs.get(jog)
        if not j:
            self.pre_jogs[jog] = PreJogador(jog, sala)
        else:
            j.trocar_sala(sala)
        s.adi_jog(jog)
        return True

    def rem_jog(self, sala, jog):
        s = self.salas[sala]
        s.rem_jog(jog)
        if s.vazia() and sala != self.central:
            self.fechar_sala(nome)

    def ret_jog(self, nome):
        return self.pre_jogs.get(nome)

    def ret_jogs(self, sala):
        self.salas[sala].ret_jogs()

    def fechar_sala(self, nome):
        s = self.salas[nome]
        jogs = s.ret_jogs()
        for jog in jogs:
            self.pre_jogs[jog].trocar_sala(self.central)
        self.salas[nome] = None
        self.sist_chat.fechar_sala(nome)


class SalaPreJogo():

    def __init__(self, nome):
        self.nome = nome
        self.jogs = []

    def adi_jog(self, jog):
        self.jogs.append(jog)

    def rem_jog(self, jog):
        self.jogs.pop(jog)

    def ret_jogs(self):
        return self.jogs

    def vazia(self):
        if len(self.jogs) == 0:
            return True
        return False


class PreJogador():
    
    def __init__(self, nome, sala):
        self.nome = nome
        self.sala = sala
        self.ult_contato = 0
        self.novo_contato()

    def novo_contato(self):
        self.ult_contato = time.time()

    def trocar_sala(self, sala):
        self.sala = sala
        self.novo_contato()
