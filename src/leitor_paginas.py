"""
Leitura e limpeza de conteúdo de posts da Comunidade Sankhya.

Execução direta (validação manual):
    python -m src.leitor_paginas "https://community.sankhya.com.br/wms/post/slug"
"""
import sys

import requests
from bs4 import BeautifulSoup, Tag

from src.config import HTTP_HEADERS, PREVIEW_LIMIT, REQUEST_TIMEOUT, SELETORES_CONTEUDO, TAGS_REMOVIDAS


def _remover_ruido(soup: BeautifulSoup) -> None:
    """Remove in-place todas as tags de layout/ruído."""
    for tag in TAGS_REMOVIDAS:
        for elemento in soup.find_all(tag):
            elemento.decompose()


def _encontrar_conteudo(soup: BeautifulSoup) -> Tag | None:
    """Retorna o elemento de conteúdo principal ou None."""
    for seletor in SELETORES_CONTEUDO:
        if (elemento := soup.find(seletor)):
            return elemento  # type: ignore[return-value]
    return soup.find("div", role="main") or soup.find("body")  # type: ignore[return-value]


def extrair_conteudo_limpo(url: str) -> str:
    """
    Acede a uma URL da Comunidade Sankhya e retorna apenas o conteúdo
    textual relevante, sem menus, cabeçalhos ou rodapés.

    Args:
        url: URL de um post em community.sankhya.com.br.

    Returns:
        Texto limpo do post ou mensagem de erro.
    """
    try:
        response = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        _remover_ruido(soup)

        conteudo = _encontrar_conteudo(soup)
        if not conteudo:
            return "Não foi possível identificar o corpo da página."

        return conteudo.get_text(separator="\n", strip=True)

    except requests.exceptions.RequestException as e:
        return f"Erro de conexão ao aceder à página: {e}"
    except Exception as e:
        return f"Erro inesperado ao extrair conteúdo da página: {e}"


if __name__ == "__main__":
    url_alvo = sys.argv[1] if len(sys.argv) > 1 else "https://community.sankhya.com.br/"
    print(f"A ler o conteúdo de: {url_alvo}\n" + "-" * 50)
    resultado = extrair_conteudo_limpo(url_alvo)
    if len(resultado) > PREVIEW_LIMIT:
        print(resultado[:PREVIEW_LIMIT] + "\n\n[... CONTEÚDO TRUNCADO PARA VISUALIZAÇÃO ...]")
    else:
        print(resultado)
