# Documentação do Projeto: MCP Sankhya Community Search Server

## 🎯 Objetivo do Projeto

Desenvolver um servidor MCP (Model Context Protocol) em **Python 3** para permitir que modelos de IA pesquisem e leiam tópicos na **Comunidade Sankhya**. O foco exclusivo desta integração é fornecer à IA acesso a discussões onde desenvolvedores resolvem problemas de implementações técnicas, personalizações e erros no sistema.

---

## ⚙️ Especificações Técnicas e Arquitetura

- **Ambiente e Dependências:** Python 3.10+, ambiente virtual (`.venv`), dependências listadas em `requirements.txt`.
- **Modos de Execução:** Suporte a execução via I/O direto (`stdio`) para integração com IDEs e clientes MCP.
- **Arquitetura Modular:** Cada responsabilidade possui seu próprio módulo, permitindo testes isolados e execução direta via linha de comando. O arquivo principal (`mcp_server.py`) atua apenas na inicialização do servidor e no registro das ferramentas (tools).

---

## 🗂️ Estrutura de Arquivos

```
.
├── mcp_server.py              # Ponto de entrada: registra as tools MCP
├── requirements.txt           # Dependências do projeto
├── .vscode/
│   └── mcp.json               # Configuração stdio para o VS Code
└── src/
    ├── config.py              # Constantes centralizadas (URLs, timeouts, seletores)
    ├── browser.py             # WebDriver Edge headless (Selenium) com context manager
    ├── comunidade_sankhya.py  # Pesquisa de tópicos via Selenium
    └── leitor_paginas.py      # Extração e limpeza de posts via requests + BeautifulSoup
```

---

## 💻 Implementação Base (`mcp_server.py`)

O arquivo principal utiliza o `FastMCP` para gerenciar as rotas e importa as lógicas dos módulos externos:

```python
from mcp.server.fastmcp import FastMCP
from src.comunidade_sankhya import pesquisar_topicos
from src.config import DOMINIO_PERMITIDO
from src.leitor_paginas import extrair_conteudo_limpo

mcp = FastMCP("SankhyaDocsServer")

@mcp.tool()
def buscar_comunidade(termo_pesquisa: str) -> str:
    """
    Pesquisa por dúvidas, problemas ou discussões na Comunidade Sankhya.
    Útil para encontrar links de tópicos sobre problemas que desenvolvedores e usuários estão enfrentando.
    """
    return pesquisar_topicos(termo_pesquisa)

@mcp.tool()
def acessar_artigo_comunidade(url: str) -> str:
    """
    Acessa uma postagem, dúvida ou artigo específico da Comunidade Sankhya através de sua URL.
    Extrai o conteúdo limpo da página para leitura e entendimento do problema/solução.
    """
    if DOMINIO_PERMITIDO not in url:
        return f"Erro: Esta ferramenta tem permissão apenas para acessar links da Comunidade Sankhya ({DOMINIO_PERMITIDO})."
    return extrair_conteudo_limpo(url)

if __name__ == "__main__":
    mcp.run()
```

---

## 🧩 Descrição dos Módulos

### `src/config.py`
Centraliza todas as constantes do projeto. Valores sensíveis (timeouts) podem ser sobrescritos via variáveis de ambiente.

| Constante | Valor padrão | Descrição |
|-----------|-------------|-----------|
| `BASE_URL` | `https://community.sankhya.com.br` | URL base da comunidade |
| `SEARCH_URL` | `{BASE_URL}/search?query={query}&type=posts&expanded=posts` | Template da URL de busca |
| `DOMINIO_PERMITIDO` | `community.sankhya.com.br` | Domínio aceito pela tool de leitura |
| `HREF_PATTERNS` | `("/post/", "/question/")` | Padrões de href que identificam posts válidos |
| `JS_WAIT_SECONDS` | `7` (env: `SANKHYA_JS_WAIT`) | Aguarda renderização JS no Selenium |
| `REQUEST_TIMEOUT` | `10` (env: `SANKHYA_REQUEST_TIMEOUT`) | Timeout HTTP em segundos |
| `TAGS_REMOVIDAS` | `header, footer, nav, script, style, ...` | Tags de layout removidas na limpeza |
| `SELETORES_CONTEUDO` | `("main", "article")` | Seletores de conteúdo principal (em ordem de prioridade) |
| `PREVIEW_LIMIT` | `1500` | Limite de caracteres na saída CLI |

