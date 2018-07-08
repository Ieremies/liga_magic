import objetos
from itertools import combinations

class compra:
    def __init__(self):
        self.lista_de_cartas = []

    def inclui(self, carta):
        self.lista_de_cartas.append(carta)

    def imprime_nome_cartas(self):
        for i in range(len(self.lista_de_cartas)):
            print(i, "-", self.lista_de_cartas[i].nome)

    def remove(self, x):
        self.lista_de_cartas.remove(x)

    def index(self, x):
        return self.lista_de_cartas[x]

    def remove_qualidade(self, q):
        for carta in self.lista_de_cartas:
            carta.remove_qualidade_carta(q)

    def remove_loja_rep(self):
        for carta in self.lista_de_cartas:
            carta.remove_loja_rep_carta()

    def remove_frete(self, valor):
        for carta in self.lista_de_cartas:
            carta.remove_frete_carta(valor)

    def calcula(self):
        dict = {}
        for carta in self.lista_de_cartas:
            dict = carta.calcula(dict)
        return dict

    def copy(self):
        copiada = compra()
        copiada.lista_de_cartas = self.lista_de_cartas.copy()
        return copiada

    def final(self, compra, frete):
        valor = 999999999999
        op = []
        for i in range(1, len(compra)+1):
            for j in combinations(compra, i):
                ok = True
                aux = []
                for carta in self.lista_de_cartas:
                    aux.append(carta.final(j))
                valor_total = frete*i
                for k in aux:
                    try:
                        valor_total += k[5]
                    except:
                        ok = False
                        break
                if not ok:
                    continue
                if valor_total < valor:
                    valor = valor_total
                    op = aux
        return op
