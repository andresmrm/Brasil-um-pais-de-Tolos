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

import os, random, re, time


DIR_CARTAS = "bpt/cartas"
MAX_CARTAS_MAO = 5
NUM_CARTAS_INICIAIS = 2
DINHEIRO_INICIAL = 5


class Magica():

    def __init__(self):
        self.efeitos = {
            "Nada acontece" : None,
            "Jogador que tiver mais cartas (?P<tipo>\w+) (?P<naipe>\w+) baixadas na mesa (?P<acao>\w+) (?P<quant>\w+)\$" : self.dinheiro_maioria,
            "(?P<acao>\w+) (?P<quant>\w+)\$" : self.altera_dinheiro,
            "Recebe (?P<quant>\w+) cartas do monte" : self.recebe_cartas_monte,
        }

    def interpretar(self, texto):
        for e in self.efeitos.keys():
            exp = re.search(e, texto)
            if exp:
                return (self.efeitos[e], exp.groupdict())
        return (None, None)

    def dinheiro_maioria(self, dados, dono):
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

    def altera_dinheiro(self, dados, dono):
        """Altera a quantidade de dinheiro do dono da carta"""
        if dados["acao"] == "perde":
            sinal = -1
        else:
            sinal = 1
        alteracao = int(sinal*int(dados["quant"]))
        dono.dinheiro += alteracao

    def recebe_cartas_monte(self, dados, dono):
        """Dono da carta pega X cartas do monte"""
        for i in range(int(dados["quant"])):
            if len(dono.mao) < MAX_CARTAS_MAO:
                carta = dono.jogo.pegar_carta_monte()
                if carta != None:
                    dono.adi_carta(carta)




M = Magica()



