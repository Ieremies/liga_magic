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

    def final(self, compra):
        aux = []
        for carta in self.lista_de_cartas:
            aux.append(carta.final(compra))
        return aux


class oferta:
    def __init__(self, loja, preco, qualidade, edicao):
        self.loja = loja
        self.preco = preco
        self.qualidade = qualidade
        self.edicao = edicao

    def imprime(self):
        print(self.loja, ' '*(45-len(self.loja)), end='')
        print('R$ %0.2f' %self.preco, ' '*(20-len(str('R$ %0.2f' %self.preco))), end = '')
        print(self.edicao, ' '*(30-len(self.edicao)), end='')
        print("qualid.:", self.qualidade)

class carta:
    def __init__(self, nome):
        self.nome = nome
        self.lista = []

    def inclui(self, oferta):
        self.lista.append(oferta)

    def remove_qualidade_carta(self, q):
        i = 0
        while i < len(self.lista):
            if self.lista[i].qualidade > q:
                self.lista.remove(self.lista[i])
                i -= 1
            i += 1

    def remove_loja_rep_carta(self):
        tamanho = len(self.lista)
        i = 0
        while i < tamanho:
            j = i +1
            while j < tamanho:
                if self.lista[i].loja == self.lista[j].loja:
                    self.lista.remove(self.lista[j])
                    tamanho -= 1
                    j -= 1
                j += 1
            i+=1

    def remove_frete_carta(self, valor):
        valor_prim = self.lista[0].preco + valor
        for outra in self.lista[1:]:
            if outra.preco > valor_prim:
                self.lista.remove(outra)

    def calcula(self, dict):
        pont = self.lista[-1].preco - self.lista[0].preco
        cont = pont / len(self.lista)
        for op in self.lista:
            if op.loja in dict.keys():
                dict[op.loja][0] += pont
                dict[op.loja][1].append(self.nome)
                pont -= cont
            else:
                dict[op.loja] = [pont, [self.nome]]
                pont -= cont
        return dict

    def final(self, compra):
        for op in self.lista:
            if op.loja in compra:
                return (op.loja, self.nome, op.edicao, op.qualidade, op.preco - self.lista[0].preco, op.preco)
