import json
import os

Arquivo = "estoque.json"

PRODUTOS = []
MOVIMENTACOES = []
HISTORICO = []
FILA_REPOSICAO = []


def SALVAR_ESTOQUE():
    with open(Arquivo, "w") as arquivo:
        json.dump(PRODUTOS, arquivo, indent=4)


def CARREGAR_ESTOQUE():
    global PRODUTOS
    if os.path.exists(Arquivo):
        with open(Arquivo, "r") as arquivo:
            PRODUTOS = json.load(arquivo)


def LER_PRECO():
    while True:
        preco_str = input("Digite o preço do produto: R$ ")
        try:
            preco = float(preco_str.replace(",", "."))
            if preco < 0:
                print("ERRO: o preço não pode ser negativo.")
            else:
                return preco
        except ValueError:
            print("ERRO: digite um valor numérico válido para o preço.")


def MOSTRAR_PRODUTO(produto):
    print(f"Nome: {produto['nome']}")
    print(f"Quantidade: {produto['quantidade']}")
    print(f"Preço: R$ {produto['preco']:.2f}")


def CALCULAR_VALOR_TOTAL(produto):
    return produto["quantidade"] * produto["preco"]


def REGISTRAR_ENTRADA(produto, quantidade):
    produto["quantidade"] += quantidade
    MOVIMENTACOES.append({
        "CODIGO": produto["codigo"],
        "nome": produto["nome"],
        "quantidade": quantidade,
        "tipo": "Entrada"
    })


def EXIBIR_MOVIMENTACOES():
    if not MOVIMENTACOES:
        print("Nenhuma movimentação registrada.")
        return
    for movimentacao in MOVIMENTACOES:
        print(
            f"{movimentacao['tipo']}: {movimentacao['nome']} "
            f"(código {movimentacao['CODIGO']}), "
            f"quantidade: {movimentacao['quantidade']}"
        )


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
    for produto in PRODUTOS:
        if produto["codigo"] == codigo:
            return produto
    return None


def cadastrar_produto():
    print("\n--- Cadastro de produto ---")
    codigo = input("Código: ").strip()
    if not codigo:
        print("ERRO: o código do produto não pode ser vazio.")
        return
    if buscar_produto(codigo) is not None:
        print("Código já cadastrado!")
        return

    nome = input("Nome: ").strip()
    if not nome:
        print("ERRO: o nome do produto não pode ser vazio.")
        return

    preco = LER_PRECO()
    try:
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("ERRO: digite uma quantidade inteira válida.")
        return
    if quantidade < 0:
        print("ERRO: a quantidade não pode ser negativa.")
        return
    prateleira = input("Prateleira: ").strip()

    PRODUTOS.append({
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco,
        "prateleira": prateleira
    })
    SALVAR_ESTOQUE()
    print("Produto cadastrado com sucesso!")


def registrar_entrada():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade de entrada: "))
    except ValueError:
        print("ERRO: digite uma quantidade inteira válida.")
        return
    if quantidade <= 0:
        print("ERRO: a quantidade de entrada precisa ser maior que zero.")
        return

    REGISTRAR_ENTRADA(produto, quantidade)
    SALVAR_ESTOQUE()
    print("Entrada registrada com sucesso!")


def ficha_produto():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    print("\n--- Ficha do Produto ---")
    print(f"Código: {produto['codigo']}")
    print(f"Nome: {produto['nome']}")
    print(f"Quantidade: {produto['quantidade']}")
    print(f"Preço: R$ {produto['preco']:.2f}")
    print(f"Prateleira: {produto.get('prateleira', '')}")


def grafico_estoque():
    if not PRODUTOS:
        print("Nenhum produto cadastrado.")
        return
    for produto in PRODUTOS:
        quantidade = produto["quantidade"]
        barra = "*" * quantidade
        print(f"{produto['nome']}: {barra} ({quantidade})")


