"""
Acesso a páginas do portal Sankhya Developer.

O portal é baseado em documentação estática — sem necessidade de Selenium.
Como não existe rota de busca textual convencional, o acesso é feito diretamente
por URL. O modelo deve navegar pelas seções conhecidas para localizar o conteúdo.

Seções disponíveis:
    Guias:      https://developer.sankhya.com.br/docs/{slug}
    Receitas:   https://developer.sankhya.com.br/recipes/{slug}
    API Ref:    https://developer.sankhya.com.br/reference/{slug}

Execução direta (validação manual):
    python -m src.developer_sankhya "https://developer.sankhya.com.br/docs/conhecendo-o-portal"
"""
import sys

from src.config import (
    BASE_URL_DEVELOPER,
    DEVELOPER_SECAO_API,
    DEVELOPER_SECAO_GUIAS,
    DEVELOPER_SECAO_RECEITAS,
    DEVELOPER_URL_INDICE_API,
    DEVELOPER_URL_INDICE_GUIAS,
    DEVELOPER_URL_INDICE_RECEITAS,
    DOMINIO_DEVELOPER,
    HREF_PATTERNS_DEVELOPER,
    PREVIEW_LIMIT,
)
from src.leitor_paginas import extrair_conteudo_limpo


def _validar_dominio(url: str) -> str | None:
    """Retorna mensagem de erro se o domínio não for o Developer, ou None se for válido."""
    if DOMINIO_DEVELOPER not in url:
        return (
            f"Erro: esta ferramenta tem permissão apenas para acessar páginas do "
            f"Sankhya Developer ({DOMINIO_DEVELOPER})."
        )
    return None


def _validar_secao(url: str, secao: str) -> str | None:
    """Retorna mensagem de erro se a URL não pertencer à seção esperada, ou None se for válida."""
    if secao not in url:
        return (
            f"Erro: URL inválida para esta ferramenta. "
            f"Esperado uma página da seção '{secao}' "
            f"(ex.: {BASE_URL_DEVELOPER}{secao}{{slug}})."
        )
    return None


def _acessar_secao(url: str, secao: str) -> str:
    """
    Valida domínio e seção, depois delega a extração ao leitor de páginas.

    Args:
        url: URL da página a ser acessada.
        secao: Prefixo de caminho esperado (ex.: '/docs/').

    Returns:
        Texto limpo da página ou mensagem de erro.
    """
    if erro := _validar_dominio(url):
        return erro
    if erro := _validar_secao(url, secao):
        return erro
    return extrair_conteudo_limpo(url)


# ---------------------------------------------------------------------------
# API pública — uma função por seção
# ---------------------------------------------------------------------------


def acessar_guia(url: str) -> str:
    """
    Acessa uma página de Guias do portal Sankhya Developer.

    Contém documentação técnica estruturada: visão geral do portal, configuração
    de ambiente, DevKit, Addon Studio, tipos de personalização, add-ons, etc.

    URL inicial do índice: https://developer.sankhya.com.br/docs/conhecendo-o-portal

    Args:
        url: URL no formato https://developer.sankhya.com.br/docs/{slug}.

    Returns:
        Texto limpo da página ou mensagem de erro.
    """
    return _acessar_secao(url, DEVELOPER_SECAO_GUIAS)


def acessar_receita(url: str) -> str:
    """
    Acessa uma página de Receitas do portal Sankhya Developer.

    Contém exemplos práticos e prontos para uso (code recipes): consultas JAPE
    com SQL nativo, chamadas de serviços, manipulação de entidades, etc.

    URL inicial do índice: https://developer.sankhya.com.br/recipes

    Args:
        url: URL no formato https://developer.sankhya.com.br/recipes/{slug}.

    Returns:
        Texto limpo da página ou mensagem de erro.
    """
    return _acessar_secao(url, DEVELOPER_SECAO_RECEITAS)


def acessar_referencia_api(url: str) -> str:
    """
    Acessa uma página de Referência de API do portal Sankhya Developer.

    Contém a referência completa das APIs REST: autenticação via API Gateway,
    endpoints por produto (pessoal, fiscal, financeiro, etc.), payloads e FAQ.

    URL inicial do índice: https://developer.sankhya.com.br/reference/guia-integracao

    Args:
        url: URL no formato https://developer.sankhya.com.br/reference/{slug}.

    Returns:
        Texto limpo da página ou mensagem de erro.
    """
    return _acessar_secao(url, DEVELOPER_SECAO_API)


def acessar_pagina(url: str) -> str:
    """
    Acessa qualquer página do portal Sankhya Developer, independente da seção.

    Valida apenas o domínio. Use as funções específicas por seção
    (acessar_guia, acessar_receita, acessar_referencia_api) quando a seção
    já for conhecida.

    Args:
        url: URL de qualquer página do portal Developer.

    Returns:
        Texto limpo da página ou mensagem de erro.
    """
    if erro := _validar_dominio(url):
        return erro

    if not any(p in url for p in HREF_PATTERNS_DEVELOPER):
        secoes = ", ".join(HREF_PATTERNS_DEVELOPER)
        return (
            f"Erro: URL fora das seções permitidas do portal Developer. "
            f"Seções válidas: {secoes}."
        )

    return extrair_conteudo_limpo(url)


if __name__ == "__main__":
    url_alvo = sys.argv[1] if len(sys.argv) > 1 else DEVELOPER_URL_INDICE_GUIAS
    print(f"A ler o conteúdo de: {url_alvo}\n" + "-" * 50)
    resultado = acessar_pagina(url_alvo)
    if len(resultado) > PREVIEW_LIMIT:
        print(resultado[:PREVIEW_LIMIT] + "\n\n[... CONTEÚDO TRUNCADO PARA VISUALIZAÇÃO ...]")
    else:
        print(resultado)