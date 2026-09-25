"""
Módulo de persistência.

Responsável por ler e gravar os dados dos alunos em um arquivo JSON
(RF07: manter os dados disponíveis depois que o programa for encerrado).
Trata erros de arquivo com cuidado, sem derrubar o aplicativo (RNF04).
"""

import json
import os

PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
ARQUIVO_DADOS = os.path.join(PASTA_DADOS, "alunos.json")


def _garantir_pasta_dados() -> None:
    os.makedirs(PASTA_DADOS, exist_ok=True)


def carregar_alunos() -> list[dict]:
    """
    Carrega a lista de alunos do arquivo JSON.
    Se o arquivo não existir ou estiver corrompido, retorna lista vazia
    em vez de travar o programa.
    """
    _garantir_pasta_dados()

    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            if isinstance(conteudo, list):
                return conteudo
            return []
    except (json.JSONDecodeError, OSError):
        # Arquivo corrompido ou inacessível: começa com lista vazia
        # em vez de encerrar o aplicativo inesperadamente.
        return []


def salvar_alunos(alunos: list[dict]) -> tuple[bool, str]:
    """
    Grava a lista de alunos no arquivo JSON.
    Retorna (sucesso, mensagem_erro).
    """
    _garantir_pasta_dados()

    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(alunos, arquivo, ensure_ascii=False, indent=2)
        return True, ""
    except OSError as erro:
        return False, f"Não foi possível salvar os dados: {erro}"
