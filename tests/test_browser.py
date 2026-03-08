"""
Testes unitários para src.browser.
Execute com: pytest tests/test_browser.py -v
"""
from unittest.mock import MagicMock, call, patch

import pytest

from src.browser import buscar_html


def _mock_driver(html: str = "<html/>") -> MagicMock:
    driver = MagicMock()
    driver.page_source = html
    return driver


@patch("src.browser.time.sleep")
@patch("src.browser.webdriver.Edge")
def test_retorna_page_source(mock_edge, mock_sleep):
    mock_edge.return_value = _mock_driver("<html><body>ok</body></html>")
    html = buscar_html("https://example.com")
    assert "<body>ok</body>" in html


@patch("src.browser.time.sleep")
@patch("src.browser.webdriver.Edge")
def test_fecha_driver_apos_sucesso(mock_edge, mock_sleep):
    driver = _mock_driver()
    mock_edge.return_value = driver
    buscar_html("https://example.com")
    driver.quit.assert_called_once()


@patch("src.browser.time.sleep")
@patch("src.browser.webdriver.Edge")
def test_fecha_driver_mesmo_com_excecao(mock_edge, mock_sleep):
    driver = MagicMock()
    driver.get.side_effect = RuntimeError("falha de rede")
    mock_edge.return_value = driver

    with pytest.raises(RuntimeError):
        buscar_html("https://example.com")

    driver.quit.assert_called_once()


@patch("src.browser.webdriver.Edge", side_effect=Exception("Edge não instalado"))
def test_propaga_excecao_do_driver(mock_edge):
    with pytest.raises(Exception, match="Edge não instalado"):
        buscar_html("https://example.com")
