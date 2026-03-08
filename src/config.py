"""
Configurações centralizadas do projeto.
Valores podem ser sobrescritos via variáveis de ambiente.
"""
import os

# --- Comunidade Sankhya ---
BASE_URL = "https://community.sankhya.com.br"
SEARCH_URL = BASE_URL + "/search?query={query}&type=posts&expanded=posts"
DOMINIO_PERMITIDO = "community.sankhya.com.br"

# Padrões de href que identificam posts válidos
HREF_PATTERNS = ("/post/", "/question/")

# --- Selenium ---
JS_WAIT_SECONDS: int = int(os.getenv("SANKHYA_JS_WAIT", "7"))

# --- HTTP ---
REQUEST_TIMEOUT: int = int(os.getenv("SANKHYA_REQUEST_TIMEOUT", "10"))
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# --- Parser HTML ---
TAGS_REMOVIDAS = (
    "header", "footer", "nav", "script", "style",
    "aside", "noscript", "meta", "svg", "button",
)
SELETORES_CONTEUDO = ("main", "article")

# --- CLI ---
PREVIEW_LIMIT: int = 1500
