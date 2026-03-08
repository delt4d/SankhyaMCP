"""
Testes unitários para src.ajuda_sankhya.
Execute com: pytest tests/test_ajuda_sankhya.py -v
"""
from unittest.mock import MagicMock, patch

import requests

from src.ajuda_sankhya import _extrair_links, pesquisar_artigos

# ---------------------------------------------------------------------------
# Fixtures de HTML
# ---------------------------------------------------------------------------

HTML_COM_RESULTADOS = """
<html><body>
  <a href="/hc/pt-br/articles/123456-como-emitir-nota-fiscal">Como Emitir Nota Fiscal</a>
  <a href="/hc/pt-br/articles/789012-configurar-tributacao">Configurar Tributação</a>
  <a href="/sobre">Sobre nós</a>
  <a href="/hc/pt-br/categories/financeiro">Financeiro</a>
</body></html>
"""

HTML_COM_DUPLICATAS = """
<html><body>
  <a href="/hc/pt-br/articles/111-artigo-duplicado">Artigo Duplicado</a>
  <a href="/hc/pt-br/articles/111-artigo-duplicado">Artigo Duplicado</a>
</body></html>
"""

HTML_VAZIO = "<html><body><p>Sem resultados</p></body></html>"


def _mock_response(html: str, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.text = html
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{status_code}")
    return resp


# ---------------------------------------------------------------------------
# Testes de _extrair_links (unidade pura)
# ---------------------------------------------------------------------------


def test_extrai_links_de_artigos():
    links = _extrair_links(HTML_COM_RESULTADOS)
    assert any("Como Emitir Nota Fiscal" in l for l in links)
    assert any("Configurar Tributação" in l for l in links)


def test_ignora_links_sem_padrao_articles():
    links = _extrair_links(HTML_COM_RESULTADOS)
    assert not any("/sobre" in l for l in links)
    assert not any("/categories/" in l for l in links)


def test_remove_duplicatas():
    links = _extrair_links(HTML_COM_DUPLICATAS)
    assert len(links) == 1


def test_retorna_lista_vazia_para_html_sem_artigos():
    links = _extrair_links(HTML_VAZIO)
    assert links == []


def test_url_contem_dominio_ajuda():
    links = _extrair_links(HTML_COM_RESULTADOS)
    for link in links:
        assert "ajuda.sankhya.com.br" in link


# ---------------------------------------------------------------------------
# Testes de pesquisar_artigos (mocka requests.get)
# ---------------------------------------------------------------------------


@patch("src.ajuda_sankhya.requests.get")
def test_retorna_artigos_encontrados(mock_get):
    mock_get.return_value = _mock_response(HTML_COM_RESULTADOS)
    resultado = pesquisar_artigos("nota fiscal")
    assert "Como Emitir Nota Fiscal" in resultado
    assert "ajuda.sankhya.com.br" in resultado


@patch("src.ajuda_sankhya.requests.get")
def test_retorna_mensagem_quando_sem_resultados(mock_get):
    mock_get.return_value = _mock_response(HTML_VAZIO)
    resultado = pesquisar_artigos("xyzinexistente")
    assert "Nenhum artigo encontrado" in resultado


@patch(
    "src.ajuda_sankhya.requests.get",
    side_effect=requests.exceptions.ConnectionError("timeout"),
)
def test_retorna_erro_de_conexao(mock_get):
    resultado = pesquisar_artigos("nota fiscal")
    assert "Erro de conexão" in resultado


@patch(
    "src.ajuda_sankhya.requests.get",
    side_effect=Exception("inesperado"),
)
def test_retorna_erro_em_excecao_generica(mock_get):
    resultado = pesquisar_artigos("nota fiscal")
    assert "Erro ao pesquisar" in resultado


def test_rejeita_query_vazia():
    resultado = pesquisar_artigos("")
    assert "vazio" in resultado.lower()


def test_rejeita_query_apenas_espacos():
    resultado = pesquisar_artigos("   ")
    assert "vazio" in resultado.lower()


@patch("src.ajuda_sankhya.requests.get")
def test_url_montada_com_query_codificada(mock_get):
    mock_get.return_value = _mock_response(HTML_COM_RESULTADOS)
    pesquisar_artigos("nota fiscal")
    chamada_url: str = mock_get.call_args[0][0]
    assert "nota+fiscal" in chamada_url or "nota%20fiscal" in chamada_url


@patch("src.ajuda_sankhya.requests.get")
def test_url_montada_contem_dominio_ajuda(mock_get):
    mock_get.return_value = _mock_response(HTML_COM_RESULTADOS)
    pesquisar_artigos("qualquer")
    chamada_url: str = mock_get.call_args[0][0]
    assert "ajuda.sankhya.com.br" in chamada_url