class SistemaPreJogo():

    def __init__(self, sist_chat):
        self.salas = {}
        self.jogadores = {}
        self.sist_chat = sist_chat
        
        self.central = 'central'
        self.criar_sala(self.central, None)

    def criar_sala(self, nome, jog):
        r = False
        if self.salas.get(nome) == None:
            s = Jogo(nome, self.sist_chat)
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
            print "Tentando remover jogador???!!! Feito mais ou menos..."
            self.jogadores[jog] = None
            return True

        s = self.salas.get(sala)
        # Verifica se a sala existe
        if not s:
            return False

        j = self.jogadores.get(jog)
        if not j:
            j = Jogador(jog, s) 
            self.jogadores[jog] = j
        else:
            j.trocar_jogo(s)
        s.adi_jogador(j)
        return True

    def rem_jogador(self, sala, jog):
        s = self.salas[sala]
        s.rem_jog(jog)
        if s.vazia() and sala != self.central:
            self.fechar_sala(nome)

    def ret_jogador(self, nome):
        return self.jogadores.get(nome)

    def ret_jogadores(self, nome_jogo):
        self.salas[nome_jogo].ret_jogadores()

    def ret_jogadores_dicio(self, jogo):
        """Retorna uma lista com os dados dos jogadores em dicionarios"""
        jogs = [ jog.__dict__ for jog in jogo.ret_jogadores()]
        for j in jogs:
            j["tam_mao"] = len(j["mao"])
        return jogs

    def ret_atualizacao(self, jogador, jogo, num):
        """Retorna dicionario com atualizacoes a serem feitas na interface"""
        try:
            num = int(num)
        except:
            return "ERRO: Numero da jogada nao e numero valido!"

        if num == jogo.num_jogada:
            return "0"

        #resposta = self.validar_jogador(nome_jog)
        #if resposta != True:
        #    return resposta

        dicio = {}
        dicio["num_jogada"] = jogo.num_jogada
        dicio["mao"] = jogador.mao
        dicio["mesas"] = "A"
        return dicio

    def validar_jogador(self, nome_jog):
        """Verifica se um jogador existe"""
        jog = self.jogadores.get(nome_jog)
        if jog == None:
            return "ERRO: Jogador nao encontrado!"

        #if jog.cod != cod:
        #    return "ERRO: Codigo nao bate!"

        return True

    def fechar_sala(self, nome):
        s = self.salas[nome]
        self.jogadores = s.ret_jogadores()
        for jog in jogadores:
            self.jogadores[jog].trocar_jogo(self.central)
        self.salas[nome] = None
        self.sist_chat.fechar_sala(nome)

    def iniciar_jogo(self, nome_jogo):
        j = self.salas.get(nome_jogo)
        if j:
            j.iniciar()
            return True
        else:
            return False

    def executar(self,nome_jog, jogada):
        """Exucuta uma jogada de um jogador"""
        resposta = self.validar_jogador(nome_jog)
        if resposta != True:
            return resposta
        jog = self.jogadores[nome_jog]
        jogo = jog.jogo
        try:
            if jogada[0] == 'R':
                jogo.iniciar()
                return "Ok"
        except:
            pass

        if jog.nome != jogo.jogador_atual:
            return "ERRO: Nao e a sua vez de jogar!"

        if len(jogada) < 2:
            return "ERRO: Jogada muito curta para processar!"

        tipo, iden = jogada[0], jogada[1:]
        if tipo == 'J':
            return jog.jogar_carta(iden)
        elif tipo == 'C':
            return jog.comprar_carta(iden)
        elif tipo == 'D':
            return jog.descartar_carta(iden)
        elif tipo == 'G':
            return jog.pegar_dinheiro()
        elif tipo == 'M':
            return jog.mais_carta()

        return "ERRO: Jogada nao identificada!" 

    def nova_pagina(self, nome_jog):
        jog = self.jogadores[nome_jog]
        jogo = jog.jogo
        jogo.iniciar()
        jogadores = self.ret_jogadores_dicio(jogo)
        descarte = jogo.descarte
        baralho = jogo.baralho
        return {'jogadores':jogadores, 'descarte':descarte, 'baralho':baralho}

    def nova_atualizacao(self, nome_jogador, num):
        jog = self.jogadores[nome_jogador]
        jogo = jog.jogo
        ret = self.ret_atualizacao(jog, jogo, num)
        if ret == "0":
            return [ret]
        else:
            j = self.ret_jogadores_dicio(jogo)
            b = jogo.baralho
            d = jogo.descarte
            return [ret, j, b, d]


