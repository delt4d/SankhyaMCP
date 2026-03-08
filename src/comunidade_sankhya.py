"""
Pesquisa de tópicos na Comunidade Sankhya.

Execução direta (validação manual):
    python -m src.comunidade_sankhya "nota fiscal"
"""
import sys
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from src.browser import buscar_html
from src.config import BASE_URL_COMUNIDADE, HREF_PATTERNS_COMUNIDADE, SEARCH_URL_COMUNIDADE


def _montar_url(query: str) -> str:
    return SEARCH_URL_COMUNIDADE.format(query=quote_plus(query))


def _extrair_links(html: str) -> list[str]:
    """Retorna lista de strings formatadas 'Título + URL' a partir do HTML."""
    soup = BeautifulSoup(html, "html.parser")
    vistos: set[str] = set()
    resultados: list[str] = []

    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"]
        texto: str = a_tag.get_text(strip=True)

        if not texto or not any(p in href for p in HREF_PATTERNS_COMUNIDADE):
            continue

        link = f"{BASE_URL_COMUNIDADE}{href}" if href.startswith("/") else href

        entrada = f"- Título: {texto}\n  URL: {link}"
        if entrada not in vistos:
            vistos.add(entrada)
            resultados.append(entrada)

    return resultados


def pesquisar_topicos(query: str) -> str:
    """
    Pesquisa tópicos na Comunidade Sankhya e retorna título + URL de cada resultado.

    Args:
        query: Termo de busca (ex.: "nota fiscal").

    Returns:
        String com os tópicos encontrados ou mensagem de erro/ausência.
    """
    if not query or not query.strip():
        return "Erro: o termo de pesquisa não pode estar vazio."

    try:
        html = buscar_html(_montar_url(query))
        resultados = _extrair_links(html)

        if not resultados:
            return "Nenhum tópico encontrado ou a estrutura da página foi alterada."

        return "\n".join(resultados)

    except Exception as e:
        return f"Erro ao pesquisar na comunidade: {e}"


if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"A pesquisar por '{termo}' na comunidade (aguarde a renderização do JS)...")
    print(pesquisar_topicos(termo))
