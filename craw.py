import re
import objetos
import urllib.request
import compra

over = re.compile(r'Oversize')
loja = re.compile(r'title=\"(?!Visitar Loja)[\w\s\d]*')
preco = re.compile(r'R. \d?\d?\d?\d,\d\d')
edicao = re.compile(r'e-mob-edicao-lbl"><p>[\w\s]*')
qualidade = re.compile(r'cardQualidade.\d.')

lands = ["floresta", "forest", "island", "ilha", "swamp", "pantano", "pântano", "planície", "planicie", "plains"]

encode = {"ç": "c", "ã": "a", "õ": "o", "â": "a", "á": "a", "à": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "ú": "u"}

def pegar_nome(nome):
    for i in encode.keys():
        while True:
            try:
                nome.index(i)
                nome = nome.replace(i, encode[i])
            except:
                break

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
        r = urllib.request.urlopen(url)
        source = r.read()
        source = str(source)
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
        print("\nConfira a carta", nome_junto + '. Corrija-a, por favor, ou tente trocar a língua (caso deseja ignorar, digite \"ignore\"):  ', end="")
        aux = input()
        if aux == "ignore":
            return 0
        nome_separado, nome_junto = pegar_nome(aux)
        print()
        return get_source(nome_separado, nome_junto)

    print("!")

    source = source.split('line')
    return source[1:]

def gerar_lista_de_ofertas_carta(nome, lista):

    def pegar_preco(price):
        for i in range(len(price)):
            price[i] = float(price[i][3:].replace(',','.'))
        price.sort()
        try:
            return price[0]
        except:
            pass

    nome_separado, nome_junto = pegar_nome(nome)

    if nome_junto.lower() in lands:
        return

    source = get_source(nome_separado, nome_junto)
    if source == 0:
        return
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
