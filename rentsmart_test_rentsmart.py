# Autor: Gustavo Henrique de Souza | RA: 241061
# Repositório: https://github.com/Gh083048-hs/Rentsmart

import unittest
import os
from imoveis import Apartamento, Casa, Estudio
from orcamento import Contrato, OrcamentoLocacao


class TestRentSmart(unittest.TestCase):
    """Testes unitários das regras de negócio da R.M Imóveis."""

    def test_apartamento_2_quartos_garagem_sem_criancas(self):
        # Base 700 + 200 (2 quartos) + 300 (garagem) = 1200 -> -5% = 1140.00
        apto = Apartamento(quartos=2, tem_garagem=True, tem_criancas=False)
        self.assertEqual(apto.calcular_aluguel_mensal(), 1140.00)

    def test_apartamento_1_quarto_sem_garagem_com_criancas(self):
        apto = Apartamento(quartos=1, tem_garagem=False, tem_criancas=True)
        self.assertEqual(apto.calcular_aluguel_mensal(), 700.00)

    def test_casa_2_quartos_com_garagem(self):
        # Base 900 + 250 (2 quartos) + 300 (garagem) = 1450.00
        casa = Casa(quartos=2, tem_garagem=True)
        self.assertEqual(casa.calcular_aluguel_mensal(), 1450.00)

    def test_estudio_com_3_vagas(self):
        # Base 1200 + 250 (2 vagas) + 60 (1 extra) = 1510.00
        estudio = Estudio(vagas_estacionamento=3)
        self.assertEqual(estudio.calcular_aluguel_mensal(), 1510.00)

    def test_contrato_parcelamento_e_csv(self):
        contrato = Contrato(parcelas=4)
        self.assertEqual(contrato.valor_parcela(), 500.00)

        casa = Casa(quartos=1, tem_garagem=False)
        orcamento = OrcamentoLocacao(imovel=casa, contrato=contrato)
        projecao = orcamento.gerar_projecao_12_meses()

        self.assertEqual(len(projecao), 12)
        self.assertEqual(projecao[0]["Total_Mes"], "1400.00")  # Mês 1 com parcela
        self.assertEqual(projecao[4]["Total_Mes"], "900.00")   # Mês 5 sem parcela

        arquivo_teste = "teste_projecao.csv"
        orcamento.exportar_csv(arquivo_teste)
        self.assertTrue(os.path.exists(arquivo_teste))
        os.remove(arquivo_teste)


if __name__ == "__main__":
    unittest.main()
