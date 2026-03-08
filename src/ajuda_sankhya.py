"""
Pesquisa de artigos na Central de Ajuda Sankhya (Zendesk).

A página de resultados é HTML estático — sem necessidade de Selenium.

Execução direta (validação manual):
    python -m src.ajuda_sankhya "nota fiscal"
"""
import sys
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from src.config import (
    BASE_URL_AJUDA,
    DOMINIO_AJUDA,
    HREF_PATTERNS_AJUDA,
    HTTP_HEADERS,
    PREVIEW_LIMIT,
    REQUEST_TIMEOUT,
    SEARCH_URL_AJUDA,
)


def _montar_url(query: str) -> str:
    return SEARCH_URL_AJUDA.format(query=quote_plus(query))


def _extrair_links(html: str) -> list[str]:
    """Retorna lista de strings formatadas 'Título + URL' a partir do HTML."""
    soup = BeautifulSoup(html, "html.parser")
    vistos: set[str] = set()
    resultados: list[str] = []

    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        texto: str = a_tag.get_text(strip=True)

        if not texto or not any(p in href for p in HREF_PATTERNS_AJUDA):
            continue

        link = f"{BASE_URL_AJUDA}{href}" if href.startswith("/") else href

        entrada = f"- Título: {texto}\n  URL: {link}"
        if entrada not in vistos:
            vistos.add(entrada)
            resultados.append(entrada)

    return resultados


def pesquisar_artigos(query: str) -> str:
    """
    Pesquisa artigos na Central de Ajuda Sankhya e retorna título + URL de cada resultado.

    Args:
        query: Termo de busca (ex.: "nota fiscal").

    Returns:
        String com os artigos encontrados ou mensagem de erro/ausência.
    """
    if not query or not query.strip():
        return "Erro: o termo de pesquisa não pode estar vazio."

    try:
        response = requests.get(
            _montar_url(query),
            headers=HTTP_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        resultados = _extrair_links(response.text)

        if not resultados:
            return "Nenhum artigo encontrado ou a estrutura da página foi alterada."

        return "\n".join(resultados)

    except requests.exceptions.RequestException as e:
        return f"Erro de conexão ao pesquisar na Central de Ajuda: {e}"
    except Exception as e:
        return f"Erro ao pesquisar na Central de Ajuda: {e}"


if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"A pesquisar por '{termo}' na Central de Ajuda...")
    resultado = pesquisar_artigos(termo)
    if len(resultado) > PREVIEW_LIMIT:
        print(resultado[:PREVIEW_LIMIT] + "\n\n[... CONTEÚDO TRUNCADO PARA VISUALIZAÇÃO ...]")
    else:
        print(resultado)
