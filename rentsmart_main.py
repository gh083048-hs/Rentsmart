# Autor: Gustavo Henrique de Souza | RA: 241061
# Repositório: https://github.com/Gh083048-hs/Rentsmart

from imoveis import Apartamento, Casa, Estudio
from orcamento import Contrato, OrcamentoLocacao


def obter_opcao_valida(mensagem: str, opcoes_validas: list[str]) -> str:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes_validas:
            return resposta
        print(f"Opção inválida! Digite uma das opções: {', '.join(opcoes_validas)}")


def obter_inteiro_valido(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"Valor fora do intervalo! Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida! Por favor, digite apenas números inteiros.")


def main():
    print("=" * 55)
    print("RENTSMART - SISTEMA DE ORÇAMENTO DE LOCAÇÃO (R.M IMÓVEIS)")
    print("Aluno: Gustavo Henrique de Souza | RA: 241061")
    print("=" * 55)
    print("Selecione a categoria do imóvel:")
    print("1 - Apartamento (Base: R$ 700,00)")
    print("2 - Casa (Base: R$ 900,00)")
    print("3 - Estúdio (Base: R$ 1.200,00)")

    categoria = obter_inteiro_valido("Escolha (1 a 3): ", 1, 3)

    if categoria == 1:
        quartos = obter_inteiro_valido("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = obter_opcao_valida("Deseja vaga de garagem? (+R$ 300,00) [s/n]: ", ["s", "n"])
        criancas = obter_opcao_valida("Possui crianças? (Sem crianças = 5% de desconto) [s/n]: ", ["s", "n"])
        imovel = Apartamento(
            quartos=quartos,
            tem_garagem=(garagem == "s"),
            tem_criancas=(criancas == "s"),
        )
    elif categoria == 2:
        quartos = obter_inteiro_valido("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = obter_opcao_valida("Deseja vaga de garagem? (+R$ 300,00) [s/n]: ", ["s", "n"])
        imovel = Casa(
            quartos=quartos,
            tem_garagem=(garagem == "s"),
        )
    else:
        quer_vagas = obter_opcao_valida("Deseja contratar estacionamento? (Pacote 2 vagas = R$ 250,00) [s/n]: ", ["s", "n"])
        if quer_vagas == "s":
            vagas = obter_inteiro_valido("Total de vagas desejadas (mínimo 2, máximo 10): ", 2, 10)
        else:
            vagas = 0
        imovel = Estudio(vagas_estacionamento=vagas)

    parcelas = obter_inteiro_valido(
        "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00? (1 a 5): ",
        1,
        5,
    )

    contrato = Contrato(parcelas=parcelas)
    orcamento = OrcamentoLocacao(imovel=imovel, contrato=contrato)

    orcamento.exibir_resumo()
    arquivo_csv = orcamento.exportar_csv()
    print(f"\nArquivo CSV gerado com sucesso: {arquivo_csv}")


if __name__ == "__main__":
    main()
