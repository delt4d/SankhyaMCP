import os

def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"Variável de ambiente '{key}' não definida.")
    return value