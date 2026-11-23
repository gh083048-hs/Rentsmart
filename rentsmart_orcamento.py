# Autor: Gustavo Henrique de Souza | RA: 241061
# Repositório: https://github.com/Gh083048-hs/Rentsmart

import csv
from imoveis import Imovel


class Contrato:
    """Gerencia a taxa contratual fixa de R$ 2.000,00 e seu parcelamento."""

    TAXA_CONTRATUAL = 2000.00

    def __init__(self, parcelas: int):
        if not (1 <= parcelas <= 5):
            raise ValueError("A taxa contratual pode ser parcelada em 1 a 5 vezes.")
        self.parcelas = parcelas

    def valor_parcela(self) -> float:
        return round(self.TAXA_CONTRATUAL / self.parcelas, 2)


class OrcamentoLocacao:
    """Consolida o orçamento mensal, a taxa contratual e a projeção de 12 meses."""

    def __init__(self, imovel: Imovel, contrato: Contrato):
        self.imovel = imovel
        self.contrato = contrato

    def gerar_projecao_12_meses(self) -> list[dict]:
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcela_contrato = self.contrato.valor_parcela()
        projecao = []

        for mes in range(1, 13):
            taxa_mes = parcela_contrato if mes <= self.contrato.parcelas else 0.00
            total_mes = round(aluguel_mensal + taxa_mes, 2)
            projecao.append({
                "Mes": f"Mês {mes}",
                "Aluguel_Mensal": f"{aluguel_mensal:.2f}",
                "Taxa_Contrato": f"{taxa_mes:.2f}",
                "Total_Mes": f"{total_mes:.2f}",
            })
        return projecao

    def exportar_csv(self, nome_arquivo: str = "projecao_locacao_12_meses.csv") -> str:
        projecao = self.gerar_projecao_12_meses()
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel_Mensal (R$)", "Taxa_Contrato (R$)", "Total_Mes (R$)"])
            for linha in projecao:
                escritor.writerow([
                    linha["Mes"],
                    linha["Aluguel_Mensal"],
                    linha["Taxa_Contrato"],
                    linha["Total_Mes"],
                ])
        return nome_arquivo

    def exibir_resumo(self) -> None:
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        parcela_contrato = self.contrato.valor_parcela()

        print("\n" + "=" * 55)
        print("RESUMO DETALHADO DO ORÇAMENTO - RENTSMART")
        print("Desenvolvido por: Gustavo Henrique de Souza | RA: 241061")
        print("=" * 55)
        print(f"Categoria do Imóvel: {self.imovel.tipo}")
        print("\nComposição do Aluguel Mensal:")
        for item in self.imovel.detalhar_composicao():
            print(f"  • {item}")
        print(f"-> Valor do Aluguel Mensal Líquido: R$ {aluguel_mensal:.2f}")
        print("-" * 55)
        print("Taxa Contratual (separada do aluguel mensal):")
        print(f"  • Valor Total da Taxa: R$ {self.contrato.TAXA_CONTRATUAL:.2f}")
        print(f"  • Condição Escolhida: {self.contrato.parcelas}x de R$ {parcela_contrato:.2f}")
        print("-" * 55)
        print(f"Total previsto nos primeiros {self.contrato.parcelas} mês(es): R$ {aluguel_mensal + parcela_contrato:.2f}/mês")
        if self.contrato.parcelas < 12:
            print(f"Total previsto do {self.contrato.parcelas + 1}º ao 12º mês: R$ {aluguel_mensal:.2f}/mês")
        print("=" * 55)
