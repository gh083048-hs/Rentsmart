# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

**Desenvolvido por:** Gustavo Henrique de Souza  
**RA:** 241061  
**Repositório GitHub:** https://github.com/Gh083048-hs/Rentsmart  

## Sobre o Projeto
Aplicação desenvolvida em Python aplicando **Pensamento Algorítmico** e **Programação Orientada a Objetos (POO)** para automatizar os orçamentos de locação da **R.M Imóveis**, separando responsabilidades em módulos organizados.

## Estrutura dos Arquivos
- `imoveis.py`: Contém a classe abstrata `Imovel` e as subclasses `Apartamento`, `Casa` e `Estudio` com suas regras de cálculo e composição.
- `orcamento.py`: Contém as classes `Contrato` (taxa contratual de R$ 2.000,00 em até 5x) e `OrcamentoLocacao` (resumo detalhado e exportação da projeção de 12 meses em `.csv`).
- `main.py`: Arquivo principal de execução via terminal, responsável pela interação com o usuário e validação das entradas.
- `test_rentsmart.py`: Suíte de testes unitários automatizados (`unittest`) validando todas as regras de negócio.
- `README.md`: Documentação de instruções e arquitetura do projeto.

## Como Executar
1. Certifique-se de ter o **Python 3.10+** instalado.
2. No terminal, navegue até a pasta do projeto e execute o programa principal:
   ```bash
   python main.py
   ```
3. Para rodar os testes unitários automatizados:
   ```bash
   python -m unittest test_rentsmart.py
   ```
