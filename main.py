import re
import objetos
import craw
import os

def ler_deck():
    print("Fazendo o download dos preços...")
    lista = objetos.compra()
    nome_do_arq = 'deck.txt'
    deck = open(nome_do_arq, 'r')
    atual = 'aa'
    while True:
        atual = deck.readline()
        if atual.split() == []:
            break
        craw.gerar_lista_de_ofertas_carta(atual, lista)
    deck.close()
    return lista

def menu():
    print()
    while True:
        try:
            qualidade_min = int(input("Digite a qualidade mínima: (1 = M, 2 = NM, 3 = SP, 4 = MP, 5 = HP ou 6 = D)  "))
            lista.remove_qualidade(qualidade_min)
            break
        except:
            print("Invalido, tente novamente")

    lista.remove_loja_rep()

    while True:
        try:
            frete = float(input('Digite o valor médio de um frete: '))
            lista.remove_frete(frete)
            break
        except:
            print("Invalido, tente novamente")

    return frete

def calcular(lista_comp):
    compra = []
    qtd = 0
    while not lista_comp.lista_de_cartas == []:
        if len(lista_comp.lista_de_cartas) == 1:
            qtd += 1
            if qtd == 2:
                print("\n\nInfelizmente a carta", lista_comp.lista_de_cartas[0].nome, "deve ser retirada do deck para que possamos calcular\n")
                raise ValueError
                break

        pont = lista_comp.calcula()

        maior_valor = 0
        loja = ''

        for key in pont.keys():
            if pont[key][0] >= maior_valor:
                maior_valor = pont[key][0]
                aux = pont[key][1]
                loja = key
        compra.append(loja)
        for i in aux:
            for j in lista_comp.lista_de_cartas:
                if i == j.nome:
                    lista_comp.lista_de_cartas.remove(j)
                    break
    return compra

def imprimir(lista_impr):
    qualid = ["n/a", "M  ", "NM ", "SP ", "MP ", "HP ", "D  "]
    lista_impr.sort()
    valor_total = 0
    print('\n\n\n' + "Loja", " "*20, "Carta", ' '*28, 'Edição', ' '*21, 'Qualidade', ' '* 5, 'Diferença', ' '*4, "Preço", '\n')
    for i in lista_impr:
        print(i[0], ' '*(25 - len(i[0])), end='')
        print(i[1], ' '*(34 - len(i[1])), end='')
        print(i[2], ' '*(28 - len(i[2])), end='')
        print(qualid[i[3]], ' '*12, end='')
        print('%2.2f' %i[4], ' '*10, end ='')
        print('%2.2f' %i[5] )
        valor_total += i[5]

    lojas = 1
    for i in range(len(lista_impr)-1):
        if lista_impr[i][0] != lista_impr[i+1][0]:
            lojas += 1

    print()
    print(' '*104, 'valor total: R$ %2.2f' %valor_total)
    print(' '*104, '  com frete: R$ %2.2f' %(valor_total+(lojas*frete)))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

lista = ler_deck()
aux = lista.copy()
frete = menu()

while True:
    cls()
    imprimir(aux.final(calcular(aux.copy())))
    comand = input("Press 1-Remover carta   Q-Sair    ")
    if comand == "q" or comand == "Q":
        break
    if comand:
        print("Escolha (pelo número) qual carta deseja remover da lista antes de ser recalculada (pode colocar uma lista de números também):")
        aux.imprime_nome_cartas()
        rem = input().split()
        list_rem = []
        for i in rem:
            list_rem.append(aux.index(int(i)))
        for i in list_rem:
            aux.remove(i)
