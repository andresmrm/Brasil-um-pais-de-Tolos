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

import os, random, re, time

from chat import SistemaChat
from efeitos import *
from constantes import *


class Magica():
    def interpretar(self, texto):
        if texto[0] == '"':
            texto = texto[1:]
        if texto[-1] == '"':
            texto = texto[:-1]
        if texto[-1] == ".":
            texto = texto[:-1]
        for e in Efeito.__subclasses__():
            exp = re.match(e.exp, texto, flags=re.UNICODE)
            if exp:
                #print texto, "||||", e.exp
                possiveis_param = [ "Escolhe (?P<quant>\d+) (?P<objeto>\w+)(\ (?P<complemento>\w+))*\.",
                                  ]
                for exp_param in possiveis_param:
                    achou_param = re.search(exp_param, texto, flags=re.UNICODE)
                    if achou_param:
                        quant = achou_param.groupdict()['quant']
                        objeto = achou_param.groupdict()['objeto']
                        complemento = achou_param.groupdict()['complemento']
                        parametros = quant+objeto[0]
                        if complemento:
                            parametros += complemento[0]
                        print parametros
                        return (e, exp.groupdict(), parametros)
                return (e, exp.groupdict(), 1)
        print texto, "---------------"
        return (None, None, "1ca")


M = Magica()


