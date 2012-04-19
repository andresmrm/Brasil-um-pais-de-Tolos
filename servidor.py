from flask import Flask
from flask import render_template
from flask import request
from slimish_jinja import SlimishExtension

from jogo import *


class BPT(Flask):
    jinja_options = Flask.jinja_options
    jinja_options['extensions'].append(SlimishExtension)

app = BPT(__name__)
app.debug = True

@app.route('/')
def rodar_jogo():
    j1 = Jogador()
    j1.nome = "Tolo1"
    j1.mao = [1,2,3,4]
    j1.pegar_dinheiro()
    j1.mesa = { 'vermelho':[1,2,3,4,5,6,7,8,9],
                'azul':[1,2],
                'amarelo': [1],
                'verde': [1],
                'laranja': [1,4,6,8],
                'roxo':[1]} 
    j2 = Jogador()
    j2.nome = "Tolo2"
    j3 = Jogador()
    j3.nome = "Tolo3"
    j3.mesa = { 'vermelho':[1,2,9],}
    j4 = Jogador()
    j4.nome = "Tolo4"
    j5 = Jogador()
    j5.nome = "Tolo5"
    jogadores = [ j.__dict__ for j in [j1, j2, j3, j4, j5]]

    return render_template('jogo.slim',jogadores=jogadores)


@app.route('/jogada', methods=['POST'])
def teste():
    print request.form
    print request.form["nome"]
    return "Aceita!"

if __name__  == '__main__':
    app.run()
