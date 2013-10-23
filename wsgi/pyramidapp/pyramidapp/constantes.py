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


from pyramid.path import AssetResolver

asset = AssetResolver('pyramidapp')
resolver = asset.resolve("cartas")
# Diretório onde estão as informações das cartas
DIR_CARTAS = resolver.abspath()

# Número de cartas máximo na mão de cada jogador
MAX_CARTAS_MAO = 5

# Quantidade inicial de dinheiro para cada jogador
DINHEIRO_INICIAL = 5

# Número de cartas inicial para cada jogador
NUM_CARTAS_INICIAIS = 2

# Custo para comprar uma carta do monte de descerte
CUSTO_COMPRA_DESCARTE = 3

# Valor mínimo de uma carta para que ela possa ser descartada
VALOR_MINIMO_PARA_DESCARTE = 5
