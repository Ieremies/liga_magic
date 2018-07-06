import re
import objetos
import craw

# TODO: salvar os valores logo dps de pega-los pra que toda vez que eu refizer a conta não ter que baixar d enovo a não ser que a ultima autalização tenha sido a mais de um dia

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
            qualidade_min = int(input("Digite a qualidade mínima: (1 = M, 2 = NM, 3 = SP, 4 = MP, 5 = HP ou 6 = D)    "))
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

def calcular(lista):
    compra = []
    qtd = 0
    while not lista.lista_de_cartas == []:
        if len(lista.lista_de_cartas) == 1:
            qtd += 1
            if qtd == 2:
                print("\n\nInfelizmente a carta", lista.lista_de_cartas[0].nome, "deve ser retirada do deck para que possamos calcular\n")
                raise ValueError
                break

        pont = lista.calcula()

        maior_valor = 0
        loja = ''

        for key in pont.keys():
            if pont[key][0] >= maior_valor:
                maior_valor = pont[key][0]
                aux = pont[key][1]
                loja = key
        compra.append(loja)
        for i in aux:
            for j in lista.lista_de_cartas:
                if i == j.nome:
                    lista.lista_de_cartas.remove(j)
                    break
    return compra

# TODO: cuidar da excessão de quando uma carta ficar sem ofertas válidas

def imprimir():
    qualid = ["n/a", "M  ", "NM ", "SP ", "MP ", "HP ", "D  "]
    lista_final.sort()
    valor_total = 0
    print('\n\n\n' + "Loja", " "*20, "Carta", ' '*28, 'Edição', ' '*21, 'Qualidade', ' '* 5, 'Diferença', ' '*4, "Preço", '\n')
    for i in lista_final:
        print(i[0], ' '*(25 - len(i[0])), end='')
        print(i[1], ' '*(34 - len(i[1])), end='')
        print(i[2], ' '*(28 - len(i[2])), end='')
        print(qualid[i[3]], ' '*12, end='')
        print('%2.2f' %i[4], ' '*10, end ='')
        print('%2.2f' %i[5] )
        valor_total += i[5]

    lojas = 1
    for i in range(len(lista_final)-1):
        if lista_final[i][0] != lista_final[i+1][0]:
            lojas += 1

    print()
    print(' '*104, 'valor total: R$ %2.2f' %valor_total)
    print(' '*104, '  com frete: R$ %2.2f' %(valor_total+(lojas*frete)))


lista = ler_deck()
frete = menu()
compra = calcular(lista.copy())
lista_final = lista.final(compra)
imprimir()
fim = input("Press enter to exit    ")
