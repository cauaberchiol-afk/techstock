# TechStock - Sistema de controle de estoque

produtos = []
movimentacoes = []


def mostrar_menu():
    print("\n========== TECHSTOCK ==========")
    print("[1] Cadastrar produto")
    print("[2] Registrar entrada")
    print("[3] Registrar venda")
    print("[4] Ficha do produto")
    print("[5] Gráfico do estoque")
    print("[6] Inventário por prateleira")
    print("[7] Relatório do dia")
    print("[8] Alterar preço")
    print("[9] Excluir produto")
    print("[10] Buscar produto por código")
    print("[11] Atualizar nome ou quantidade")
    print("[12] Relatório geral do estoque")
    print("[0] Sair")


def buscar_produto(codigo):
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto
    return None


def mostrar_produto(produto):
    print("\nCódigo:", produto["codigo"])
    print("Nome:", produto["nome"])
    print("Quantidade:", produto["quantidade"])
    print(f"Preço: R$ {produto['preco']:.2f}")
    print("Prateleira:", produto["prateleira"])


def calcular_subtotal(produto):
    return produto["quantidade"] * produto["preco"]


def cadastrar_produto():
    print("\n--- Cadastro de produto ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Digite um código válido.")
        return

    if buscar_produto(codigo) is not None:
        print("Código já cadastrado!")
        return

    nome = input("Nome: ")

    try:
        quantidade = int(input("Quantidade: "))
        preco = float(input("Preço: ").replace(",", "."))
    except ValueError:
        print("Digite valores válidos.")
        return

    if quantidade < 0 or preco < 0:
        print("Quantidade e preço não podem ser negativos.")
        return

    prateleira = input("Prateleira: ")

    novo = {
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco,
        "prateleira": prateleira
    }

    produtos.append(novo)
    print("Produto cadastrado!")


def registrar_entrada():
    print("\n--- Registrar entrada ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade que entrou: "))
    except ValueError:
        print("Digite uma quantidade válida.")
        return

    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")
        return

    produto["quantidade"] += quantidade

    movimentacoes.append({
        "tipo": "Entrada",
        "produto": produto["nome"],
        "quantidade": quantidade
    })

    print("Entrada registrada!")


def registrar_venda():
    print("\n--- Registrar venda ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade vendida: "))
    except ValueError:
        print("Digite uma quantidade válida.")
        return

    if quantidade <= 0:
        print("A quantidade precisa ser maior que zero.")

    elif quantidade > produto["quantidade"]:
        print("Não há estoque suficiente.")

    else:
        produto["quantidade"] -= quantidade
        valor = quantidade * produto["preco"]

        movimentacoes.append({
            "tipo": "Venda",
            "produto": produto["nome"],
            "quantidade": quantidade,
            "valor": valor
        })

        print(f"Venda registrada! Total: R$ {valor:.2f}")


def ficha_produto():
    print("\n--- Ficha do produto ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
    else:
        mostrar_produto(produto)
        print(f"Valor em estoque: R$ {calcular_subtotal(produto):.2f}")


def grafico_estoque():
    print("\n--- Gráfico do estoque ---")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        barras = "#" * min(produto["quantidade"], 40)
        print(f"{produto['nome']}: {barras} ({produto['quantidade']})")


def inventario_prateleira():
    print("\n--- Inventário por prateleira ---")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    prateleira = input("Digite a prateleira: ")
    encontrou = False

    for produto in produtos:
        if produto["prateleira"].lower() == prateleira.lower():
            mostrar_produto(produto)
            encontrou = True

    if not encontrou:
        print("Nenhum produto nessa prateleira.")


def relatorio_dia():
    print("\n--- Relatório do dia ---")

    if len(movimentacoes) == 0:
        print("Ainda não existem movimentações.")
        return

    total_vendas = 0

    for movimento in movimentacoes:
        print(
            movimento["tipo"], "-",
            movimento["produto"],
            "- Quantidade:", movimento["quantidade"]
        )

        if movimento["tipo"] == "Venda":
            total_vendas += movimento["valor"]

    print(f"Total vendido: R$ {total_vendas:.2f}")


def alterar_preco():
    print("\n--- Alterar preço ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    try:
        novo_preco = float(input("Novo preço: ").replace(",", "."))
    except ValueError:
        print("Digite um preço válido.")
        return

    if novo_preco < 0:
        print("O preço não pode ser negativo.")
    else:
        produto["preco"] = novo_preco
        print("Preço atualizado!")


def excluir_produto():
    print("\n--- Excluir produto ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
    else:
        produtos.remove(produto)
        print("Produto excluído!")


def consultar_produto():
    print("\n--- Buscar produto ---")

    try:
        codigo = int(input("Código para buscar: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
    else:
        mostrar_produto(produto)


def atualizar_produto():
    print("\n--- Atualizar produto ---")

    try:
        codigo = int(input("Código do produto: "))
    except ValueError:
        print("Código inválido.")
        return

    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    print("1 - Alterar nome")
    print("2 - Alterar quantidade")

    escolha = input("Escolha: ")

    if escolha == "1":
        produto["nome"] = input("Novo nome: ")
        print("Nome atualizado!")

    elif escolha == "2":
        try:
            nova_quantidade = int(input("Nova quantidade: "))
        except ValueError:
            print("Digite uma quantidade válida.")
            return

        if nova_quantidade < 0:
            print("Quantidade inválida!")
        else:
            produto["quantidade"] = nova_quantidade
            print("Quantidade atualizada!")

    else:
        print("Opção inválida.")


def relatorio_geral():
    print("\n====== RELATÓRIO GERAL ======")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    total_estoque = 0

    for produto in produtos:
        subtotal = calcular_subtotal(produto)
        total_estoque += subtotal

        print("\n", produto["codigo"], "-", produto["nome"])
        print("Quantidade:", produto["quantidade"])
        print(f"Preço unitário: R$ {produto['preco']:.2f}")
        print(f"Subtotal: R$ {subtotal:.2f}")

    print(f"\nTotal do estoque: R$ {total_estoque:.2f}")


opcao = ""

while opcao != "0":

    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_produto()

    elif opcao == "2":
        registrar_entrada()

    elif opcao == "3":
        registrar_venda()

    elif opcao == "4":
        ficha_produto()

    elif opcao == "5":
        grafico_estoque()

    elif opcao == "6":
        inventario_prateleira()

    elif opcao == "7":
        relatorio_dia()

    elif opcao == "8":
        alterar_preco()

    elif opcao == "9":
        excluir_produto()

    elif opcao == "10":
        consultar_produto()

    elif opcao == "11":
        atualizar_produto()

    elif opcao == "12":
        relatorio_geral()

    elif opcao == "0":
        print("Saindo do TechStock...")

    else:
        print("Opção inválida. Tente novamente.")