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

import json

from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

from sqlalchemy.exc import DBAPIError



from .models import (
    DBSession,
    BdJogador,
    )

from jogo import *
from chat import SistemaChat


CONTROLADOR = None


class Controlador():
    """Controla e faz o jogo rodar"""

    def __init__(self):
        self.jogo = None
        self.inicializar()
        print("Montando")

    def inicializar(self):
        self.jogo = Jogo()
        j = self.jogo
        j1 = Jogador("a", j)
        j2 = Jogador("ZOrnitorrinco Voador", j)
        j2.automatico = True
        j3 = Jogador("Tolo3", j)
        j3.automatico = True

        j.iniciar()
        #j1.mesa = { 'pol':[1,2,3,4,5,6,7,8,9],
        #            'fic':[1,2],
        #            'ent': [1],
        #            'soc': [1],
        #            'esp': [1,4,6,8],
        #            'lit':[1]} 

    def ret_jogadores(self):
        """Retorna uma lista com os dados dos jogadores em dicionarios"""
        jogs = [ jog.__dict__ for jog in self.jogo.jogadores.values()]
        for j in jogs:
            j["tam_mao"] = len(j["mao"])
        return jogs

    def ret_atualizacao(self, nome_jog, num):
        """Retorna dicionario com atualizacoes a serem feitas na interface"""
        try:
            num = int(num)
        except:
            return "ERRO: Numero da jogada nao e numero valido!"

        if num == self.jogo.num_jogada:
            return "0"

        resposta = self.validar_jogador(nome_jog)
        if resposta != True:
            return resposta

        dicio = {}
        dicio["num_jogada"] = self.jogo.num_jogada
        dicio["mao"] = self.jogo.jogadores[nome_jog].mao
        dicio["mesas"] = "A"
        return dicio

    def validar_jogador(self, nome_jog):
        """Verifica se um jogador existe"""
        jog = self.jogo.jogadores.get(nome_jog)
        if jog == None:
            return "ERRO: Jogador nao encontrado!"

        #if jog.cod != cod:
        #    return "ERRO: Codigo nao bate!"

        return True

    def executar(self,nome_jog, jogada):
        """Exucuta uma jogada de um jogador"""
        try:
            if jogada[0] == 'R':
                self.inicializar()
                return "Ok"
        except:
            pass

        resposta = self.validar_jogador(nome_jog)
        if resposta != True:
            return resposta
        jog = self.jogo.jogadores.get(nome_jog)

        if jog.nome != self.jogo.jogador_atual:
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

    def nova_pagina(self):
        jogadores = self.ret_jogadores()
        descarte = self.jogo.descarte
        baralho = self.jogo.baralho
        return {'jogadores':jogadores, 'descarte':descarte, 'baralho':baralho}

    def nova_atualizacao(self, jogador, num):
        ret = self.ret_atualizacao(jogador, num)
        if ret == "0":
            return ret
        else:
            j = self.ret_jogadores()
            b = self.jogo.baralho
            d = self.jogo.descarte
            pa = render_to_response('mao.slim',{'jogadores':j,'baralho':b})
            ret["mao"] = pa.body
            pa = render_to_response('mesas.slim',{'jogadores':j,'baralho':b, 'descarte':d})
            ret["mesas"] = pa.body
            return json.dumps(ret)


CONTROLADOR = Controlador()
CHAT = SistemaChat()
CHAT.criar_sala("central")




import deform
import colander
from deform import Form

def record_to_appstruct(self):
    form =  formulador(FormRegistrar,('Registrar',))
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__) if '_sa_' != k[:4]])

def merge_session_with_post(session, post):
    for key,value in post:
        setattr(session, key, value)
    return session


def formulador(form, botoes):
    f = {"form":Form(form(),buttons=botoes).render()}
    return f

def verif_nome_unico(nome):
    dbsession = DBSession()
    j = dbsession.query(BdJogador).filter_by(nome=nome).first()
    if j == None:
        return True
    else:
        return False



class FormLogin(colander.MappingSchema):
    nome = colander.SchemaNode(colander.String(),
                        description='Digite seu nome de usuário')
    senha = colander.SchemaNode(
                        colander.String(),
                        validator=colander.Length(min=5, max=100),
                        widget=deform.widget.PasswordWidget(size=20),
                        description='Digite sua senha')

class FormRegistrar(colander.MappingSchema):
    nome = colander.SchemaNode(colander.String(),
                        validator=colander.Function(verif_nome_unico,"Nome existe"),
                        description='Digite seu nome de usuário')
    senha = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(min=5),
                widget=deform.widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
    email = colander.SchemaNode(
                colander.String(),
                validator=colander.Email('Email inválido'))