def inventario_prateleira():
    if not PRODUTOS:
        print("Nenhum produto cadastrado.")
        return
    prateleiras = input("Digite as prateleiras separadas por vírgula: ").split(",")
    for prateleira in (p.strip() for p in prateleiras):
        produtos_na_prateleira = [
            produto for produto in PRODUTOS
            if produto.get("prateleira", "") == prateleira
        ]
        if not produtos_na_prateleira:
            print(f"Não há produtos na prateleira {prateleira}.")
            continue
        print(f"\n--- Inventário da Prateleira {prateleira} ---")
        for produto in produtos_na_prateleira:
            print(
                f"Código: {produto['codigo']}, Nome: {produto['nome']}, "
                f"Quantidade: {produto['quantidade']}, "
                f"Preço: R$ {produto['preco']:.2f}"
            )


def relatorio_geral():
    if not PRODUTOS:
        print("Nenhum produto cadastrado.")
        return

    for produto in PRODUTOS:
        print("\n--- Relatório do Produto ---")
        MOSTRAR_PRODUTO(produto)
        print(f"Valor em estoque: R$ {CALCULAR_VALOR_TOTAL(produto):.2f}")

        entradas = 0
        vendas = 0
        unidades_vendidas = 0
        faturamento = 0

        for movimentacao in MOVIMENTACOES:
            if movimentacao["CODIGO"] == produto["codigo"]:
                if movimentacao["tipo"] == "Entrada":
                    entradas += movimentacao["quantidade"]
                elif movimentacao["tipo"] == "Venda":
                    vendas += 1
                    unidades_vendidas += movimentacao["quantidade"]
                    faturamento += movimentacao["quantidade"] * produto["preco"]

        print(f"Entradas: {entradas}")
        print(f"Vendas: {vendas}")
        print(f"Unidades vendidas: {unidades_vendidas}")
        print(f"Faturamento: R$ {faturamento:.2f}")
        print("-----------------------------")


def registrar_venda():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade vendida: "))
    except ValueError:
        print("ERRO: digite uma quantidade inteira válida.")
        return

    if quantidade <= 0:
        print("ERRO: a quantidade vendida precisa ser maior que zero.")
        return
    if quantidade > produto["quantidade"]:
        print("ERRO: estoque insuficiente.")
        return

    produto["quantidade"] -= quantidade
    MOVIMENTACOES.append({
        "CODIGO": produto["codigo"],
        "nome": produto["nome"],
        "quantidade": quantidade,
        "tipo": "Venda"
    })
    SALVAR_ESTOQUE()
    print("Venda registrada com sucesso!")
    print(f"Estoque atual: {produto['quantidade']}")


def alterar_preco():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    novo_preco = LER_PRECO()
    produto["preco"] = novo_preco
    SALVAR_ESTOQUE()
    print("Preço alterado com sucesso!")


def excluir_produto():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    PRODUTOS.remove(produto)
    SALVAR_ESTOQUE()
    print("Produto excluído com sucesso!")


def consultar_produto_por_codigo():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    MOSTRAR_PRODUTO(produto)
    print(f"Valor em estoque: R$ {CALCULAR_VALOR_TOTAL(produto):.2f}")


def atualizar_nome_ou_quantidade():
    codigo = input("Código do produto: ").strip()
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    print("1 - Atualizar nome")
    print("2 - Atualizar quantidade")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        novo_nome = input("Novo nome: ").strip()
        if not novo_nome:
            print("ERRO: o nome do produto não pode ser vazio.")
            return
        produto["nome"] = novo_nome
        SALVAR_ESTOQUE()
        print("Nome atualizado com sucesso!")
    elif opcao == "2":
        try:
            nova_quantidade = int(input("Nova quantidade: "))
        except ValueError:
            print("ERRO: digite uma quantidade inteira válida.")
            return
        if nova_quantidade < 0:
            print("ERRO: a quantidade não pode ser negativa.")
            return
        produto["quantidade"] = nova_quantidade
        SALVAR_ESTOQUE()
        print("Quantidade atualizada com sucesso!")
    else:
        print("Opção inválida.")


