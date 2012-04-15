import os
import random


DIR_CARTAS = "cartas"
MAX_CARTAS_MAO = 5


class Jogo():

    def __init__(self):
        self.baralho = {}
        self.jogadores = []
        self.monte = []

    def adi_jogador(self, jog): 
        self.jogadores.append(jog)

    def montar_baralho(self):
        nomes_arqs = os.listdir(DIR_CARTAS)
        for nome in nomes_arqs:
            with open(os.path.join(DIR_CARTAS, nome)) as arq:
                linhas = arq.read().splitlines()
                atributos = {}
                for linha in linhas:
                    tipo, valor = linha.split(":")
                    atributos[tipo.strip()] = valor.strip()
                c = Carta(nome=atributos['nome'],
                          num=atributos['valor'],
                          naipe=atributos['naipe'],
                          efeito=atributos['efeito'])
                self.baralho[len(self.baralho)] = c

    def distribuir_cartas(self):
        for j in self.jogadores:
            j.adi_carta(self.monte.pop())
            j.adi_carta(self.monte.pop())

    def iniciar(self):
        self.montar_baralho()
        self.monte = list(self.baralho.keys())
        random.shuffle(self.monte)
        self.distribuir_cartas()


class Jogador():

    def __init__(self):
        self.nome = "Tolo"
        self.dinheiro = 5
        self.mao = []
        self.mesa = {}

    def adi_carta(self, carta):
        if len(self.mao) < MAX_CARTAS_MAO:
            self.mao.append(carta)

class Carta():

    def __init__(self, nome="Boba", num=1, naipe="Azul", efeito=None):
        self.nome = nome
        self.num = num
        self.naipe = naipe
        self.efeito = efeito


j = Jogo()
j1 = Jogador()
j2 = Jogador()
j3 = Jogador()

j.adi_jogador(j1)
j.adi_jogador(j2)
j.adi_jogador(j3)

j.iniciar()

for jog in j.jogadores:
    print jog.mao
print j.monte
