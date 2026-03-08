"""
Ponto de entrada do servidor MCP Sankhya.
Registra as tools e delega toda a lógica aos módulos em src/.
"""
from mcp.server.fastmcp import FastMCP

from src.ajuda_sankhya import pesquisar_artigos
from src.comunidade_sankhya import pesquisar_topicos
from src.config import DOMINIO_AJUDA, DOMINIO_COMUNIDADE, DOMINIO_DEVELOPER
from src.developer_sankhya import (
    acessar_guia as acessar_guia_developer,
    acessar_pagina as acessar_pagina_developer,
    acessar_receita as acessar_receita_developer,
    acessar_referencia_api as acessar_referencia_developer,
)
from src.leitor_paginas import extrair_conteudo_limpo

mcp = FastMCP("SankhyaDocsServer")


# ---------------------------------------------------------------------------
# Comunidade Sankhya
# ---------------------------------------------------------------------------


@mcp.tool()
def buscar_comunidade(termo_pesquisa: str) -> str:
    """
    Pesquisa por dúvidas, problemas ou discussões na Comunidade Sankhya.
    Útil para encontrar links de tópicos sobre problemas que desenvolvedores
    e usuários estão enfrentando.
    """
    return pesquisar_topicos(termo_pesquisa)


@mcp.tool()
def acessar_artigo_comunidade(url: str) -> str:
    """
    Acessa uma postagem, dúvida ou artigo específico da Comunidade Sankhya
    através de sua URL. Extrai o conteúdo limpo da página para leitura e
    entendimento do problema/solução.
    """
    if DOMINIO_COMUNIDADE not in url:
        return (
            f"Erro: esta ferramenta tem permissão apenas para acessar links "
            f"da Comunidade Sankhya ({DOMINIO_COMUNIDADE})."
        )
    return extrair_conteudo_limpo(url)


# ---------------------------------------------------------------------------
# Central de Ajuda Sankhya
# ---------------------------------------------------------------------------


@mcp.tool()
def buscar_ajuda_sankhya(termo_pesquisa: str) -> str:
    """
    Pesquisa artigos na Central de Ajuda Sankhya (documentação oficial do ERP).
    Útil para perguntas sobre uso do sistema, configurações e funcionalidades.
    Retorna título e URL dos artigos encontrados.
    """
    return pesquisar_artigos(termo_pesquisa)


@mcp.tool()
def acessar_artigo_ajuda(url: str) -> str:
    """
    Acessa um artigo específico da Central de Ajuda Sankhya através de sua URL.
    Extrai o conteúdo limpo do artigo para leitura da documentação oficial.
    """
    if DOMINIO_AJUDA not in url:
        return (
            f"Erro: esta ferramenta tem permissão apenas para acessar links "
            f"da Central de Ajuda Sankhya ({DOMINIO_AJUDA})."
        )
    return extrair_conteudo_limpo(url)


# ---------------------------------------------------------------------------
# Sankhya Developer
# ---------------------------------------------------------------------------


@mcp.tool()
def buscar_guia_developer(url: str) -> str:
    """
    Acessa uma página de Guias do portal Sankhya Developer.

    Contém documentação técnica estruturada para desenvolvedores: visão geral
    do portal, configuração de ambiente, DevKit, Addon Studio, criação de
    add-ons, tipos de personalização (telas, botões, ações agendadas,
    dashboards, relatórios, EDIs), menus personalizados e gestão de objetos.

    Use a URL do índice para descobrir os guias disponíveis:
        https://developer.sankhya.com.br/docs/conhecendo-o-portal

    Formato das URLs: https://developer.sankhya.com.br/docs/{slug}
    """
    return acessar_guia_developer(url)


@mcp.tool()
def buscar_receita_developer(url: str) -> str:
    """
    Acessa uma página de Receitas do portal Sankhya Developer.

    Contém exemplos práticos prontos para uso (code recipes): consultas JAPE
    com SQL nativo, chamadas de serviços, manipulação de entidades e outros
    padrões de implementação recorrentes na plataforma Sankhya.

    Use a URL do índice para descobrir as receitas disponíveis:
        https://developer.sankhya.com.br/recipes

    Formato das URLs: https://developer.sankhya.com.br/recipes/{slug}
    """
    return acessar_receita_developer(url)


@mcp.tool()
def buscar_referencia_api_developer(url: str) -> str:
    """
    Acessa uma página de Referência de API do portal Sankhya Developer.

    Contém a referência completa das APIs REST do Sankhya Om: autenticação
    via API Gateway, endpoints organizados por produto (pessoal, fiscal,
    financeiro, etc.), parâmetros, exemplos de payload e respostas, e FAQ
    sobre integração.

    Use a URL do índice para descobrir os endpoints disponíveis:
        https://developer.sankhya.com.br/reference/guia-integracao

    Formato das URLs: https://developer.sankhya.com.br/reference/{slug}
    """
    return acessar_referencia_developer(url)


@mcp.tool()
def acessar_pagina_developer_sankhya(url: str) -> str:
    """
    Acessa qualquer página do portal Sankhya Developer quando a seção não é
    conhecida previamente. Prefira as ferramentas específicas por seção
    (buscar_guia_developer, buscar_receita_developer,
    buscar_referencia_api_developer) sempre que a seção for conhecida.

    Seções válidas:
      - Guias:    https://developer.sankhya.com.br/docs/{slug}
      - Receitas: https://developer.sankhya.com.br/recipes/{slug}
      - API Ref:  https://developer.sankhya.com.br/reference/{slug}
    """
    return acessar_pagina_developer(url)


if __name__ == "__main__":
    mcp.run()