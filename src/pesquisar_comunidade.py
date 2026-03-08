import requests
from pathlib import Path
from src.bettermode import check_graphql_errors
from src.get_env import get_env

graphql_query = (
    Path(__file__).parent 
    / "pesquisar_comunidade.gql"
).read_text(encoding="utf-8")

def pesquisar_comunidade(
    bearer_token: str,
    query: str,
    limit: int,
    after: str|None = None,
) -> dict:
    url = "https://api.bettermode.com/"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Referer": "https://community.sankhya.com.br/",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }

    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    variables = {
        "query": query,
        "limit": limit,
    }

    if after:
        variables["after"] = after

    payload = {
        "query": graphql_query,
        "variables": variables,
        "operationName": "searchPosts",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    check_graphql_errors(data)

    return data


if __name__ == "__main__":
    import json
    import argparse

    bearer_token = get_env("BEARER_TOKEN")

    parser = argparse.ArgumentParser(description="Busca posts na Comunidade Sankhya.")
    parser.add_argument("--query",  required=True,       help="Termo de busca")
    parser.add_argument("--limit",  required=True, type=int, help="Número de resultados")
    parser.add_argument("--after",  default=None,        help="Cursor de paginação (opcional)")
    args = parser.parse_args()

    resultado = pesquisar_comunidade(
        bearer_token=bearer_token,
        query=args.query,
        limit=args.limit,
        after=args.after,
    )
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    page_info = resultado["data"]["searchPosts"]["pageInfo"]
    if page_info["hasNextPage"]:
        proxima_pagina = pesquisar_comunidade(
            bearer_token=bearer_token,
            query=args.query,
            limit=args.limit,
            after=page_info["endCursor"]
        )
        print(json.dumps(proxima_pagina, indent=2, ensure_ascii=False))