class SistemaPreJogo():
    """Reúne e organiza os jogos"""

    def __init__(self):
        self.jogos = {}
        self.jogadores = {}
        self.sist_chat = SistemaChat()
        
        self.central = 'central'
        self.criar_jogo(self.central, None)

    def adi_msg(self, nome_jogo, nome_jogador, msg):
        """Adiciona 'msg' ao jogo 'nome_jogo' com autoria de 'nome_jogador' e
        retorna o número de mensagens nesse jogo"""
        return self.sist_chat.adi_msg(nome_jogo, nome_jogador, msg)

    def ret_msgs(self, nome_jogo):
        """Retorna mensagens do jogo 'nome_jogo'"""
        return self.sist_chat.ret_msgs(nome_jogo)

    def criar_jogo(self, nome_jogo, nome_jogador):
        """Cria um jogo 'nome_jogo' e adiciona o jogador 'nome_jogador'"""
        r = False
        # Caso jogo não exista
        if self.jogos.get(nome_jogo) == None:
            s = Jogo(nome_jogo, self.sist_chat)
            self.jogos[nome_jogo] = s
            r = True
        # Caso deve colocar um jogador dentro da sala
        if nome_jogador:
            r = self.colocar_jogador_jogo(nome_jogo, nome_jogador)
        return r

    def ret_jogo(self, nome_jogo):
        """Retorna o jogo de nome 'nome_jogo'"""
        return self.jogos.get(nome_jogo)

    def ret_jogos(self):
        """Retorna os jogos abertos"""
        r = []
        for s in self.jogos.values():
            if s.nome != 'central':
                r.append(s)
        return r

    def colocar_jogador_jogo(self, nome_jogo, nome_jogador):
        """Coloca um jogador em uma determinada sala"""
        if not nome_jogo:
            self.jogadores[nome_jogador] = None
            return True

        s = self.jogos.get(nome_jogo)
        # Verifica se a sala existe
        if not s:
            return False
            return "ERRO: Sala nao existe!"
        # Verifica se jogo tem espaço para mais um jogador
        if len(s.ret_jogadores())+1 > s.max_num_jogadores:
            return False
            return "ERRO: Sala cheia!"

        j = self.jogadores.get(nome_jogador)
        # Caso jogador ainda não exista
        if not j:
            j = Jogador(nome_jogador, s) 
            self.jogadores[nome_jogador] = j
            s.adi_jogador(j)
        elif j.jogo and j.jogo != s:
                self.rem_jogador(j.jogo.nome, j)
                s.adi_jogador(j)
                j.trocar_jogo(s)
                j.pronto = False
        return True

    def rem_jogador(self, nome_jogo, nome_jogador):
        """Remove um jogador de uma sala"""
        s = self.jogos.get(nome_jogo)
        if s:
            s.rem_jogador(nome_jogador)
            if s.vazio() and nome_jogo != self.central:
                self.fechar_jogo(nome_jogo)

    def ret_jogador(self, nome):
        """Retorna uma jogador pelo nome"""
        return self.jogadores.get(nome)

    def ret_jogadores(self, nome_jogo):
        """Retorna os jogadores de um jogo"""
        return self.jogos[nome_jogo].ret_jogadores()

    def ret_jogadores_dicio(self, jogo):
        """Retorna uma lista com os dados dos jogadores em dicionarios"""
        jogs = [ jog.__dict__ for jog in jogo.ret_jogadores()]
        for j in jogs:
            j["tam_mao"] = len(j["mao"])
        return jogs

    def ret_todos_jogadores(self):
        """Retorna todos os jogadores"""
        return self.jogadores.values()

    def validar_jogador(self, nome_jog):
        """Verifica se um jogador existe"""
        jog = self.jogadores.get(nome_jog)
        if jog == None:
            return "ERRO: Jogador nao encontrado!"

        #if jog.cod != cod:
        #    return "ERRO: Codigo nao bate!"

        return True

    def fechar_jogo(self, nome):
        """Fecha um jogo"""
        s = self.jogos[nome]
        jogadores = s.ret_jogadores()
        for jog in jogadores:
            self.jogadores[jog].trocar_jogo(self.central)
        self.jogos.pop(nome)
        self.sist_chat.fechar_sala(nome)

    def iniciar_jogo(self, nome_jogo):
        """Inicia o jogo de nome 'nome_jogo'"""
        j = self.jogos.get(nome_jogo)
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

        if jog.nome != jogo.nome_jogador_atual:
            return "ERRO: Nao e a sua vez de jogar!"

        if len(jogada) < 2:
            return "ERRO: Jogada muito curta para processar!"

        #exp = "^(?P<tipo>\w)(?P<iden>\d+)(\-(?P<param>\d+))*$"
        exp = "^(\w)(\d+)(?:\-(\d+))?(?:\-(\d+))?(?:\-(\d+))?(?:\-(\d+))?$"
        bateu = re.match(exp, jogada)
        if bateu:
            tipo, iden = bateu.groups()[:2]
            if tipo == 'J':
                params = []
                for p in bateu.groups()[2:]:
                    if p:
                        params.append(p)
                return jog.jogar_carta(iden, params)
            elif tipo == 'C':
                return jog.comprar_carta(iden)
            elif tipo == 'D':
                return jog.descartar_carta(iden)
            elif tipo == 'G':
                return jog.pegar_dinheiro()
            elif tipo == 'M':
                return jog.mais_carta()

        return "ERRO: Jogada nao identificada!" 

    def nova_pagina(self, nome_jogador):
        """Prepara dados para a visualização da página de jogo"""
        jogador = self.jogadores.get(nome_jogador)
        if jogador:
            jogo = jogador.jogo
            jogadores = self.ret_jogadores_dicio(jogo)
            descarte = jogo.descarte
            baralho = jogo.baralho
            return {'jogadores':jogadores, 'descarte':descarte, 'baralho':baralho, 'jogo':jogo.nome}
        else:
            return {}

    def nova_atualizacao(self, nome_jogador, num):
        """Retorna dicionario com atualizacoes a serem feitas na interface"""
        try:
            num = int(num)
        except:
            return "ERRO: Numero da jogada nao e numero valido!"

        jogador = self.jogadores.get(nome_jogador)
        if jogador:
            jogo = jogador.jogo
            if num == jogo.num_jogada and not jogo.fim:
                # Nada para ser atualizado
                return "0"

            dicio = {}
            dicio["num_jogada"] = jogo.num_jogada
            dicio["mao"] = jogador.mao
            dicio["mesas"] = "A"
            dicio["fim"] = jogo.fim
            j = self.ret_jogadores_dicio(jogo)
            b = jogo.baralho
            d = jogo.descarte
            return [dicio, j, b, d]
        else:
            return "0"


