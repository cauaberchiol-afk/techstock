# ============================================
#  TechStock - Controle de estoque TechPoint
#  Aluno(a): Cauã Berchiol
# ============================================

print("Bem-vindo ao TechStock - Controle de Estoque TechPoint")

# Sistema de Controle de Estoque - Etapa 3

produtos = [
    {"nome": "Mouse", "quantidade": 10, "preco": 25.00},
    {"nome": "Teclado", "quantidade": 4, "preco": 80.00},
    {"nome": "Monitor", "quantidade": 2, "preco": 500.00}
]


def listar():
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\n=== PRODUTOS CADASTRADOS ===")

    for indice in range(len(produtos)):
        produto = produtos[indice]

        situacao = ""

        if produto["quantidade"] == 0:
            situacao = " | SEM ESTOQUE"

        print(f'{indice + 1} - {produto["nome"]} | '
              f'Qtd: {produto["quantidade"]} | '
              f'R$ {produto["preco"]:.2f}{situacao}')

    print(f"Tipos de produtos: {len(produtos)}")

    baixo = 0

    for indice in range(len(produtos)):
        if produtos[indice]["quantidade"] < 5:
            baixo = baixo + 1

    print("Produtos com menos de 5 unidades:", baixo)


def consultar_numero():
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    listar()

    texto = input("Digite o número do produto: ")

    if not texto.isdigit():
        print("Digite um número inteiro válido.")
        return

    numero = int(texto)

    if numero < 1 or numero > len(produtos):
        print("Produto fora da lista.")
        return

    produto = produtos[numero - 1]

    print(f'Produto: {produto["nome"]}')
    print(f'Quantidade: {produto["quantidade"]}')
    print(f'Preço: R$ {produto["preco"]:.2f}')

    valor_total = produto["quantidade"] * produto["preco"]

    print(f"Valor total: R$ {valor_total:.2f}")


def adicionar_produto():
    nome = input("Nome do produto: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))

    if quantidade < 0 or preco <= 0:
        print("Quantidade ou preço inválido.")
    else:
        produto = {
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco
        }

        produtos.append(produto)

        print("Produto cadastrado.")


opcao = ""

while opcao != "0":
    print("\n===== CONTROLE DE ESTOQUE =====")
    print("1 - Listar produtos")
    print("2 - Consultar pelo número")
    print("3 - Adicionar produto")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        listar()

    elif opcao == "2":
        consultar_numero()

    elif opcao == "3":
        adicionar_produto()

    elif opcao == "0":
        print("Encerrando...")

    else:
        print("Opção inválida.")