import csv
from abc import ABC, abstractmethod


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel da R.M Imóveis."""

    def __init__(self, tipo: str, aluguel_base: float):
        self.tipo = tipo
        self.aluguel_base = aluguel_base

    @abstractmethod
    def calcular_aluguel_mensal(self) -> float:
        """Calcula o valor final do aluguel mensal com adicionais e descontos."""
        pass

    @abstractmethod
    def detalhar_composicao(self) -> list[str]:
        """Retorna uma lista legível explicando como o valor do aluguel foi formado."""
        pass


class Apartamento(Imovel):
    """Representa um apartamento com regras de quartos, garagem e desconto sem crianças."""

    def __init__(self, quartos: int, tem_garagem: bool, tem_criancas: bool):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.tem_criancas = tem_criancas

    def calcular_aluguel_mensal(self) -> float:
        valor = self.aluguel_base
        if self.quartos == 2:
            valor += 200.00
        if self.tem_garagem:
            valor += 300.00
        if not self.tem_criancas:
            valor *= 0.95  # Desconto de 5% após aplicação dos adicionais
        return round(valor, 2)

    def detalhar_composicao(self) -> list[str]:
        detalhes = [f"Aluguel-base (1 quarto): R$ {self.aluguel_base:.2f}"]
        subtotal = self.aluguel_base

        if self.quartos == 2:
            detalhes.append("Adicional 2º quarto: + R$ 200,00")
            subtotal += 200.00
        if self.tem_garagem:
            detalhes.append("Adicional vaga de garagem: + R$ 300,00")
            subtotal += 300.00
        if not self.tem_criancas:
            desconto = subtotal * 0.05
            detalhes.append(f"Desconto comercial (5% sem crianças): - R$ {desconto:.2f}")

        return detalhes


class Casa(Imovel):
    """Representa uma casa com regras de quartos e vaga de garagem."""

    def __init__(self, quartos: int, tem_garagem: bool):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_aluguel_mensal(self) -> float:
        valor = self.aluguel_base
        if self.quartos == 2:
            valor += 250.00
        if self.tem_garagem:
            valor += 300.00
        return round(valor, 2)

    def detalhar_composicao(self) -> list[str]:
        detalhes = [f"Aluguel-base (1 quarto): R$ {self.aluguel_base:.2f}"]
        if self.quartos == 2:
            detalhes.append("Adicional 2º quarto: + R$ 250,00")
        if self.tem_garagem:
            detalhes.append("Adicional vaga de garagem: + R$ 300,00")
        return detalhes


class Estudio(Imovel):
    """Representa um estúdio com pacote inicial de 2 vagas e vagas adicionais."""

    def __init__(self, vagas_estacionamento: int):
        super().__init__("Estúdio", 1200.00)
        self.vagas_estacionamento = vagas_estacionamento

    def calcular_aluguel_mensal(self) -> float:
        valor = self.aluguel_base
        if self.vagas_estacionamento >= 2:
            valor += 250.00  # Pacote inicial de 2 vagas
            vagas_extras = self.vagas_estacionamento - 2
            valor += vagas_extras * 60.00
        return round(valor, 2)

    def detalhar_composicao(self) -> list[str]:
        detalhes = [f"Aluguel-base Estúdio: R$ {self.aluguel_base:.2f}"]
        if self.vagas_estacionamento == 0:
            detalhes.append("Estacionamento: Sem vagas contratadas (R$ 0,00)")
        elif self.vagas_estacionamento >= 2:
            detalhes.append("Pacote inicial de estacionamento (2 vagas): + R$ 250,00")
            vagas_extras = self.vagas_estacionamento - 2
            if vagas_extras > 0:
                custo_extras = vagas_extras * 60.00
                detalhes.append(
                    f"Vagas extras ({vagas_extras}x R$ 60,00): + R$ {custo_extras:.2f}"
                )
        return detalhes


class Contrato:
    """Gerencia a taxa contratual fixa e suas condições de parcelamento."""

    TAXA_CONTRATUAL = 2000.00

    def __init__(self, parcelas: int):
        if not (1 <= parcelas <= 5):
            raise ValueError("A taxa contratual deve ser parcelada entre 1 e 5 vezes.")
        self.parcelas = parcelas

    def valor_parcela(self) -> float:
        return round(self.TAXA_CONTRATUAL / self.parcelas, 2)


class GeradorProjecaoCSV:
    """Responsável por gerar a projeção financeira de 12 meses e exportar em CSV."""

    def __init__(self, imovel: Imovel, contrato: Contrato, nome_arquivo: str = "projecao_locacao_12_meses.csv"):
        self.imovel = imovel
        self.contrato = contrato
        self.nome_arquivo = nome_arquivo

    def gerar_linhas(self) -> list[list[str]]:
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcela_contrato = self.contrato.valor_parcela()
        linhas = []

        for mes in range(1, 13):
            valor_taxa_mes = parcela_contrato if mes <= self.contrato.parcelas else 0.00
            total_mes = round(aluguel_mensal + valor_taxa_mes, 2)
            linhas.append([
                f"Mês {mes:02d}",
                self.imovel.tipo,
                f"{aluguel_mensal:.2f}",
                f"{valor_taxa_mes:.2f}",
                f"{total_mes:.2f}",
            ])
        return linhas

    def exportar(self) -> str:
        linhas = self.gerar_linhas()
        with open(self.nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow([
                "Mes",
                "Categoria_Imovel",
                "Aluguel_Mensal_R$",
                "Parcela_Taxa_Contrato_R$",
                "Total_Previsto_Mes_R$",
            ])
            escritor.writerows(linhas)
        return self.nome_arquivo


def obter_opcao_valida(mensagem: str, opcoes_validas: list[str]) -> str:
    """Valida respostas textuais do usuário dentro de um conjunto permitido."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes_validas:
            return resposta
        print(f"[Erro] Opção inválida. Digite uma das opções: {', '.join(opcoes_validas)}.")


