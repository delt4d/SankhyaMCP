"""
Configurações centralizadas do projeto.
Valores de timeout podem ser sobrescritos via variáveis de ambiente.
"""
import os

# ---------------------------------------------------------------------------
# Comunidade Sankhya
# ---------------------------------------------------------------------------
BASE_URL_COMUNIDADE = "https://community.sankhya.com.br"
SEARCH_URL_COMUNIDADE = BASE_URL_COMUNIDADE + "/search?query={query}&type=posts&expanded=posts"
DOMINIO_COMUNIDADE = "community.sankhya.com.br"
HREF_PATTERNS_COMUNIDADE = ("/post/", "/question/")

# ---------------------------------------------------------------------------
# Central de Ajuda Sankhya
# ---------------------------------------------------------------------------
BASE_URL_AJUDA = "https://ajuda.sankhya.com.br"
SEARCH_URL_AJUDA = BASE_URL_AJUDA + "/hc/pt-br/search?utf8=%E2%9C%93&query={query}&filter_by=knowledge_base"
DOMINIO_AJUDA = "ajuda.sankhya.com.br"
HREF_PATTERNS_AJUDA = ("/hc/pt-br/articles/",)

# ---------------------------------------------------------------------------
# Sankhya Developer
# ---------------------------------------------------------------------------
BASE_URL_DEVELOPER = "https://developer.sankhya.com.br"
DOMINIO_DEVELOPER = "developer.sankhya.com.br"
HREF_PATTERNS_DEVELOPER = ("/docs/", "/recipes/", "/reference/")

# Padrão de href e URL de índice de cada seção do portal Developer
DEVELOPER_SECAO_GUIAS = "/docs/"
DEVELOPER_SECAO_RECEITAS = "/recipes/"
DEVELOPER_SECAO_API = "/reference/"

DEVELOPER_URL_INDICE_GUIAS = BASE_URL_DEVELOPER + "/docs/conhecendo-o-portal"
DEVELOPER_URL_INDICE_RECEITAS = BASE_URL_DEVELOPER + "/recipes"
DEVELOPER_URL_INDICE_API = BASE_URL_DEVELOPER + "/reference/guia-integracao"

# ---------------------------------------------------------------------------
# Selenium
# ---------------------------------------------------------------------------
JS_WAIT_SECONDS: int = int(os.getenv("SANKHYA_JS_WAIT", "7"))

# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
REQUEST_TIMEOUT: int = int(os.getenv("SANKHYA_REQUEST_TIMEOUT", "10"))
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ---------------------------------------------------------------------------
# Parser HTML
# ---------------------------------------------------------------------------
TAGS_REMOVIDAS = (
    "header", "footer", "nav", "script", "style",
    "aside", "noscript", "meta", "svg", "button",
)
SELETORES_CONTEUDO = ("main", "article")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
PREVIEW_LIMIT: int = 1500