import re
import objetos
import requests


def pegar_nome(nome):
    nome_separado = nome.split()
    try:
        if nome_separado[0][-1] == 'x':
            nome_separado[0] = nome_separado[0][:-1]
        nome_separado[0] = int(nome_separado[0])
        nome_separado.remove(nome_separado[0])
    except:
        pass

    nome_junto = nome_separado[0]
    for i in nome_separado[1:]:
        nome_junto +=' ' + i

    return (nome_separado, nome_junto)

def get_source(nome_separado, nome_junto):
    print(nome_junto, end ='')

    url = "https://www.ligamagic.com.br/?view=cards%2Fsearch&card=" + nome_separado[0]
    for i in range(1, len(nome_separado)):
        url += "+" + nome_separado[i]

    try:
        r = requests.get(url)
        source = str(r.content)
    except:
        print("\nConfira sua internet ou leia o README.txt pra mais informações")
        raise ValueError

    inf = 'marketplace-lojas'
    sup = 'exibir_mais'
    try:
        lim_inf = int(source.index(inf))
        lim_sup = int(source.index(sup))
        source = source[lim_inf:lim_sup]
    except:
        print("\nConfira a carta", nome_junto + '. Corrija-a, por favor, ou tente trocar a língua:  ', end="")
        aux = input()
        nome_separado, nome_junto = pegar_nome(aux)
        print()
        return get_source(nome_separado, nome_junto)

    print("!")

    source = source.split('line')
    return source[1:]

def gerar_lista_de_ofertas_carta(nome, lista):

    over = re.compile(r'Oversize')
    loja = re.compile(r'title=\"(?!Visitar Loja)[\w\s\d]*')
    preco = re.compile(r'R. \d?\d?\d?\d,\d\d')
    edicao = re.compile(r'e-mob-edicao-lbl"><p>[\w\s]*')
    qualidade = re.compile(r'cardQualidade.\d.')

    def pegar_preco(price):
        for i in range(len(price)):
            price[i] = float(price[i][3:].replace(',','.'))
        price.sort()
        try:
            return price[0]
        except:
            pass

    nome_separado, nome_junto = pegar_nome(nome)
    source = get_source(nome_separado, nome_junto)
    atual = objetos.carta(nome_junto)

    for i in source:
        oversize = over.search(i)
        if oversize != None:
            continue

        lojas = loja.findall(i)
        lojas = lojas[0][7:]

        price = preco.findall(i)
        price = pegar_preco(price)
        if price == None:
            continue

        ed = edicao.findall(i)
        ed = ed[0][21:]

        qual = qualidade.findall(i)
        qual = int(qual[0][14:-1])

        atual.inclui(objetos.oferta(lojas, price, qual, ed))

    lista.inclui(atual)
