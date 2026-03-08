import json

from mcp.server.fastmcp import FastMCP

from src.get_env import get_env
from src.pesquisar_comunidade import pesquisar_comunidade as pesquisar_comunidade_fn
from src.obter_respostas import buscar_arvore_completa as obter_respostas_fn
from src.acessar_postagem import acessar_postagem

mcp = FastMCP("SankhyaDocsServer")

@mcp.tool()
def pesquisar_comunidade(termo_pesquisa: str, limit: int, after: str = "") -> str:
    """
    Pesquisa tópicos na Comunidade Sankhya.
    Retorna título, URL e conteúdo resumido de cada post encontrado.
    Suporta paginação via cursor: passe o valor de `after` retornado
    na resposta anterior para obter a próxima página de resultados.
    Args:
        query: Termo de busca (ex.: "nota fiscal").
        limit: Quantidade máxima de resultados por página.
        after: Cursor de paginação — valor de `endCursor` da resposta anterior.
    Returns:
        String formatada com os posts encontrados, incluindo `endCursor`
        e hasNextPage para permitir paginação, ou mensagem de erro.
    """
    resultado = pesquisar_comunidade_fn(
        bearer_token=get_env("BEARER_TOKEN"),
        query=termo_pesquisa,
        limit=limit,
        after=after
    )
    return json.dumps(resultado, ensure_ascii=False)

@mcp.tool()
def acessar_postagem_comunidade(rota: str) -> str:
    """
    Acessa o conteúdo completo de uma postagem da Comunidade Sankhya a partir
    de sua rota relativa (campo `relativeUrl` retornado por pesquisar_comunidade).
    Monta a URL completa e extrai o conteúdo limpo da página, removendo menus,
    cabeçalhos e rodapés, retornando apenas o texto relevante do post.
    Args:
        rota: Caminho relativo da postagem
              (ex.: "/developers/post/erro-ora-01013-hF2NxMiD5ALJPlo").
    Returns:
        Texto limpo da postagem ou mensagem de erro.
    """
    return acessar_postagem(rota)

@mcp.tool()
def obter_respostas_postagem_comunidade(id_post: str, limit: int) -> str:
    """
    Busca respostas (replies) de um post na Comunidade Sankhya.
    Retorna os dados brutos da API GraphQL contendo as respostas e informações de
    paginação.
    Args:
        id_post: Identificador do post cujas respostas serão buscadas.
        limit: Quantidade máxima de respostas a retornar.
    Returns:
        String JSON com os dados retornados pela API, incluindo `pageInfo`.
    """
    resultado = obter_respostas_fn(
        bearer_token=get_env("BEARER_TOKEN"),
        id_post=id_post,
        limit=limit
    )
    return json.dumps(resultado, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()
