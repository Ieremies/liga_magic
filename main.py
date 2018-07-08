import objetos
import craw
import compra
import funcoes

def menu_config():
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

    return (frete, qualidade_min)

lista = funcoes.ler_deck()
aux = lista.copy()
frete, qualidade_min = menu_config()

while True:
    funcoes.cls()
    funcoes.imprimir(aux.final(funcoes.calcular(aux.copy()), frete), frete)
    command = input("Press 1-Remover carta   2-Adicionar carta  Q-Sair    ")
    if command == "q" or command == "Q":
        break
    if command == "1":
        print("Escolha (pelo número) qual carta deseja remover da lista antes de ser recalculada (pode colocar uma lista de números também):")
        aux.imprime_nome_cartas()
        rem = input().split()
        list_rem = []
        for i in rem:
            list_rem.append(aux.index(int(i)))
        for i in list_rem:
            aux.remove(i)
    if command == "2":
        nome = input("Digite o nome da carta:   ")
        craw.gerar_lista_de_ofertas_carta(nome, aux)
        #craw.gerar_lista_de_ofertas_carta(nome, lista)
        aux.remove_frete(frete)
        aux.remove_qualidade(qualidade_min)