class Jogo():
    """Reune e centraliza os elementos do jogo"""

    def __init__(self, nome, sist_chat):
        self.nome = nome
        self. iniciado = False
        self.sist_chat = sist_chat
        self.sist_chat.criar_sala(nome)

        self.baralho = {}
        self.jogadores = {}
        self.maiorias = {}
        self.monte = []
        self.descarte = {}
        self.jogador_atual = None
        self.num_jogada = 0
        self.fim = False

    def adi_jogador(self, jog): 
        """Adiciona um jogador a lista de jogadores do jogo"""
        self.jogadores[jog.nome] = jog

    def rem_jogador(self, jog):
        self.jogadores[jog.nome] = None

    def ret_jogadores(self):
        return self.jogadores.values()

    def vazio(self):
        if len(self.jogadores) == 0:
            return True
        return False

    def montar_baralho(self):
        """Carrega as cartas e monta o monte inicial de cartas"""
        nomes_arqs = os.listdir(DIR_CARTAS)
        for nome in nomes_arqs:
            if nome[0] != ".":
                with open(os.path.join(DIR_CARTAS, nome)) as arq:
                    linhas = arq.read().splitlines()
                    for linha in linhas:
                        if len(linha) > 0:
                            linha = linha.decode('utf-8')
                            try:
                                atribs = linha.split('\t')
                                naipe,imagem,valor,custo,tipo,nome,frase,efeito = atribs
                                e, d = M.interpretar(efeito)
                                c = Carta(nome=nome,
                                          naipe=naipe[0:3].lower(),
                                          imagem=str(imagem+".png"),
                                            valor=int(valor),
                                            custo=int(custo),
                                            tipo=tipo,
                                            frase=frase.encode('ascii','xmlcharrefreplace'),
                                            efeito_texto=efeito.encode('ascii','xmlcharrefreplace'),
                                            efeito_dados=d,
                                            efeito=e)
                                self.baralho[len(self.baralho)] = c
                            except:
                                raise
                                print("Carta nao pode ser lida: "+linha)
    #                atributos = {}
    #                for linha in linhas:
    #                    tipo, valor = linha.split(":")
    #                    atributos[tipo.strip()] = valor.strip()
    #                c = Carta(nome=atributos['nome'],
    #                          num=atributos['valor'],
    #                          naipe=atributos['naipe'],
    #                          naipe=atributos['tipo'],
    #                          custo=int(atributos['custo']),
    #                          efeito=atributos['efeito']),
    #                          frase=atributos['frase'])
    #                self.baralho[len(self.baralho)] = c

    def distribuir_cartas(self):
        """Da as primeiras cartas para cada jogador"""
        for j in self.jogadores.values():
            for n in range(NUM_CARTAS_INICIAIS):
                j.adi_carta(self.monte.pop())

    def iniciar(self):
        """Faz as preparacoes iniciais para comecar o jogo"""
        if self.iniciado == False:
            self.montar_baralho()
            self.monte = list(self.baralho.keys())
            #DELETE ESSE FOR DEPOIS DE TESTAR
            for i in range(50):
                self.monte = self.monte + list(self.baralho.keys())
            random.shuffle(self.monte)
            self.distribuir_cartas()
            self.jogador_atual = self.jogadores.keys()[0]
            self.iniciado = True
            print "INICIAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaR"

    def verificar_maiorias(self):
        """Verifica e marca em cada jogador quais maiorias de naipe ele tem"""
        self.maiorias = {}
        for j in self.jogadores.values():
            for naipe in j.mesa.keys():
                quant = len(j.mesa[naipe])
                atual = self.maiorias.get(naipe)
                if atual == None or atual[0] < quant:
                    self.maiorias[naipe] = (quant, [j.nome])
                elif atual[0] == quant:
                    atual[1].append(j.nome)
        for j in self.jogadores.values():
            j.maiorias = []
        for naipe in self.maiorias.keys():
            for nome_jog in self.maiorias[naipe][1]:
                self.jogadores[nome_jog].maiorias.append(naipe)

    def calc_pontos(self):
        """Calcula os pontos de cada jogador"""
        for j in self.jogadores.values():
            j.calc_pontos()

    def pegar_carta_monte(self):
        """Tira uma carta no monte"""
        if len(self.monte) == 0:
            self.fim = True
            return None
        return self.monte.pop()

    def receber_descarte(self, iden, carta):
        """Recebe uma carta e a coloca no monte de descartadas"""
        naipe = self.descarte.get(carta.naipe)
        if naipe:
            naipe.append(iden)
        else:
            self.descarte[carta.naipe] = [iden]


    def prox_jogador(self):
        """Passa a vez de jogar para o proximo jogador"""
        nomes = self.jogadores.keys()
        if self.jogador_atual == nomes[-1]:
            self.jogador_atual = nomes[0]
        else:
            num = nomes.index(self.jogador_atual)
            self.jogador_atual = nomes[num+1]
        self.verificar_maiorias()
        self.calc_pontos()
        self.num_jogada += 1

        # Roda IA caso jogador esteja em modo automatico
        j = self.jogadores[self.jogador_atual]
        if j.automatico == True:
            j.jogada_automatica()