---

### `src/browser.py`
Gerencia o ciclo de vida do Microsoft Edge em modo headless via Selenium. Expõe um context manager (`edge_driver`) que garante `driver.quit()` mesmo em caso de exceção, e a função `buscar_html(url)` que aguarda a renderização JavaScript antes de retornar o HTML.

> **Nota:** A página de resultados de busca da Comunidade Sankhya é renderizada via JavaScript, por isso o Selenium é necessário neste módulo.

---

### `src/comunidade_sankhya.py`
Responsável pela pesquisa de tópicos. Constrói a URL de busca com o termo codificado, delega a obtenção do HTML ao `browser.py` e extrai os links de posts válidos via BeautifulSoup.

**Execução direta:**
```bash
python -m src.comunidade_sankhya "nota fiscal"
```

**Saída esperada:**
```
- Título: Como usar Notas Fiscais no Sankhya
  URL: https://community.sankhya.com.br/wms/post/como-usar-notas-fiscais-abc123
```

---

### `src/leitor_paginas.py`
Responsável pela leitura e limpeza de posts individuais. Usa `requests` (HTTP direto, sem Selenium) para buscar o HTML, remove as tags de ruído definidas em `TAGS_REMOVIDAS` e extrai o conteúdo principal usando os seletores em `SELETORES_CONTEUDO` (prioridade: `main` → `article` → `div[role=main]` → `body`).

**Execução direta:**
```bash
python -m src.leitor_paginas "https://community.sankhya.com.br/wms/post/slug"
```

---

## 🧹 Diretrizes de Processamento de Dados

### Módulo de Busca (`comunidade_sankhya.py`)
Nas páginas de resultados, retornar **apenas título e URL** dos tópicos encontrados — sem HTML, sem metadados adicionais.

### Módulo de Leitura (`leitor_paginas.py`)
Ao acessar um post, extrair todo o conteúdo textual relevante (problema + respostas), mas **remover obrigatoriamente**: `header`, `footer`, `nav`, `script`, `style`, `aside`, `noscript`, `meta`, `svg`, `button`.

---

## 🔗 Rotas e Endpoints

| Descrição | URL |
|-----------|-----|
| Home | `https://community.sankhya.com.br/` |
| Pesquisa | `https://community.sankhya.com.br/search?query={TERMO}&type=posts&expanded=posts` |
| Post | `https://community.sankhya.com.br/wms/post/{SLUG}` |

**Exemplo prático:**
- Buscar "Notas" → `query=Notas`
- Acessar post → `.../wms/post/notas-relatorio-ajczdGPLbDLnOH0`

---

## 🧪 Testes

Os testes utilizam `unittest.mock` para isolar o Selenium (`buscar_html`) e as chamadas HTTP (`requests.get`), garantindo execução sem dependências externas.

```bash
# Todos os testes
pytest tests/ -v

# Por módulo
pytest tests/test_browser.py -v
pytest tests/test_comunidade_sankhya.py -v
pytest tests/test_leitor_paginas.py -v
```

### Cobertura dos testes

| Módulo | O que é testado |
|--------|----------------|
| `test_browser.py` | Retorno do `page_source`, fechamento do driver (sucesso e falha), propagação de exceções |
| `test_comunidade_sankhya.py` | Extração de links, deduplicação, query vazia, encoding da URL, mock de `buscar_html` |
| `test_leitor_paginas.py` | Remoção de tags de ruído, fallback de seletores, mock de `requests.get`, erros de conexão |

---

## 🖥️ Integração com VS Code

O arquivo `.vscode/mcp.json` configura o servidor no modo `stdio`:

```json
{
  "servers": {
    "sankhya": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/mcp_server.py"]
    }
  }
}
```

> **Linux/macOS:** substituir `Scripts/python.exe` por `bin/python`.