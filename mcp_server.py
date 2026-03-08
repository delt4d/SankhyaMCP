"""
Ponto de entrada do servidor MCP Sankhya.
Registra as tools e delega toda a lógica aos módulos em src/.
"""
from mcp.server.fastmcp import FastMCP

from src.comunidade_sankhya import pesquisar_topicos
from src.config import DOMINIO_PERMITIDO
from src.leitor_paginas import extrair_conteudo_limpo

mcp = FastMCP("SankhyaDocsServer")


@mcp.tool()
def buscar_comunidade(termo_pesquisa: str) -> str:
    """
    Pesquisa por dúvidas, problemas ou discussões na Comunidade Sankhya.
    Útil para encontrar links de tópicos sobre problemas que desenvolvedores e usuários estão enfrentando.
    """
    return pesquisar_topicos(termo_pesquisa)


@mcp.tool()
def acessar_artigo_comunidade(url: str) -> str:
    """
    Acessa uma postagem, dúvida ou artigo específico da Comunidade Sankhya através de sua URL.
    Extrai o conteúdo limpo da página para leitura e entendimento do problema/solução.
    """
    if DOMINIO_PERMITIDO not in url:
        return f"Erro: Esta ferramenta tem permissão apenas para acessar links da Comunidade Sankhya ({DOMINIO_PERMITIDO})."

    return extrair_conteudo_limpo(url)


if __name__ == "__main__":
    mcp.run()