def relatorio_geral_do_estoque():
    if not PRODUTOS:
        print("Nenhum produto cadastrado.")
        return

    for produto in PRODUTOS:
        MOSTRAR_PRODUTO(produto)
        print(f"Valor em estoque: R$ {CALCULAR_VALOR_TOTAL(produto):.2f}")
        print("-----------------------------")


def desfazer_ultima_movimentacao():
    if not MOVIMENTACOES:
        print("Nenhuma movimentação registrada.")
        return

    ultima_movimentacao = MOVIMENTACOES.pop()
    produto = buscar_produto(ultima_movimentacao["CODIGO"])
    if produto is None:
        print("Produto não encontrado.")
        return

    if ultima_movimentacao["tipo"] == "Entrada":
        produto["quantidade"] -= ultima_movimentacao["quantidade"]
        if produto["quantidade"] < 0:
            produto["quantidade"] = 0
    elif ultima_movimentacao["tipo"] == "Venda":
        produto["quantidade"] += ultima_movimentacao["quantidade"]

    SALVAR_ESTOQUE()
    print("Última movimentação desfeita com sucesso!")
    print(f"Estoque atual: {produto['quantidade']}")


def mostrar_historico_movimentacoes():
    if not MOVIMENTACOES:
        print("Nenhuma movimentação registrada.")
        return

    for movimentacao in MOVIMENTACOES:
        print(
            f"{movimentacao['tipo']}: {movimentacao['nome']} "
            f"(código {movimentacao['CODIGO']}), "
            f"quantidade: {movimentacao['quantidade']}"
        )
        print("-----------------------------")


def pedir_reposicao():
    if not PRODUTOS:
        print("Nenhum produto cadastrado.")
        return

    FILA_REPOSICAO.clear()
    for produto in PRODUTOS:
        if produto["quantidade"] < 5:
            FILA_REPOSICAO.append(produto)

    if not FILA_REPOSICAO:
        print("Nenhum produto precisa de reposição.")
        return

    print("\n--- Fila de Reposição ---")
    for i, produto in enumerate(FILA_REPOSICAO, start=1):
        print(f"{i} - {produto['nome']} (Quantidade: {produto['quantidade']})")


def receber_reposicao():
    if not FILA_REPOSICAO:
        print("Nenhum produto na fila de reposição.")
        return

    for produto in list(FILA_REPOSICAO):
        try:
            quantidade = int(input(f"Digite a quantidade recebida para o produto {produto['nome']}: "))
        except ValueError:
            print("ERRO: digite uma quantidade inteira válida.")
            continue

        if quantidade <= 0:
            print("ERRO: a quantidade precisa ser maior que zero.")
            continue

        REGISTRAR_ENTRADA(produto, quantidade)
        print(f"Reposição registrada para o produto {produto['nome']}.")

    FILA_REPOSICAO.clear()
    SALVAR_ESTOQUE()
    print("Fila de reposição esvaziada e estoque atualizado.")


def atualizar_fila_reposicao():
    pedir_reposicao()


def main():
    CARREGAR_ESTOQUE()
    while True:
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
        print("[13] Desfazer última movimentação")
        print("[14] Histórico de movimentações")
        print("[15] Pedir reposição")
        print("[16] Receber reposição")
        print("[0] Sair")

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
            relatorio_geral()
        elif opcao == "8":
            alterar_preco()
        elif opcao == "9":
            excluir_produto()
        elif opcao == "10":
            consultar_produto_por_codigo()
        elif opcao == "11":
            atualizar_nome_ou_quantidade()
        elif opcao == "12":
            relatorio_geral_do_estoque()
        elif opcao == "13":
            desfazer_ultima_movimentacao()
        elif opcao == "14":
            mostrar_historico_movimentacoes()
        elif opcao == "15":
            pedir_reposicao()
        elif opcao == "16":
            receber_reposicao()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

