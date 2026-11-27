
# TechStock 2.0 - Controle de estoque TechPoint
# Aluno(a): Cauã Berchiol

print("=================================")
print("   TECHSTOCK 2.0 - TECHPOINT")
print("=================================")

# Cadastro do produto
codigo = input("Código do produto: ")
nome = input("Nome do produto: ")

preco = float(input("Preço de venda (R$): "))
while preco <= 0:
    print("ERRO: o preço precisa ser maior que zero.")
    preco = float(input("Preço de venda (R$): "))

quantidade = int(input("Quantidade em estoque: "))
while quantidade < 0:
    print("ERRO: a quantidade não pode ser negativa.")
    quantidade = int(input("Quantidade em estoque: "))

estoque_minimo = int(input("Estoque mínimo: "))
while estoque_minimo < 0:
    print("ERRO: o estoque mínimo não pode ser negativo.")
    estoque_minimo = int(input("Estoque mínimo: "))

print("Produto cadastrado!")

# Contadores e acumuladores
qtd_entradas = 0
qtd_vendas = 0
unidades_vendidas = 0
faturamento = 0

# Menu principal
opcao = ""

while opcao != "0":
    print()
    print("============ MENU ============")
    print("[1] Registrar entrada")
    print("[2] Registrar venda")
    print("[3] Vendas em sequência")
    print("[4] Ficha do produto")
    print("[5] Gráfico do estoque")
    print("[6] Inventário por prateleira")
    print("[7] Relatório do dia")
    print("[0] Sair")

    opcao = input("Escolha uma opção: ")

    # Registrar entrada
    if opcao == "1":
        entrada = int(input("Quantas unidades chegaram? "))

        while entrada <= 0:
            print("ERRO: digite um valor maior que zero.")
            entrada = int(input("Quantas unidades chegaram? "))

        quantidade = quantidade + entrada
        qtd_entradas = qtd_entradas + 1

        print("Entrada registrada. Estoque atual:", quantidade)

    # Registrar venda
    elif opcao == "2":
        if quantidade <= 0:
            print("Produto SEM ESTOQUE. Não é possível vender.")
        else:  
            saida = int(input("Quantas unidades foram vendidas? "))

            while saida <= 0 or saida > quantidade:
                print("ERRO: digite um valor entre 1 e", quantidade)
                saida = int(input("Quantas unidades foram vendidas? "))

            quantidade = quantidade - saida
            qtd_vendas = qtd_vendas + 1
            unidades_vendidas = unidades_vendidas + saida
            faturamento = faturamento + (saida * preco)

            print("Venda registrada. Estoque atual:", quantidade)

    # Vendas em sequência
    elif opcao == "3":
        total = int(input("Quantas vendas você quer registrar? "))

        while total < 0:
            print("Digite zero ou um número positivo.")
            total = int(input("Quantas vendas você quer registrar? "))

        for i in range(1, total + 1):
            if quantidade == 0:
                print("O estoque acabou! Encerrando as vendas.")
                break

            print("Venda", i)
            saida = int(input("Unidades vendidas: "))

            if saida <= 0 or saida > quantidade:
                print("Venda ignorada: valor inválido.")
                continue

            quantidade = quantidade - saida
            qtd_vendas = qtd_vendas + 1
            unidades_vendidas = unidades_vendidas + saida
            faturamento = faturamento + (saida * preco)

            print("Venda", i, "registrada. Estoque atual:", quantidade)

    # Ficha do produto
    elif opcao == "4":
        valor_total = round(preco * quantidade, 2)

        print()
        print("------- FICHA DO PRODUTO -------")
        print("Código:", codigo)
        print("Produto:", nome)
        print("Preço: R$", round(preco, 2))
        print("Quantidade em estoque:", quantidade)
        print("Estoque mínimo:", estoque_minimo)
        print("Valor total em estoque: R$", valor_total)

        if quantidade <= estoque_minimo:
            print("Situação: ESTOQUE BAIXO")
        else:
            print("Situação: ESTOQUE OK")

        print("--------------------------------")

    # Gráfico do estoque
    elif opcao == "5":
        barra = ""

        for i in range(quantidade):
            barra = barra + "#"

        marca = ""

        for i in range(estoque_minimo):
            marca = marca + "#"

        print("Estoque:", barra, quantidade)
        print("Mínimo: ", marca, estoque_minimo)

    # Inventário por prateleira
    elif opcao == "6":
        prateleiras = int(input("Quantas prateleiras guardam o produto? "))
        caixas = int(input("Quantas caixas tem cada prateleira? "))

        while prateleiras < 0 or caixas < 0:
            print("Digite quantidades que não sejam negativas.")
            prateleiras = int(input("Quantas prateleiras guardam o produto? "))
            caixas = int(input("Quantas caixas tem cada prateleira? "))

        total_contado = 0

        for p in range(1, prateleiras + 1):
            soma_prateleira = 0

            for c in range(1, caixas + 1):
                print("Prateleira", p, "- caixa", c)
                unidades = int(input("Unidades na caixa: "))

                while unidades < 0:
                    print("A quantidade não pode ser negativa.")
                    unidades = int(input("Unidades na caixa: "))

                soma_prateleira = soma_prateleira + unidades

            print("Total da prateleira", p, "=", soma_prateleira)
            total_contado = total_contado + soma_prateleira

        print("Total contado:", total_contado, "| No sistema:", quantidade)

        if total_contado == quantidade:
            print("Contagem confere com o sistema!")
        else:
            diferenca = total_contado - quantidade
            print("Diferença de", diferenca, "unidade(s). Estoque ajustado.")
            quantidade = total_contado

    # Relatório do dia
    elif opcao == "7":
        print()
        print("------- RELATÓRIO DO DIA -------")
        print("Entradas registradas:", qtd_entradas)
        print("Vendas registradas:", qtd_vendas)
        print("Unidades vendidas:", unidades_vendidas)
        print("Faturamento: R$", round(faturamento, 2))

        if qtd_vendas > 0:
            media = unidades_vendidas / qtd_vendas
            print("Média por venda:", round(media, 1), "unidade(s)")

        print("--------------------------------")

    elif opcao == "0":
        print("Encerrando o TechStock... até logo!")

    else:
        print("Opção inválida. Tente de novo.")

