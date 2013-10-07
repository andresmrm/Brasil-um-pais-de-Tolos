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

import json

from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget, authenticated_userid
import deform

from .models import DBSession, BdJogador
from jogo import *
from forms import *


# DELETAR ISSO!!!!!!!!!!!!
PREJOGO = SistemaPreJogo()
PREJOGO.criar_jogo("a","1")
PREJOGO.colocar_jogador_jogo("a","olegal")
PREJOGO.colocar_jogador_jogo("a","legalzao")
PREJOGO.colocar_jogador_jogo("a","1")
PREJOGO.ret_jogador("olegal").automatico = True
PREJOGO.ret_jogador("legalzao").automatico = True
PREJOGO.iniciar_jogo("a")

j = PREJOGO.jogos["a"]
j.jogadores["1"].mao.append(51)
for i,c in j.baralho.items():
    print(i,c.naipe, c.valor, c.nome)
#j.jogadores["olegal"].mesa["fic"] = [1,2,3]
#j.jogadores["olegal"].mesa["esp"] = [20,21,22]

# PREPARACAO

@forbidden_view_config(renderer='proibida.slim')
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    logado = authenticated_userid(request)
    if logado:
        return {'logado':logado}
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
                #'came_from' : came_from,
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

@view_config(route_name='sala_central', renderer='central.slim', permission='jogar')
def salas_central(request):
    logado = authenticated_userid(request)
    if 'criar_sala' in request.POST:
        nome = request.POST.get("nome",'')
        PREJOGO.colocar_jogador_jogo(nome, logado)
        return HTTPFound(location = request.route_url('sala', {'nome': nome}))
    PREJOGO.colocar_jogador_jogo(PREJOGO.central, logado)
    return {'logado': logado,
           }

@view_config(route_name='sala', renderer='sala.slim', permission='jogar')
def sala(request):
    logado = authenticated_userid(request)
    sala = request.matchdict['nome']
    if PREJOGO.criar_jogo(sala, logado):
        return {'logado': logado,
                'sala': sala,
               }
    else:
        return HTTPFound(location = request.route_url('sala_central'))


@view_config(route_name='fim', renderer='final.slim', permission='jogar')
def fim(request):
    logado = authenticated_userid(request)
    nome_jogo = request.matchdict['nome']
    jogo = PREJOGO.ret_jogo(nome_jogo)
    jogadores = jogo.ret_jogadores()
    ganhador = jogo.ret_jog_mais_pontos().nome
    return {'logado': logado,
            'ganhador': ganhador,
            'jogadores': jogadores,
           }

@view_config(route_name='atualizar_central', permission='jogar')
def atualizar_central(request):
    salas = PREJOGO.ret_jogos()
    s = render_to_response('listar_salas.slim',{'salas':salas}, request=request).body
    jogs = PREJOGO.ret_jogadores(PREJOGO.central)
    j = render_to_response('jogadores_central.slim',{'jogs':jogs}, request=request).body
    ret = {
        "salas": s,
        "jogadores": j
    }
    return Response(json.dumps(ret))

@view_config(route_name='atualizar_sala', permission='jogar')
def atualizar_sala(request):
    nome_sala = request.matchdict['nome']
    jogs = PREJOGO.ret_jogadores(nome_sala)

    todos_prontos = True
    for j in jogs:
        if not j.pronto:
            todos_prontos = False

    if not todos_prontos:
        j = render_to_response('jogadores_sala.slim',{'jogs':jogs},request=request).body
        ret = {
            "jogadores": j
        }
        return Response(json.dumps(ret))
    else:
        PREJOGO.iniciar_jogo(nome_sala)
        dbsession = DBSession()
        #bd_jogadores = dbsession.query.filter(BdJogador.nome.in_(jogs))
        #bd_jogadores = dbsession.query(BdJogador).filter(BdJogador.nome.in_(jogs))
        nome_jogs = [j.nome for j in jogs]
        bd_jogadores = dbsession.query(BdJogador).filter(BdJogador.nome.in_(nome_jogs)).all()
        for j in bd_jogadores:
            j.partidas += 1
        ret = {'link': request.route_url('jogo', nome=nome_sala)}
        return Response(json.dumps(ret))

@view_config(route_name='pronto', permission='jogar')
def pronto(request):
    nome_jogador = authenticated_userid(request)
    jogador = PREJOGO.ret_jogador(nome_jogador)
    jogador.pronto = not jogador.pronto
    return Response("OK")


# PERFIS

