"""
Módulo de validações.

Centraliza as regras de validação de dados do sistema (RNF03) e o
cálculo de média e situação do aluno (RF08), para que interface.py
e dados.py não precisem repetir essas regras.
"""

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 10.0
MEDIA_APROVACAO = 6.0
MEDIA_RECUPERACAO = 4.0


def validar_nome(nome: str) -> tuple[bool, str]:
    """Valida o nome do aluno. Retorna (ok, mensagem_erro)."""
    nome = nome.strip()
    if not nome:
        return False, "O nome do aluno é obrigatório."
    if len(nome) < 2:
        return False, "O nome deve ter pelo menos 2 caracteres."
    if any(char.isdigit() for char in nome):
        return False, "O nome não deve conter números."
    return True, ""


def validar_turma(turma: str) -> tuple[bool, str]:
    """Valida o campo turma. Retorna (ok, mensagem_erro)."""
    turma = turma.strip()
    if not turma:
        return False, "A turma é obrigatória."
    return True, ""


def validar_nota(valor_texto: str) -> tuple[bool, str, float | None]:
    """
    Valida um valor de nota digitado como texto.
    Retorna (ok, mensagem_erro, valor_convertido_ou_None).
    """
    valor_texto = valor_texto.strip().replace(",", ".")
    if not valor_texto:
        return False, "Digite um valor de nota antes de adicionar.", None

    try:
        nota = float(valor_texto)
    except ValueError:
        return False, "A nota deve ser um número (ex.: 7.5).", None

    if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
        return False, f"A nota deve estar entre {NOTA_MINIMA:.1f} e {NOTA_MAXIMA:.1f}.", None

    return True, "", round(nota, 2)


def validar_notas_preenchidas(notas: list[float]) -> tuple[bool, str]:
    """Garante que o aluno tenha ao menos uma avaliação antes de salvar."""
    if not notas:
        return False, "Adicione ao menos uma avaliação antes de salvar."
    return True, ""


def calcular_media(notas: list[float]) -> float:
    """Calcula a média aritmética das notas. Retorna 0.0 se a lista for vazia."""
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), 2)


def calcular_situacao(media: float) -> str:
    """Classifica a situação do aluno a partir da média (RF08)."""
    if media >= MEDIA_APROVACAO:
        return "Aprovado"
    if media >= MEDIA_RECUPERACAO:
        return "Recuperação"
    return "Reprovado"
