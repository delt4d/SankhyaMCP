"""
Testes unitários para src.leitor_paginas.
Execute com: pytest tests/test_leitor_paginas.py -v
"""
from unittest.mock import MagicMock, patch

import requests

from src.leitor_paginas import _encontrar_conteudo, _remover_ruido, extrair_conteudo_limpo
from bs4 import BeautifulSoup

URL_VALIDA = "https://community.sankhya.com.br/wms/post/exemplo-abc123"

HTML_COMPLETO = """
<html>
  <head><title>Teste</title></head>
  <body>
    <header>Menu principal</header>
    <nav>Links de navegação</nav>
    <main>
      <h1>Título do problema</h1>
      <p>Descrição detalhada do problema técnico.</p>
      <p>Resposta da comunidade: utilize o método X.</p>
    </main>
    <footer>Rodapé</footer>
    <script>console.log("remover")</script>
  </body>
</html>
"""

HTML_SEM_MAIN = "<html><body><p>Conteúdo direto no body.</p></body></html>"

HTML_ARTICLE = """
<html><body>
  <nav>Navegação</nav>
  <article><p>Conteúdo do artigo.</p></article>
</body></html>
"""


def _mock_response(html: str):
    resp = MagicMock()
    resp.text = html
    resp.raise_for_status = MagicMock()
    return resp


# ---------------------------------------------------------------------------
# Testes das helpers (unidade pura)
# ---------------------------------------------------------------------------

def test_remover_ruido_elimina_tags_de_layout():
    soup = BeautifulSoup(HTML_COMPLETO, "html.parser")
    _remover_ruido(soup)
    assert soup.find("header") is None
    assert soup.find("nav") is None
    assert soup.find("footer") is None
    assert soup.find("script") is None


def test_encontrar_conteudo_prefere_main():
    soup = BeautifulSoup(HTML_COMPLETO, "html.parser")
    _remover_ruido(soup)
    conteudo = _encontrar_conteudo(soup)
    assert conteudo is not None
    assert conteudo.name == "main"


def test_encontrar_conteudo_usa_article_como_fallback():
    soup = BeautifulSoup(HTML_ARTICLE, "html.parser")
    _remover_ruido(soup)
    conteudo = _encontrar_conteudo(soup)
    assert conteudo is not None
    assert conteudo.name == "article"


def test_encontrar_conteudo_usa_body_como_ultimo_fallback():
    soup = BeautifulSoup(HTML_SEM_MAIN, "html.parser")
    conteudo = _encontrar_conteudo(soup)
    assert conteudo is not None
    assert conteudo.name == "body"


# ---------------------------------------------------------------------------
# Testes de extrair_conteudo_limpo (mocka requests.get)
# ---------------------------------------------------------------------------

@patch("src.leitor_paginas.requests.get")
def test_remove_elementos_de_navegacao(mock_get):
    mock_get.return_value = _mock_response(HTML_COMPLETO)
    resultado = extrair_conteudo_limpo(URL_VALIDA)

    assert "Título do problema" in resultado
    assert "Resposta da comunidade" in resultado
    assert "Menu principal" not in resultado
    assert "Links de navegação" not in resultado
    assert "Rodapé" not in resultado
    assert "remover" not in resultado


@patch("src.leitor_paginas.requests.get")
def test_fallback_para_body_quando_sem_main(mock_get):
    mock_get.return_value = _mock_response(HTML_SEM_MAIN)
    resultado = extrair_conteudo_limpo(URL_VALIDA)
    assert "Conteúdo direto no body" in resultado


@patch("src.leitor_paginas.requests.get", side_effect=requests.exceptions.ConnectionError("timeout"))
def test_retorna_erro_de_conexao(mock_get):
    resultado = extrair_conteudo_limpo(URL_VALIDA)
    assert "Erro de conexão" in resultado


@patch("src.leitor_paginas.requests.get", side_effect=Exception("inesperado"))
def test_retorna_erro_em_excecao_generica(mock_get):
    resultado = extrair_conteudo_limpo(URL_VALIDA)
    assert "Erro inesperado" in resultado
