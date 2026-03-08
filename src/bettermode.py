class BettermodeAuthError(Exception):
    """Token inválido, expirado ou sem permissão (código 102 / status 403)."""
    pass

class BettermodeGraphQLError(Exception):
    """Erro genérico retornado pela API GraphQL."""
    def __init__(self, errors: list):
        self.errors = errors
        messages = " | ".join(e.get("message", "Erro desconhecido") for e in errors)
        super().__init__(f"Erro GraphQL: {messages}")

def check_graphql_errors(data: dict) -> None:
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