def obter_inteiro_valido(mensagem: str, minimo: int, maximo: int) -> int:
    """Valida entradas numéricas inteiras dentro de um intervalo fechado."""
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo <= valor <= maximo:
                return valor
            print(f"[Erro] Informe um número inteiro entre {minimo} e {maximo}.")
        except ValueError:
            print("[Erro] Entrada inválida. Digite apenas números inteiros.")


def obter_vagas_estudio() -> int:
    """Valida a regra específica de estacionamento do Estúdio (0 vagas ou pacote mínimo de 2)."""
    while True:
        try:
            vagas = int(input("Quantas vagas de estacionamento deseja? (0 para nenhuma, ou mínimo 2): ").strip())
            if vagas == 0 or vagas >= 2:
                return vagas
            print("[Erro] Para estúdios, o pacote inicial exige no mínimo 2 vagas (ou digite 0 para não contratar).")
        except ValueError:
            print("[Erro] Entrada inválida. Digite apenas números inteiros.")


def exibir_resumo_orcamento(imovel: Imovel, contrato: Contrato) -> None:
    """Apresenta no terminal o detalhamento transparente do orçamento."""
    aluguel_mensal = imovel.calcular_aluguel_mensal()
    parcela_contrato = contrato.valor_parcela()

    print("\n" + "=" * 56)
    print("        ORÇAMENTO DETALHADO — RENTSMART (R.M IMÓVEIS)")
    print("=" * 56)
    print(f"Categoria do Imóvel: {imovel.tipo}")
    print("\nComposição do Aluguel Mensal:")
    for item in imovel.detalhar_composicao():
        print(f"  • {item}")
    print(f"-> Valor do Aluguel Mensal Líquido: R$ {aluguel_mensal:.2f}")

    print("\nTaxa Contratual (Custo Administrativo Separado):")
    print(f"  • Valor Total da Taxa: R$ {contrato.TAXA_CONTRATUAL:.2f}")
    print(f"  • Condição Escolhida: {contrato.parcelas}x de R$ {parcela_contrato:.2f}")

    print("\nResumo de Desembolso no Primeiro Ano:")
    print(f"  • Meses 1 a {contrato.parcelas}: R$ {aluguel_mensal + parcela_contrato:.2f}/mês (Aluguel + Parcela Contrato)")
    if contrato.parcelas < 12:
        print(f"  • Meses {contrato.parcelas + 1} a 12: R$ {aluguel_mensal:.2f}/mês (Somente Aluguel)")
    print("=" * 56)


def main() -> None:
    print("=" * 56)
    print("   BEM-VINDO AO RENTSMART — R.M IMÓVEIS")
    print("=" * 56)
    print("Selecione a categoria do imóvel para orçamento:")
    print("  1 - Apartamento")
    print("  2 - Casa")
    print("  3 - Estúdio")

    categoria = obter_inteiro_valido("Opção desejada (1 a 3): ", 1, 3)

    if categoria == 1:
        quartos = obter_inteiro_valido("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = obter_opcao_valida("Deseja incluir 1 vaga de garagem? (s/n): ", ["s", "n"])
        criancas = obter_opcao_valida("O cliente possui crianças? (s/n): ", ["s", "n"])
        imovel = Apartamento(
            quartos=quartos,
            tem_garagem=(garagem == "s"),
            tem_criancas=(criancas == "s"),
        )
    elif categoria == 2:
        quartos = obter_inteiro_valido("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = obter_opcao_valida("Deseja incluir 1 vaga de garagem? (s/n): ", ["s", "n"])
        imovel = Casa(
            quartos=quartos,
            tem_garagem=(garagem == "s"),
        )
    else:
        vagas = obter_vagas_estudio()
        imovel = Estudio(vagas_estacionamento=vagas)

    parcelas = obter_inteiro_valido(
        "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00? (1 a 5): ",
        1,
        5,
    )
    contrato = Contrato(parcelas=parcelas)

    exibir_resumo_orcamento(imovel, contrato)

    exportador = GeradorProjecaoCSV(imovel, contrato)
    caminho_csv = exportador.exportar()
    print(f"\n[Sucesso] Projeção de 12 meses exportada para: {caminho_csv}\n")


if __name__ == "__main__":
    main()