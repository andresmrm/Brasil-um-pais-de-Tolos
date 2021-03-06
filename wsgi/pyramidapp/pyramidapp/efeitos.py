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

from constantes import *
from random import choice, randint


class Efeito(object):
    exp = "^Nada acontece$"
    @classmethod
    def descer(cls, carta, dono, params):
        pass
    @classmethod
    def perder(cls, dono, carta):
        pass

class Permanente(object):
    @classmethod
    def descer(cls, carta, dono, params):
        dono.adi_especial(cls.especial, carta)
    @classmethod
    def perder(cls, dono, carta):
        dono.rem_especial(cls.especial, carta)

class Nada(Efeito):
    exp = "^Nada acontece$"

class DinheiroMaioria(Efeito):
    exp = "^Jogador que tiver mais cartas (?P<tipo>\w+) (?P<naipe>\w+) baixadas na mesa (?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, carta, dono, params):
        """Da dinheiro para jogador com uma determinada maioria"""
        nome_jog = dono.jogo.maiorias.get(carta.efeito_dados["naipe"].lower())
        if nome_jog != None:
            if carta.efeito_dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            nomes = nome_jog[1]
            for nome in nomes:
                jog = dono.jogo.jogadores[nome]
                alteracao = int(sinal*int(carta.efeito_dados["quant"])/len(nomes))
                jog.dinheiro += alteracao

