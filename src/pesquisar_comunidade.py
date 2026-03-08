import requests
import argparse
from pathlib import Path
from src.get_env import get_env

graphql_query = (
    Path(__file__).parent 
    / "pesquisar_comunidade.gql"
).read_text(encoding="utf-8")

class BettermodeAuthError(Exception):
    """Token inválido, expirado ou sem permissão (código 102 / status 403)."""
    pass


class BettermodeGraphQLError(Exception):
    """Erro genérico retornado pela API GraphQL."""
    def __init__(self, errors: list):
        self.errors = errors
        messages = " | ".join(e.get("message", "Erro desconhecido") for e in errors)
        super().__init__(f"Erro GraphQL: {messages}")


def _check_graphql_errors(data: dict) -> None:
    """Lança exceção se a resposta contiver erros GraphQL."""
    errors = data.get("errors")
    if not errors:
        return

    for error in errors:
        status = error.get("status") or error.get("extensions", {}).get("status")
        code = error.get("code") or error.get("extensions", {}).get("code")

        if status == 403 or str(code) == "102":
            raise BettermodeAuthError(
                f"Acesso negado (status={status}, code={code}). "
                "Verifique se o BEARER_TOKEN é válido e não expirou."
            )

    raise BettermodeGraphQLError(errors)

def pesquisar_comunidade(
    bearer_token: str,
    query: str,
    limit: int,
    after: str = None,
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
    _check_graphql_errors(data)

    return data


if __name__ == "__main__":
    import json

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