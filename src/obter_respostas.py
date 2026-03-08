import requests
from pathlib import Path
from bettermode import check_graphql_errors
from get_env import get_env

graphql_query = (
    Path(__file__).parent 
    / "obter_respostas.gql"
).read_text(encoding="utf-8")

def obter_respostas(
    bearer_token: str,
    id_post: str,
    limit: int,
    after: str|None = None
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
        "postId": id_post,
        "limit": limit,
        "reverse": False,
        "orderBy": "publishedAt"
    }

    if after:
        variables["after"] = after

    payload = {
        "query": graphql_query,
        "variables": variables,
        "operationName": "replies",
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
    parser.add_argument("--id",     required=True,           help="Id do POST")
    parser.add_argument("--limit",  required=True, type=int, help="Número de resultados")
    parser.add_argument("--after",  default=None,            help="Cursor de paginação (opcional)")
    args = parser.parse_args()

    resultado = obter_respostas(
        bearer_token=bearer_token,
        id_post=args.id,
        limit=args.limit,
        after=args.after,
    )
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    page_info = resultado["data"]["replies"]["pageInfo"]
    if page_info["hasNextPage"]:
        proxima_pagina = obter_respostas(
            bearer_token=bearer_token,
            id_post=args.id,
            limit=args.limit,
            after=page_info["endCursor"]
        )
        print(json.dumps(proxima_pagina, indent=2, ensure_ascii=False))