class DinheiroPorCarta(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ pra cada carta (?P<tipo>\w+) (?P<naipe>\w+) que o jogador tiver baixado na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        naipe = carta.efeito_dados["naipe"].lower()
        l = dono.mesa.get(naipe)
        if l:
            num = len(l)
            dono.dinheiro += int(carta.efeito_dados["quant"]) * num

class DinheiroPorCartaAlheia(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ pra cada carta (?P<tipo>\w+) (?P<naipe>\w+) que outros jogadores tiverem na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        num = 0
        naipe = carta.efeito_dados["naipe"].lower()
        for j in dono.jogo.jogadores.values():
            l = j.mesa.get(naipe)
            if l:
                num += len(l)
        dono.dinheiro += int(carta.efeito_dados["quant"]) * num

class AlterarDinheiro(Efeito):
    exp = "^(?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, carta, dono, params):
        """Altera a quantidade de dinheiro do dono da carta"""
        if carta.efeito_dados["acao"] == "perde":
            sinal = -1
        else:
            sinal = 1
        alteracao = int(sinal*int(carta.efeito_dados["quant"]))
        dono.dinheiro += alteracao

class JogadorComMaisDinheiro(Efeito):
    exp = "^Caso seja o jogador com mais dinheiro, (?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, carta, dono, params):
        """Altera a quantidade de dinheiro do dono da carta"""
        dados = carta.efeito_dados
        if dono.dinheiro == dono.jogo.ret_jog_mais_dinheiro().dinheiro:
            if dados["acao"] == "perde":
                sinal = -1
            else:
                sinal = 1
            alteracao = int(sinal*int(dados["quant"]))
            dono.dinheiro += alteracao

class RecebeCartasMonte(Efeito):
    exp = "^Recebe (?P<quant>\w+) cartas do monte$"
    @classmethod
    def descer(cls, carta, dono, params):
        """Dono da carta pega X cartas do monte"""
        dados = carta.efeito_dados
        for i in range(int(dados["quant"])):
            if len(dono.mao) < MAX_CARTAS_MAO:
                carta = dono.jogo.pegar_carta_monte()
                if carta != None:
                    dono.adi_carta(carta)

class VantagemEmpateNaipe(Permanente, Efeito):
    exp = "^Vantagem na maioria em caso de empate de cartas deste naipe$"
    especial = "calculo_maioria"
    @classmethod
    def executar(cls, dados, dono, carta):
        if dados["naipe"] == carta.naipe:
            dados["quant"] += 0.5

class RecebeDinheiroPorMaiorias(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ pra cada naipe que tiver maioria na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        dono.dinheiro += int(carta.efeito_dados["quant"]) * len(dono.maiorias)

class RecebeNaipesDiferentes(Efeito):
    exp = "^Recebe (?P<quant>\w+)\$ para cada 2 naipes diferentes que tiver cartas na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        dono.dinheiro += int(carta.efeito_dados["quant"]) * int(len(dono.mesa)/2)

class ExcluiAleatoriamenteCartasDosOutros(Efeito):
    exp = "^O jogador exclui aleatoriamente uma carta na m\wo de todos os outros jogadores$"
    @classmethod
    def descer(cls, carta, dono, params):
        for j in dono.jogo.jogadores.values():
            if j != dono:
                escolha = choice(j.mao)
                if escolha:
                    j.mao.remove(escolha)
                    #j.jogo.receber_descarte(escolha)

class DinheiroMoeda(Efeito):
    exp = "^Joga uma moeda, escolhe cara ou coroa, se acertar ganha (?P<quant1>\w+)\$, se errar perde (?P<quant2>\w+)\$$"
    @classmethod
    def descer(cls, carta, dono, params):
        moeda = randint(0, 1)
        if moeda:
            dono.dinheiro += int(carta.efeito_dados["quant1"])
        else:
            dono.dinheiro -= int(carta.efeito_dados["quant2"])
        if dono.dinheiro < 0:
            dono.dinheiro = 0

class DinheiroDado(Efeito):
    exp = "^Joga-se um dado, o jogador ganha dinheiro equivalente a (?P<quant>\w+) vezes o valor, caso saia 6 n\wo ganha nada$"
    @classmethod
    def descer(cls, carta, dono, params):
        dado = randint(1, 6)
        if dado != 6:
            dono.dinheiro += int(carta.efeito_dados["quant"]) * dado

class ExcluiCartasJogadorMenosPontos(Efeito):
    exp = "^Excluir todas as cartas do jogador com menos pontos$"
    @classmethod
    def descer(cls, carta, dono, params):
        jogador_menos_pontos = None
        pontos = 1000
        for j in dono.jogo.jogadores.values():
            if j.pontos < pontos:
                jogador_menos_pontos = j
                pontos = j.pontos
        jogador_menos_pontos.mao = []
        for naipe in jogador_menos_pontos.mesa.values():
            for iden in naipe:
                c = dono.jogo.baralho.get(iden)
                naipe.remove(iden)
                c.efeito.perder(dono, c)

class OutrosPerdemDinheiro(Efeito):
    exp = "^Caso tenha (?P<quant>\w+) pts a mais do que qualquer um dos demais jogadores, o jogo termina e voc\w vence$"
    @classmethod
    def descer(cls, carta, dono, params):
        vencer = True
        for j in dono.jogo.jogadores.values():
            if j != dono and (dono.pontos-j.pontos) < carta.efeito_dados["quant"]:
                vencer = False
        if vencer:
            dono.jogo.fim = True

class OutrosPerdemDinheiro(Efeito):
    exp = "^Todos os demais jogadores perdem todo seu dinheiro$"
    @classmethod
    def descer(cls, carta, dono, params):
        for j in dono.jogo.jogadores.values():
            if j != dono:
                j.dinheiro = 0

class InverteOrdemJogo(Efeito):
    exp = "^Inverte a ordem do jogo$"
    @classmethod
    def descer(cls, carta, dono, params):
        dono.jogo.inverter_ordem_jogadas()

class VizinhosNaoJogam(Efeito):
    exp = "^O jogador anterior e posterior a voc\w ficam uma rodada sem jogar$"
    @classmethod
    def descer(cls, carta, dono, params):
        vizinhos = dono.jogo.ret_vizinhos(dono)
        for j in vizinhos:
            j.jogadas_extras = -1

class JogaMaisDuasVezes(Efeito):
    exp = "^Jogador joga mais (?P<quant>\w+) vezes$"
    @classmethod
    def descer(cls, carta, dono, params):
        dono.jogadas_extras += int(carta.efeito_dados["quant"])

class RecebeCartasJogadorComMaisPontos(Efeito):
    exp = "^Recebe (?P<quant>\w+) cartas aleat\wrias da m\wo do jogador com mais pontos$"
    @classmethod
    def descer(cls, carta, dono, params):
        j = dono.jogo.ret_jog_mais_pontos()
        for i in range(int(carta.efeito_dados["quant"])):
            if len(j.mao) and len(dono.mao) < MAX_CARTAS_MAO:
                escolha = choice(j.mao)
                j.mao.remove(escolha)
                dono.mao.append(escolha)

class RecebeCartaDeUmDinheiroDoOutro(Efeito):
    exp = "^Recebe uma carta aleat\wria da m\wo de um e (?P<quant>\w+)\$ do outro$"
    @classmethod
    def descer(cls, carta, dono, params):
        alvo1 = dono.jogo.ret_jog_num(params[0])
        alvo2 = dono.jogo.ret_jog_num(params[1])
        if len(dono.mao) < MAX_CARTAS_MAO:
            if len(alvo1.mao) > 0:
                escolha = choice(alvo1.mao)
                alvo1.mao.remove(escolha)
                dono.mao.append(escolha)
        alteracao = int(carta.efeito_dados["quant"])
        if alvo2.dinheiro >= int(carta.efeito_dados["quant"]):
            alvo2.dinheiro -= alteracao
            dono.dinheiro += alteracao
        else:
            dono.dinheiro += alvo2.dinheiro
            alvo2.dinheiro = 0

class EscolheJogadorFicaSemJogar(Efeito):
    exp = "^Este fica uma rodada sem jogar$"
    @classmethod
    def descer(cls, carta, dono, params):
        alvo = dono.jogo.ret_jog_num(params[0])
        alvo.jogadas_extras -= 1

class ExcluiDuasMenoresCartas(Efeito):
    exp = "^Este tem excluidas suas duas menores cartas$"
    @classmethod
    def descer(cls, carta, dono, params):
        alvo = dono.jogo.ret_jog_num(params[0])
        for i in range(2):
            menor_valor = 1000
            menor_carta = None
            menor_iden = None
            for naipe in alvo.mesa.values():
                for iden in naipe:
                    c = dono.jogo.baralho.get(iden)
                    if c.valor < menor_valor:
                        menor_carta = c
                        menor_iden = iden
            if menor_carta:
                alvo.perder_carta_mesa(menor_iden, menor_carta)

class ExcluiMenorCarta(Efeito):
    exp = "^Este excluir a menor carta que tiver baixada na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        alvo = dono.jogo.ret_jog_num(params[0])
        menor_valor = 1000
        menor_carta = None
        menor_iden = None
        for naipe in alvo.mesa.values():
            for iden in naipe:
                c = dono.jogo.baralho.get(iden)
                if c.valor < menor_valor:
                    menor_carta = c
                    menor_iden = iden
        if menor_carta:
            alvo.perder_carta_mesa(menor_iden, menor_carta)

class PerdeDinheiroPorCartasBaixas(Efeito):
    exp = "^Este perde (?P<quant>\w+)\$ para cada carta de valor um ou 3 que tiver baixada na sua mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        alvo = dono.jogo.ret_jog_num(params[0])
        num = 0
        for naipe in alvo.mesa.values():
            for iden in naipe:
                c = dono.jogo.baralho.get(iden)
                if c.valor in [1,3]:
                    num += 1
        alteracao = int(num*int(carta.efeito_dados["quant"]))
        alvo.dinheiro -= alteracao

class AlteraDinheiroSeuOutro(Efeito):
    exp = "^Este e voc\w (?P<acao>\w+) (?P<quant>\w+)\$$"
    @classmethod
    def descer(cls, carta, dono, params):
        if carta.efeito_dados["acao"] == "perdem":
            sinal = -1
        else:
            sinal = 1
        alvo = dono.jogo.ret_jog_num(params[0])
        alteracao = int(sinal*int(carta.efeito_dados["quant"]))
        alvo.dinheiro += alteracao
        dono.dinheiro += alteracao

class AlteraDinheiroPorCartaDeNaipe(Efeito):
    exp = "^Este (?P<acao>\w+) (?P<quant>\w+)\$ pra cada carta (?P<naipe>\w+) que o mesmo tiver baixado na mesa$"
    @classmethod
    def descer(cls, carta, dono, params):
        if carta.efeito_dados["acao"] == "perde":
            sinal = -1
        else:
            sinal = 1
        naipe = carta.efeito_dados["naipe"].lower()
        alvo = dono.jogo.ret_jog_num(params[0])
        l = alvo.mesa.get(naipe)
        if l:
            num = len(l)
        else:
            num = 0
        alteracao = int(sinal*int(carta.efeito_dados["quant"])*num)
        alvo.dinheiro += alteracao

class PegarCartasDescarte(Efeito):
    exp = "^Elas v\wm para a sua m\wo$"
    @classmethod
    def descer(cls, carta, dono, params):
        # ALTERARRRRRRRRRRRRRRRRRRRRRRRRRR
        pass

class PontosPorCartaFinal(Permanente, Efeito):
    exp = "^Jogador recebe (?P<quant>\w+) ponto\w? por carta (?P<tipo>\w+) (?P<naipe>\w+) ao final do jogo$"
    especial = "calculo_pontos_finais"
    @classmethod
    def executar(cls, dados, dono, carta):
        naipe = carta.efeito_dados["naipe"].lower()
        l = dono.mesa.get(naipe)
        if l:
            num = 0
            for c in l:
                # caso seja uma carta impar
                if dono.jogo.baralho.get(c).valor%2 == 1:
                    num += 1
            dados["pontos"] += int(carta.efeito_dados["quant"]) * num

class PontosFinal(Permanente, Efeito):
    exp = "^A carta vale mais (?P<quant>\w+) ponto\w? ao final do jogo$"
    especial = "calculo_pontos_finais"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["pontos"] += int(carta.efeito_dados["quant"])

class DinheiroAoBaixar(Permanente, Efeito):
    exp = "^Jogador ganha \+(?P<quant1>\w+)\$ ao baixar carta (?P<tipo>\w+) de (?P<naipe>\w+) de valor 1,3,5 e \+(?P<quant2>\w+)\$ de valor 7 e 9$"
    especial = "ao_descer_carta"
    @classmethod
    def executar(cls, dados, dono, carta):
        carta_baixada = dados["carta"]
        if carta_baixada.naipe == carta.efeito_dados["naipe"].lower():
            if carta_baixada.valor in [1, 3, 5]:
                dados["dinheiro"] += int(carta.efeito_dados["quant1"])
            elif carta_baixada.valor in [7, 9]:
                dados["dinheiro"] += int(carta.efeito_dados["quant2"])

class ReceberMaisDinheiro(Permanente, Efeito):
    exp = "^PODER FIXO: quando escolher receber dinheiro, recebe (?P<quant>\w+)\$ a mais$"
    especial = "ao_pegar_dinheiro"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["dinheiro"] += int(carta.efeito_dados["quant"])

class AlteraCustoCompraDescarte(Permanente, Efeito):
    exp = "^PODER FIXO: Compra do descarte pagando (?P<quant>\w+)\$$"
    especial = "altera_custo_compra_descarte"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["custo"] = int(carta.efeito_dados["quant"])

class AlteraValorMinDescarte(Permanente, Efeito):
    exp = "^PODER FIXO: jogador pode descartar qualquer carta$"
    especial = "altera_valor_min_descarte"
    @classmethod
    def executar(cls, dados, dono, carta):
        #dados["custo"] = int(carta.efeito_dados["quant"])
        dados["valor"] = -1

class AlteraCustoCoringas(Permanente, Efeito):
    exp = "^PODER FIXO: Adiciona curingas sem ter necessidade de pagar$"
    especial = "altera_custo_curingas"
    @classmethod
    def executar(cls, dados, dono, carta):
        if dados["valor"] in [2,6,10]:
            dados["custo"] = 0

class PegaMaisCartas(Permanente, Efeito):
    exp = "^PODER FIXO: Quando selecionar comprar cartas, compra (?P<quant>\w+) de uma vez$"
    especial = "pega_mais_cartas"
    @classmethod
    def executar(cls, dados, dono, carta):
        dados["quant"] = 2