class Jogador():
    """Um jogador"""

    def __init__(self, nome, jogo):
        self.nome = nome
        self.automatico = False
        self.ult_contato = 0
        self.trocar_jogo(jogo)

    def novo_contato(self):
        self.ult_contato = time.time()

    def trocar_jogo(self, jogo):
        self.jogo = jogo
        self.dinheiro = DINHEIRO_INICIAL
        self.mao = []
        self.mesa = {}
        self.pontos = 0
        self.maiorias = []
        self.novo_contato()

    def adi_carta(self, carta):
        """Adiciona uma carta a mao do jogador"""
        if len(self.mao) < MAX_CARTAS_MAO:
            self.mao.append(carta)

    def calc_pontos(self):
        """Calcula os pontos desse jogador"""
        self.pontos = 0
        for naipe in self.mesa.values():
            for carta in naipe:
                valor = self.jogo.baralho[carta].valor
                if valor%2 == 1:
                    self.pontos += valor

    def identificar_carta(self, iden, verif_mao=True):
        """Identifica uma carta na mao do jogador"""
        try:
            iden = int(iden)
        except:
            return "ERRO: Identificador da carta nao e numero valido!"

        if verif_mao:
            if iden not in self.mao:
                return "ERRO: Jogador nao tem essa carta na mao!"

        carta = self.jogo.baralho.get(iden)
        if carta == None:
            return "ERRO: Carta nao existe no baralho!"
        return carta, iden

    def jogar_carta(self, str_iden):
        """Joga uma carta da mao para a mesa"""
        ret = self.identificar_carta(str_iden)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        if self.dinheiro < carta.custo:
            return "ERRO: Dinheiro insuficiente para baixar carta!"
        self.dinheiro -= carta.custo

        self.mao.remove(iden)
        if self.mesa.get(carta.naipe) == None:
            self.mesa[carta.naipe] = []
        self.mesa[carta.naipe] += [iden]
        carta.executar(self)
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def comprar_carta(self, str_iden):
        """Compra uma carta do monte de descarte"""
        if self.dinheiro < 3:
            return "ERRO: Comprar uma carta gasta 3 de dinheiro!"

        ret = self.identificar_carta(str_iden, False)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        if iden not in self.jogo.descarte[carta.naipe]:
            return "ERRO: Monte de descarte nao tem essa carta!"

        self.jogo.descarte[carta.naipe].remove(iden)
        self.mao.append(iden)
        self.dinheiro -= 3
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"
            
    def pegar_dinheiro(self):
        """Pega dinheiro da banca"""
        self.dinheiro += 2
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def descartar_carta(self, str_iden):
        """Descarta uma carta da mão e a coloca no monte de descartes"""
        ret = self.identificar_carta(str_iden)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        if carta.custo <= 5:
            return "ERRO: A carta deve valer mais do que 5!"

        self.mao.remove(iden)
        self.jogo.receber_descarte(iden, carta)
        self.dinheiro += 5
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def mais_carta(self):
        """Pega uma carta do monte"""
        if len(self.mao) >= MAX_CARTAS_MAO:
            return "ERRO: Mao cheia!"

        carta = self.jogo.pegar_carta_monte()
        if carta == None:
            print("O MONTE ACABOU!!!")
            return "ERRO: O monte acabou!"

        self.mao.append(carta)
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def jogada_automatica(self):
        """Faz uma jogada automatica"""
        if self.dinheiro < 10:
            self.pegar_dinheiro()
        elif len(self.mao) < 1:
            self.mais_carta()
        else:
            self.jogar_carta(self.mao[0])


class Carta():
    """Uma carta"""

    def __init__(self, nome="Boba", imagem="", valor=1, naipe="Azul", tipo="Normal",
                 custo=1, frase="Ahhhhh", efeito_texto="Oh", efeito_dados={}, efeito=None):
        self.nome = nome
        self.imagem = imagem
        self.valor = valor
        self.naipe = naipe
        self.tipo = tipo
        self.custo = custo
        self.frase = frase
        self.efeito_texto = efeito_texto
        self.efeito_dados = efeito_dados
        self.efeito = efeito

    def executar(self, dono):
        if self.efeito != None:
            self.efeito(self.efeito_dados, dono)