class FormEditar(colander.MappingSchema):
    senha = colander.SchemaNode(
                colander.String(),
                validator=colander.Length(min=5),
                widget=deform.widget.CheckedPasswordWidget(size=20),
                description='Digite sua senha e a confirme')
    email = colander.SchemaNode(
                colander.String(),
                validator=colander.Email('Email inválido'))


# PREPARACAO

@forbidden_view_config()
#@forbidden_view_config(renderer='login.slim')
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()
    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)

@view_config(route_name='login', renderer='login.slim')
def pagina_login(request):
    next = request.params.get('next') or request.route_url('inicial')
    login_url = request.route_url('login')
    form = deform.Form(FormLogin(), buttons=('Entrar',))
    if 'Entrar' in request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            return {'form':e.render()}
        nome = request.POST.get("nome",'')
        senha = request.POST.get("senha",'')
        dbsession = DBSession()
        jog = dbsession.query(BdJogador).filter_by(nome=nome).first()
        if jog and jog.verif_senha(senha):
            headers = remember(request, nome)
            return HTTPFound(location=next, headers=headers)
        mensagem = 'Falha no login'
        return {'form':form.render(appstruct={'nome':nome,'senha':senha}),
                'mensagem' : mensagem,
                'url' : request.application_url + '/login',
                'came_from' : came_from,
               }
    return {'form':form.render()}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('inicial'), headers = headers)

@view_config(route_name='inicial', renderer='inicial.slim')
def incial(request):
    logado = authenticated_userid(request)
    return {'logado': logado,
           }

@view_config(route_name='criar_perfil', renderer='registrar.slim')
def criar_perfil(request):
    form = deform.Form(FormRegistrar(), buttons=('Registrar',))
    if 'Registrar' in request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            return {'form':e.render()}
        dbsession = DBSession()
        record = BdJogador()
        record = merge_session_with_post(record, request.POST.items())
        dbsession.merge(record)
        dbsession.flush()
        return {'sucesso': 'True'}
    return {'form':form.render()}

@view_config(route_name='editar_perfil', renderer='editar_perfil.slim',
             permission='jogar')
def editar_perfil(request):
    dbsession = DBSession()
    record = dbsession.query(BdJogador).filter_by(nome=request.matchdict['nome']).first()
    if record == None:
        return {'perdido':'True'}
    else:
        form = deform.Form(FormEditar(), buttons=('Alterar',))
        if 'Alterar' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
            except deform.ValidationFailure, e:
                return {'form':e.render()}
            record = merge_session_with_post(record, request.POST.items())
            dbsession.merge(record)
            dbsession.flush()
            return {'sucesso': 'True'}
        else:
            appstruct = record_to_appstruct(record)
        return {'form':form.render(appstruct=appstruct)}

# CHAT
@view_config(route_name='enviar_msg', permission='jogar')
def receber_msg(request):
    jogador = authenticated_userid(request)
    if jogador:
        msg = request.POST["msg"]
        num = CHAT.adi_msg('central', jogador, msg)
        return Response(str(num))
    return HTTPForbidden

@view_config(route_name='ret_msgs', permission='jogar')
def ret_msgs(request):
    jogador = authenticated_userid(request)
    if jogador:
        msgs = CHAT.ret_msgs('central')
        print "aaaaaaaaaaaaaa",msgs, CHAT.salas["central"].msgs
        pa = render_to_response('chat_msgs.slim',{'msgs':msgs})
        ret = {}
        ret["msgs"] = pa.body
        return Response(json.dumps(ret))
    return HTTPForbidden


# JOGO
@view_config(route_name='jogo', renderer='jogo.slim', permission='jogar')
def nova_pagina(request):
    return CONTROLADOR.nova_pagina()

#@app.route('/jogada', methods=['POST'])
@view_config(route_name='jogada', permission='jogar')
def nova_jogada(request):
    jogador = authenticated_userid(request)
    jogada = request.POST["jogada"]
    return Response(CONTROLADOR.executar(jogador, jogada))

#@app.route('/atualizar', methods=['POST'])
@view_config(route_name='atualizar', permission='jogar')
def enviar_atualizacao(request):
    jogador = authenticated_userid(request)
    num = request.POST["num_jogada"]
    return Response(CONTROLADOR.nova_atualizacao(jogador, num))

#@app.route('/baralho', methods=['GET'])
@view_config(route_name='baralho')
def enviar_baralho(request):
    cartas = {} 
    for c in CONTROLADOR.jogo.baralho:
        cartas[c] = dict(CONTROLADOR.jogo.baralho[c].__dict__)
        cartas[c].pop("efeito")
        cartas[c].pop("efeito_dados")
    return Response(json.dumps(cartas))
