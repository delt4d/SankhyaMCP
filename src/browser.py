"""
Gerenciamento do WebDriver (Microsoft Edge headless).
Isolado para facilitar mock nos testes e futura troca de browser.
"""
import time
from contextlib import contextmanager
from typing import Generator

from selenium import webdriver
from selenium.webdriver.edge.options import Options

from src.config import JS_WAIT_SECONDS


def _criar_opcoes() -> Options:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    return options


@contextmanager
def edge_driver() -> Generator[webdriver.Edge, None, None]:
    """
    Context manager que cria e fecha o Edge WebDriver com segurança.

    Uso:
        with edge_driver() as driver:
            driver.get(url)
            html = driver.page_source
    """
    driver = webdriver.Edge(options=_criar_opcoes())
    try:
        yield driver
    finally:
        driver.quit()


def buscar_html(url: str) -> str:
    """
    Abre a URL no Edge headless, aguarda a renderização via JS e retorna o HTML.
    Lança exceção em caso de falha — o chamador decide como tratar.
    """
    with edge_driver() as driver:
        driver.get(url)
        time.sleep(JS_WAIT_SECONDS)
        return driver.page_source