@view_config(route_name='criar_perfil', renderer='registrar.slim')
def criar_perfil(request):
    form = deform.Form(FormRegistrar(), buttons=('Registrar',))
    if 'Registrar' in request.POST:
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure, e:
            return {'form':e.render()}
        dbsession = DBSession()

        atribs = request.POST
        nome = atribs["nome"]
        senha = atribs["senha"]

        record = BdJogador(nome, senha)
        record = merge_session_with_post(record, request.POST.items())
        dbsession.merge(record)
        dbsession.flush()
        return {'sucesso': 'True'}
    appstruct = record_to_appstruct(record)
    return {'form':form.render(appstruct=appstruct)}

@view_config(route_name='ver_perfil', renderer='ver_perfil.slim')
def ver_perfil(request):
    dbsession = DBSession()
    record = dbsession.query(BdJogador).filter_by(nome=request.matchdict['nome']).first()
    logado = authenticated_userid(request)
    if record == None:
        return {'perdido':'True'}
    else:
        appstruct = record_to_appstruct(record)
        if appstruct['nome'] == logado:
            appstruct['e_o_proprio'] = True
        return appstruct
        #return {'form':form.render(appstruct=appstruct)}

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
    nome_jogador = authenticated_userid(request)
    nome_sala = request.matchdict['nome']
    if nome_jogador:
        msg = request.POST["msg"]
        num = PREJOGO.adi_msg(nome_sala, nome_jogador, msg)
        return Response(str(num))
    return HTTPForbidden

@view_config(route_name='ret_msgs', permission='jogar')
def ret_msgs(request):
    ret = {}
    nome_sala = request.matchdict['nome']
    msgs = PREJOGO.ret_msgs(nome_sala)
    pa = render_to_response('chat_msgs.slim',{'msgs':msgs})
    ret["msgs"] = pa.body
    #jogs = PREJOGO.ret_jogadores(nome_sala)
    #pa = render_to_response('participantes.slim',{'jogs':jogs})
    #ret["participantes"] = pa.body
    return Response(json.dumps(ret))


# JOGO
@view_config(route_name='jogo', renderer='jogo.slim', permission='jogar')
def nova_pagina(request):
    nome_jogador = authenticated_userid(request)
    return PREJOGO.nova_pagina(nome_jogador)

@view_config(route_name='jogada', permission='jogar')
def nova_jogada(request):
    nome_jogo = request.matchdict['nome']
    nome_jogador = authenticated_userid(request)
    jogada = request.POST["jogada"]
    msg = PREJOGO.executar(nome_jogador, jogada)
    if msg[:3] == "FIM":
        jogo = PREJOGO.ret_jogo(nome_jogo)
        ganhador = jogo.ret_jog_mais_pontos()
        dbsession = DBSession()
        j = dbsession.query(BdJogador).filter_by(nome=ganhador.nome).first()
        j.vitorias += 1
        j.pontos += 1
    return Response(msg)

@view_config(route_name='atualizar_jogo', permission='jogar')
def enviar_atualizacao(request):
    nome_jogo = request.matchdict['nome']
    nome_jogador = authenticated_userid(request)
    num = request.POST["num_jogada"]
    r = PREJOGO.nova_atualizacao(nome_jogador, num)
    if r == "0":
        return Response(r)
    ret, j, b, d = r
    for jog in j:
        if jog['nome'] == nome_jogador:
            dic_jog = jog
    pa = render_to_response('mao.slim',{'jogador':dic_jog,'baralho':b})
    ret["mao"] = pa.body
    pa = render_to_response('mesas.slim',{'jogadores':j,'baralho':b, 'descarte':d})
    ret["mesas"] = pa.body
    return Response(json.dumps(ret))

@view_config(route_name='baralho', permission='jogar')
def enviar_baralho(request):
    nome_jogo = request.matchdict['nome']
    nome_jogador = authenticated_userid(request)

    jogador = PREJOGO.ret_jogador(nome_jogador)
    if jogador:
        baralho = jogador.jogo.baralho
        cartas = {} 
        for c in baralho:
            cartas[c] = dict(baralho[c].__dict__)
            cartas[c].pop("efeito")
            cartas[c].pop("efeito_dados")
        print("LA VAI!!!!!!!!!!!!!!!!!!!!!!!")
        return Response(json.dumps(cartas))
    else:
        Response()

@view_config(route_name='rank', renderer='rank.slim')
def rank(request):
    nome_jogador = authenticated_userid(request)
    dbsession = DBSession()
    jogadores = dbsession.query(BdJogador).all()
    jogadores.sort(key=lambda j: j.pontos, reverse=True)
    for j in jogadores:
        j.posicao = jogadores.index(j)+1
    return {'jogadores': jogadores,
            'logado' : nome_jogador
           }
