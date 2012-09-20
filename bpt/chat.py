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

    def __init__(self):
        self.salas = {}

    def criar_sala(self, nome):
        self.salas[nome] = Sala(nome)

    def adi_msg(self, sala, jog, msg):
        return self.salas[sala].adi_msg(jog, msg)

    def ret_msgs(self, sala, quant=20):
        return self.salas[sala].ret_msgs(quant)

    def fechar_sala(self, nome):
        self.salas[nome] = None


class Sala():

    def __init__(self, nome):
        self.nome = nome
        self.msgs = []

    def adi_msg(self, jog, msg):
        self.msgs.append("%s: %s" % (jog, msg))
        return len(self.msgs)

    def ret_msgs(self, quant):
        return self.msgs[-quant:]
