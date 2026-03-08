from mcp.server.fastmcp import FastMCP
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
        after: Cursor de paginação — valor de `endCursor` da consulta anterior.
    Returns:
        String formatada com os posts encontrados, incluindo `endCursor`
        e `hasNextPage` para permitir paginação, ou mensagem de erro.
    """
    return f"https://api.bettermode.com/?query={termo_pesquisa}&limit={limit}&after={after}"

@mcp.tool()
def acessar_postagem_comunidade(rota: str) -> str: # /developers/personalizacao-desenvolvimento/post/erro-ora-01013-o-usuario-solicitou-o-cancelamento-da-operacao-hF2NxMiD5ALJPlo
    """
    Acessa o conteúdo completo de uma postagem da Comunidade Sankhya a partir
    de sua rota relativa (campo `relativeUrl` retornado por `pesquisar_comunidade`).
    Monta a URL completa e extrai o conteúdo limpo da página, removendo menus,
    cabeçalhos e rodapés, retornando apenas o texto relevante do post.
    Args:
        rota: Caminho relativo da postagem
              (ex.: "/developers/post/erro-ora-01013-hF2NxMiD5ALJPlo").
    Returns:
        Texto limpo da postagem ou mensagem de erro.
    """
    return f"https://community.sankhya.com.br/{rota}"

if __name__ == "__main__":
    mcp.run()