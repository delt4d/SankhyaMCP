"""
Testes unitários para src.developer_sankhya.
Execute com: pytest tests/test_developer_sankhya.py -v
"""
from unittest.mock import call, patch

import pytest

from src.developer_sankhya import (
    acessar_guia,
    acessar_pagina,
    acessar_receita,
    acessar_referencia_api,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

URL_DOCS = "https://developer.sankhya.com.br/docs/conhecendo-o-portal"
URL_RECIPES = "https://developer.sankhya.com.br/recipes/consulta-jape"
URL_REFERENCE = "https://developer.sankhya.com.br/reference/guia-integracao"
URL_DOMINIO_ERRADO = "https://evil.com/docs/injection"
URL_SECAO_INVALIDA = "https://developer.sankhya.com.br/blog/novidades"

CONTEUDO_LIMPO = "Guia completo de integração com a API Sankhya."
ERRO_CONEXAO = "Erro de conexão ao aceder à página: timeout"
ERRO_EXTRACAO = "Não foi possível identificar o corpo da página."


# ---------------------------------------------------------------------------
# acessar_guia
# ---------------------------------------------------------------------------


def test_guia_rejeita_dominio_externo():
    resultado = acessar_guia(URL_DOMINIO_ERRADO)
    assert "Erro" in resultado
    assert "developer.sankhya.com.br" in resultado


def test_guia_rejeita_secao_errada_recipes():
    resultado = acessar_guia(URL_RECIPES)
    assert "Erro" in resultado
    assert "/docs/" in resultado


def test_guia_rejeita_secao_errada_reference():
    resultado = acessar_guia(URL_REFERENCE)
    assert "Erro" in resultado
    assert "/docs/" in resultado


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=CONTEUDO_LIMPO)
def test_guia_acessa_url_valida(mock_extrair):
    resultado = acessar_guia(URL_DOCS)
    assert resultado == CONTEUDO_LIMPO
    mock_extrair.assert_called_once_with(URL_DOCS)


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=ERRO_CONEXAO)
def test_guia_propaga_erro_de_conexao(mock_extrair):
    resultado = acessar_guia(URL_DOCS)
    assert "Erro de conexão" in resultado


# ---------------------------------------------------------------------------
# acessar_receita
# ---------------------------------------------------------------------------


def test_receita_rejeita_dominio_externo():
    resultado = acessar_receita(URL_DOMINIO_ERRADO)
    assert "Erro" in resultado
    assert "developer.sankhya.com.br" in resultado


def test_receita_rejeita_secao_errada_docs():
    resultado = acessar_receita(URL_DOCS)
    assert "Erro" in resultado
    assert "/recipes/" in resultado


def test_receita_rejeita_secao_errada_reference():
    resultado = acessar_receita(URL_REFERENCE)
    assert "Erro" in resultado
    assert "/recipes/" in resultado


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=CONTEUDO_LIMPO)
def test_receita_acessa_url_valida(mock_extrair):
    resultado = acessar_receita(URL_RECIPES)
    assert resultado == CONTEUDO_LIMPO
    mock_extrair.assert_called_once_with(URL_RECIPES)


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=ERRO_EXTRACAO)
def test_receita_propaga_falha_de_extracao(mock_extrair):
    resultado = acessar_receita(URL_RECIPES)
    assert "Não foi possível" in resultado


# ---------------------------------------------------------------------------
# acessar_referencia_api
# ---------------------------------------------------------------------------


def test_referencia_rejeita_dominio_externo():
    resultado = acessar_referencia_api(URL_DOMINIO_ERRADO)
    assert "Erro" in resultado
    assert "developer.sankhya.com.br" in resultado


def test_referencia_rejeita_secao_errada_docs():
    resultado = acessar_referencia_api(URL_DOCS)
    assert "Erro" in resultado
    assert "/reference/" in resultado


def test_referencia_rejeita_secao_errada_recipes():
    resultado = acessar_referencia_api(URL_RECIPES)
    assert "Erro" in resultado
    assert "/reference/" in resultado


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=CONTEUDO_LIMPO)
def test_referencia_acessa_url_valida(mock_extrair):
    resultado = acessar_referencia_api(URL_REFERENCE)
    assert resultado == CONTEUDO_LIMPO
    mock_extrair.assert_called_once_with(URL_REFERENCE)


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=ERRO_CONEXAO)
def test_referencia_propaga_erro_de_conexao(mock_extrair):
    resultado = acessar_referencia_api(URL_REFERENCE)
    assert "Erro de conexão" in resultado


# ---------------------------------------------------------------------------
# acessar_pagina (genérico — aceita qualquer seção válida)
# ---------------------------------------------------------------------------


def test_pagina_rejeita_dominio_externo():
    resultado = acessar_pagina(URL_DOMINIO_ERRADO)
    assert "Erro" in resultado
    assert "developer.sankhya.com.br" in resultado


def test_pagina_rejeita_url_fora_das_secoes_validas():
    resultado = acessar_pagina(URL_SECAO_INVALIDA)
    assert "Erro" in resultado
    assert "Seções válidas" in resultado


@pytest.mark.parametrize("url", [URL_DOCS, URL_RECIPES, URL_REFERENCE])
@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=CONTEUDO_LIMPO)
def test_pagina_acessa_todas_as_secoes(mock_extrair, url):
    resultado = acessar_pagina(url)
    assert resultado == CONTEUDO_LIMPO
    mock_extrair.assert_called_once_with(url)


@patch("src.developer_sankhya.extrair_conteudo_limpo", return_value=ERRO_EXTRACAO)
def test_pagina_propaga_falha_de_extracao(mock_extrair):
    resultado = acessar_pagina(URL_DOCS)
    assert "Não foi possível" in resultado