class Jogo():
    """Reune e centraliza os elementos do jogo"""

    def __init__(self, nome, sist_chat):
        self.nome = nome
        self.iniciado = False
        self.sist_chat = sist_chat
        self.sist_chat.criar_sala(nome)

        self.monte = []
        self.baralho = {}
        self.maiorias = {}
        self.descarte = {}
        self.jogadores = {}
        self.fim = False
        self.num_jogada = 0
        self.nome_jogador_atual = None
        self.max_num_jogadores = 5
        self.ordem_invertida = False

    def adi_jogador(self, jog): 
        """Adiciona um jogador a lista de jogadores do jogo"""
        self.jogadores[jog.nome] = jog

    def rem_jogador(self, jog):
        """Remove um jogador do jogo"""
        if jog.nome in self.jogadores:
            self.jogadores.pop(jog.nome)

    def ret_jogadores(self):
        """Retorna jogadores no jogo"""
        return self.jogadores.values()

    def ret_jog_mais_pontos(self):
        """Retorna o ganhador do jogo"""
        ordenado = sorted(self.jogadores.values(),key=lambda j: j.pontos)
        return ordenado[-1]

    def vazio(self):
        """Se o jogo está vazio ou não"""
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
                                e, d, p = M.interpretar(efeito)
                                c = Carta(nome=nome,
                                          naipe=naipe[0:3].lower(),
                                          imagem=str(imagem+".png"),
                                          valor=int(valor),
                                          custo=int(custo),
                                          tipo=tipo,
                                          frase=frase.encode('ascii','xmlcharrefreplace'),
                                          efeito_texto=efeito.encode('ascii','xmlcharrefreplace'),
                                          efeito_dados=d,
                                          efeito=e,
                                          parametros=p)
                                self.baralho[len(self.baralho)] = c
                                #print c.efeito, c.frase
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
            #for i in range(50):
            #    self.monte = self.monte + list(self.baralho.keys())
            #self.monte = self.monte[:3]


            random.shuffle(self.monte)
            self.distribuir_cartas()
            self.nome_jogador_atual = self.jogadores.keys()[0]
            self.iniciado = True

    def verificar_maiorias(self):
        """Verifica e marca em cada jogador quais maiorias de naipe ele tem"""
        self.maiorias = {}
        for j in self.jogadores.values():
            for naipe in j.mesa.keys():
                quant = len(j.mesa[naipe])
                if quant:
                    # Aplica especial
                    dados = {"naipe":naipe,
                             "quant":quant}
                    j.aplicar_especial("calculo_maioria", dados)
                    quant = dados["quant"]

                    atual = self.maiorias.get(naipe)
                    if atual == None or atual[0] < quant:
                        self.maiorias[naipe] = (quant, [j.nome])
                    # Em caso de empate de numero de cartas de um naipe
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
            j.calc_pontos(final=self.fim)

    def pegar_carta_monte(self):
        """Tira uma carta no monte"""
        if len(self.monte) == 0:
            return None
        return self.monte.pop()

    def receber_descarte(self, iden, carta):
        """Recebe uma carta e a coloca no monte de descartadas"""
        naipe = self.descarte.get(carta.naipe)
        if naipe:
            naipe.append(iden)
        else:
            self.descarte[carta.naipe] = [iden]

    def ret_vizinhos(self, jogador):
        """Retorna os vizinhos de um jogador"""
        nomes = self.jogadores.keys()
        num = nomes.index(jogador.nome)
        anterior = num-1
        posterior = num+1
        if anterior < 0:
            anterior = len(nomes)-1
        if posterior > len(nomes)-1:
            posterior = 0
        j1 = self.jogadores[nomes[anterior]]
        j2 = self.jogadores[nomes[posterior]]

        # Caso so tenha 2 ou 1 jogador
        if anterior == posterior:
            # Caso so tenha 1 jogador
            if anterior == num:
                return []
            return [j1]
        else:
            return [j1, j2]


    def prox_jogador(self):
        """Passa a vez de jogar para o próximo jogador"""
        jogador_atual = self.jogadores[self.nome_jogador_atual]
        if jogador_atual.jogadas_extras <= 0:
            nomes = self.jogadores.keys()
            if not self.ordem_invertida:
                if self.nome_jogador_atual == nomes[-1]:
                    self.nome_jogador_atual = nomes[0]
                else:
                    num = nomes.index(self.nome_jogador_atual)
                    self.nome_jogador_atual = nomes[num+1]
            else:
                if self.nome_jogador_atual == nomes[0]:
                    self.nome_jogador_atual = nomes[-1]
                else:
                    num = nomes.index(self.nome_jogador_atual)
                    self.nome_jogador_atual = nomes[num-1]
            jogador_atual = self.jogadores[self.nome_jogador_atual]
            if jogador_atual.jogadas_extras < 0:
                jogador_atual.jogadas_extras += 1
                self.prox_jogador()
        else:
            jogador_atual.jogadas_extras -= 1

        self.verificar_maiorias()
        self.calc_pontos()
        self.num_jogada += 1

        # Roda IA caso jogador esteja em modo automatico
        j = self.jogadores[self.nome_jogador_atual]
        if j.automatico == True:
            j.jogada_automatica()

    def ret_jog_mais_dinheiro(self):
        """Retorna o jogador com mais dinheiro"""
        ordenado = sorted(self.jogadores.values(), key=lambda j: j.dinheiro)
        return ordenado[-1]

    def inverter_ordem_jogadas(self):
        self.ordem_invertida = not self.ordem_invertida


