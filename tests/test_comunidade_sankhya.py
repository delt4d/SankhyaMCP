"""
Testes unitários para src.comunidade_sankhya.
Execute com: pytest tests/test_comunidade_sankhya.py -v
"""
from unittest.mock import patch

from src.comunidade_sankhya import _extrair_links, pesquisar_topicos

# ---------------------------------------------------------------------------
# Fixtures de HTML
# ---------------------------------------------------------------------------

HTML_COM_RESULTADOS = """
<html><body>
  <a href="/wms/post/como-usar-notas-fiscais-abc123">Como usar Notas Fiscais no Sankhya</a>
  <a href="/wms/post/erro-nota-fiscal-xyz789">Erro ao emitir Nota Fiscal</a>
  <a href="/sobre">Sobre nós</a>
</body></html>
"""

HTML_COM_DUPLICATAS = """
<html><body>
  <a href="/wms/post/topico-duplicado-abc">Tópico Duplicado</a>
  <a href="/wms/post/topico-duplicado-abc">Tópico Duplicado</a>
</body></html>
"""

HTML_VAZIO = "<html><body><p>Sem resultados</p></body></html>"

# ---------------------------------------------------------------------------
# Testes de _extrair_links (unidade pura — sem I/O)
# ---------------------------------------------------------------------------

def test_extrai_links_de_posts():
    links = _extrair_links(HTML_COM_RESULTADOS)
    assert any("Como usar Notas Fiscais" in l for l in links)
    assert any("Erro ao emitir Nota Fiscal" in l for l in links)


def test_ignora_links_sem_padrao_post():
    links = _extrair_links(HTML_COM_RESULTADOS)
    assert not any("/sobre" in l for l in links)


def test_remove_duplicatas():
    links = _extrair_links(HTML_COM_DUPLICATAS)
    assert len(links) == 1


def test_retorna_lista_vazia_para_html_sem_posts():
    links = _extrair_links(HTML_VAZIO)
    assert links == []


# ---------------------------------------------------------------------------
# Testes de pesquisar_topicos (mocka buscar_html)
# ---------------------------------------------------------------------------

@patch("src.comunidade_sankhya.buscar_html", return_value=HTML_COM_RESULTADOS)
def test_retorna_topicos_encontrados(mock_buscar):
    resultado = pesquisar_topicos("Nota Fiscal")
    assert "Como usar Notas Fiscais no Sankhya" in resultado
    assert "community.sankhya.com.br" in resultado


@patch("src.comunidade_sankhya.buscar_html", return_value=HTML_VAZIO)
def test_retorna_mensagem_quando_sem_resultados(mock_buscar):
    resultado = pesquisar_topicos("xyzinexistente")
    assert "Nenhum tópico encontrado" in resultado


@patch("src.comunidade_sankhya.buscar_html", side_effect=Exception("Driver não encontrado"))
def test_retorna_erro_em_excecao(mock_buscar):
    resultado = pesquisar_topicos("qualquer coisa")
    assert "Erro ao pesquisar" in resultado


def test_rejeita_query_vazia():
    resultado = pesquisar_topicos("")
    assert "vazio" in resultado.lower()


def test_rejeita_query_apenas_espacos():
    resultado = pesquisar_topicos("   ")
    assert "vazio" in resultado.lower()


@patch("src.comunidade_sankhya.buscar_html", return_value=HTML_COM_RESULTADOS)
def test_url_montada_com_query_codificada(mock_buscar):
    pesquisar_topicos("nota fiscal")
    chamada_url: str = mock_buscar.call_args[0][0]
    assert "nota+fiscal" in chamada_url or "nota%20fiscal" in chamada_url
