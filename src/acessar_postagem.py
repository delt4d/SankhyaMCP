from src.ler_pagina import ler_conteudo_markdown

def acessar_postagem(rota: str) -> str:
    """
    Acessa o conteúdo de uma postagem da Comunidade Sankhya e retorna como Markdown.

    Args:
        rota (str): A rota relativa da postagem (ex.: "/developers/post/erro-ora-01013-hF2NxMiD5ALJPlo").

    Returns:
        str: O conteúdo da postagem convertido para Markdown.
    """
    base_url = "https://community.sankhya.com.br"
    url = base_url + rota
    return ler_conteudo_markdown(url)