class Jogador():
    """Um jogador"""

    def __init__(self, nome, jogo):
        self.nome = nome
        self.automatico = False
        self.ult_contato = 0
        self.trocar_jogo(jogo)
        self.pronto = False

    def novo_contato(self):
        """Avisa que o jogador ainda está online"""
        self.ult_contato = time.time()

    def trocar_jogo(self, jogo):
        """Troca esse jogador de jogo"""
        self.jogo = jogo
        self.dinheiro = DINHEIRO_INICIAL
        self.mao = []
        self.mesa = {}
        self.pontos = 0
        self.maiorias = []
        self.especiais = []
        self.jogadas_extras = 0
        self.novo_contato()

    def adi_carta(self, carta):
        """Adiciona uma carta a mao do jogador"""
        if len(self.mao) < MAX_CARTAS_MAO:
            self.mao.append(carta)

    def calc_pontos(self, final=False):
        """Calcula os pontos desse jogador"""

        #REMOVER ESSA LINHA ABAIXO!!!!!!!!!!!
        final = True

        self.pontos = 0
        for naipe in self.mesa.values():
            pontos_naipe = 0
            for carta in naipe:
                valor = self.jogo.baralho[carta].valor
                pontos_naipe += valor
                # Adiciona apenas os valores das cartas ímpares
                if valor%2 == 1:
                    self.pontos += valor
            # Verifica se tem todas as cartas de um naipe
            if pontos_naipe == 55:
                self.pontos += 20
        # Pontos pelas maiorias CALCULO SIMPLIFICADO!!!!!!!!!!
        self.pontos += len(self.maiorias)*10
        
        if final:
            dados = {"pontos":self.pontos}
            self.aplicar_especial("calculo_pontos_finais", dados)
            self.pontos = dados["pontos"]

        #if self.nome == "2":
        #    self.pontos = 100

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

    def jogar_carta(self, str_iden, param):
        """Joga uma carta da mao para a mesa"""
        ret = self.identificar_carta(str_iden)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        if self.dinheiro < carta.custo:
            return "ERRO: Dinheiro insuficiente para baixar carta!"
        self.dinheiro -= carta.custo

        # Cria lista para o naipe caso nao exista
        self.mao.remove(iden)
        if self.mesa.get(carta.naipe) == None:
            self.mesa[carta.naipe] = []

        # Verifica se já tem uma carta de mesmo valor e naipe da mesa
        for ident_tmp in self.mesa[carta.naipe]:
            carta_tmp = self.jogo.baralho.get(ident_tmp)
            if carta_tmp.valor == carta.valor:
                self.perder_carta_mesa(ident_tmp,carta_tmp)

        self.mesa[carta.naipe] += [iden]
        self.mesa[carta.naipe].sort(key=lambda id: self.jogo.baralho.get(id).valor)
        carta.descer(self)

        # Aplica especial
        dados = {"dinheiro":self.dinheiro,
                 "carta":carta,
                }
        self.aplicar_especial("ao_descer_carta", dados)
        self.dinheiro = dados["dinheiro"]

        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def comprar_carta(self, str_iden):
        """Compra uma carta do monte de descarte"""
        custo = CUSTO_COMPRA_DESCARTE

        # Aplica especial
        dados = {"custo":custo}
        self.aplicar_especial("altera_custo_compra_descarte", dados)
        custo = dados["custo"]

        if self.dinheiro < custo:
            return "ERRO: Comprar uma carta gasta %s de dinheiro!" % custo

        if len(self.mao) >= MAX_CARTAS_MAO:
            return "ERRO: Mao cheia!"

        ret = self.identificar_carta(str_iden, False)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        if iden not in self.jogo.descarte[carta.naipe]:
            return "ERRO: Monte de descarte nao tem essa carta!"

        self.jogo.descarte[carta.naipe].remove(iden)
        self.mao.append(iden)
        self.dinheiro -= custo
        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"
            
    def pegar_dinheiro(self):
        """Pega dinheiro da banca"""
        self.dinheiro += 2

        # Aplica especial
        dados = {"dinheiro":self.dinheiro,
                }
        self.aplicar_especial("ao_pegar_dinheiro", dados)
        self.dinheiro = dados["dinheiro"]

        self.jogo.prox_jogador()
        return "Ok! Jogada feita!"

    def perder_carta_mesa(self, iden, carta):
        """Joga fora uma carta da mesa"""
        self.mesa[carta.naipe].remove(iden)
        if carta.efeito:
            carta.efeito.perder(self, carta)
        self.jogo.receber_descarte(iden, carta)


    def descartar_carta(self, str_iden):
        """Descarta uma carta da mão e a coloca no monte de descartes"""
        ret = self.identificar_carta(str_iden)
        if type(ret) == str:
            return ret
        else:
            carta, iden = ret

        custo = CUSTO_MINIMO_PARA_DESCARTE

        # Aplica especial
        dados = {"custo":custo}
        self.aplicar_especial("altera_valor_min_descarte", dados)
        custo = dados["custo"]

        if carta.custo <= custo:
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
            if self.jogo.fim:
                self.jogo.calc_pontos()
                return "O monte acabou!"
            else:
                self.jogo.fim = True
                return "FIM: O monte acabou!"

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

    def adi_especial(self, especial, carta):
        self.especiais.append((especial, carta))

    def rem_especial(self, especial, carta):
        self.especiais.remove((especial, carta))

    def aplicar_especial(self, especial, dados):
        for texto, carta in self.especiais:
            if texto == especial:
                carta.efeito.executar(dados, self, carta)


class Carta():
    """Uma carta"""

    def __init__(self, nome="Boba", imagem="", valor=1, naipe="Azul", tipo="Normal",
                 custo=1, frase="Ahhhhh", efeito_texto="Oh", efeito_dados={}, efeito=None,
                 parametros=None):
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
        self.parametros = parametros

    def descer(self, dono):
        """Executa o efeito dessa carta ao descê-la"""
        if self.efeito != None:
            self.efeito.descer(self.efeito_dados, dono, self)

    def executar(self, dono):
        """Executa o efeito permanente dessa carta"""
        if self.efeito != None:
            self.efeito.executar(self.efeito_dados, dono, self)
