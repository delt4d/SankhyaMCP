# Documentação do Projeto: MCP Sankhya Search Server

## 🎯 Objetivo do Projeto

Desenvolver um servidor MCP (Model Context Protocol) em **Python 3** para permitir que modelos de IA pesquisem e leiam conteúdo em **três fontes oficiais Sankhya**:

- **Comunidade Sankhya** (`community.sankhya.com.br`) — fórum onde desenvolvedores e usuários discutem e resolvem problemas de implementação, personalizações e erros no sistema.
- **Central de Ajuda Sankhya** (`ajuda.sankhya.com.br`) — documentação oficial de uso do ERP, com manuais e artigos técnicos publicados pela equipe Sankhya.
- **Sankhya Developer** (`developer.sankhya.com.br`) — portal técnico oficial para desenvolvedores, com guias de desenvolvimento, receitas práticas e documentação completa das APIs.

Ao receber uma pergunta sobre o Sankhya, o modelo deve consultar as fontes mais relevantes para o contexto, usando termos de busca variados para maximizar a chance de encontrar resultados úteis.

---

## ⚙️ Especificações Técnicas e Arquitetura

- **Ambiente e Dependências:** Python 3.10+, ambiente virtual (`.venv`), dependências listadas em `requirements.txt`.
- **Modos de Execução:** Suporte a execução via I/O direto (`stdio`) para integração com IDEs e clientes MCP.
- **Arquitetura Modular:** Cada fonte de dados possui seu próprio módulo de busca, permitindo testes isolados e execução direta via linha de comando. O arquivo principal (`mcp_server.py`) atua apenas na inicialização do servidor e no registro das ferramentas (tools). A lógica de extração de conteúdo de páginas é centralizada em um módulo compartilhado.

---

## 🗂️ Estrutura de Arquivos

```
.
├── mcp_server.py              # Ponto de entrada: registra as tools MCP
├── requirements.txt           # Dependências do projeto
├── .vscode/
│   └── mcp.json               # Configuração stdio para o VS Code
└── src/
    ├── config.py              # Constantes centralizadas (URLs, domínios, seletores, timeouts)
    ├── browser.py             # WebDriver Edge headless (Selenium) com context manager
    ├── comunidade_sankhya.py  # Pesquisa de tópicos na Comunidade Sankhya
    ├── ajuda_sankhya.py       # Pesquisa de artigos na Central de Ajuda Sankhya
    ├── developer_sankhya.py   # Leitura de páginas do Sankhya Developer
    └── leitor_paginas.py      # Extração e limpeza de conteúdo HTML (módulo compartilhado)
```

---

## 🔧 Ferramentas MCP (Tools)

O servidor expõe **seis tools** ao modelo:

| Tool | Fonte | Descrição |
|------|-------|-----------|
| `buscar_comunidade` | Comunidade | Pesquisa tópicos e discussões por termo |
| `acessar_artigo_comunidade` | Comunidade | Lê o conteúdo de um post específico |
| `buscar_ajuda_sankhya` | Central de Ajuda | Pesquisa artigos da documentação oficial do ERP |
| `acessar_artigo_ajuda` | Central de Ajuda | Lê o conteúdo de um artigo específico |
| `buscar_developer_sankhya` | Sankhya Developer | Pesquisa conteúdo no portal Developer |
| `acessar_pagina_developer` | Sankhya Developer | Lê o conteúdo de uma página do portal Developer |

---

## 🧩 Descrição dos Módulos

### `src/config.py`
Centraliza todas as constantes do projeto. Valores de timeout podem ser sobrescritos via variáveis de ambiente.

| Constante | Descrição |
|-----------|-----------|
| `BASE_URL_COMUNIDADE` / `SEARCH_URL_COMUNIDADE` | URLs da Comunidade Sankhya |
| `DOMINIO_COMUNIDADE` / `HREF_PATTERNS_COMUNIDADE` | Domínio e padrões de link válidos da Comunidade |
| `BASE_URL_AJUDA` / `SEARCH_URL_AJUDA` | URLs da Central de Ajuda |
| `DOMINIO_AJUDA` / `HREF_PATTERNS_AJUDA` | Domínio e padrões de link válidos da Ajuda |
| `BASE_URL_DEVELOPER` | URL base do Sankhya Developer |
| `DOMINIO_DEVELOPER` / `HREF_PATTERNS_DEVELOPER` | Domínio e padrões de link válidos do Developer |
| `JS_WAIT_SECONDS` | Tempo de espera para renderização JS — env: `SANKHYA_JS_WAIT` (padrão: `7`) |
| `REQUEST_TIMEOUT` | Timeout HTTP em segundos — env: `SANKHYA_REQUEST_TIMEOUT` (padrão: `10`) |
| `TAGS_REMOVIDAS` | Tags de layout removidas na limpeza de HTML |
| `SELETORES_CONTEUDO` | Seletores de conteúdo principal, em ordem de prioridade |

---

### `src/browser.py`
Gerencia o ciclo de vida do Microsoft Edge em modo headless via Selenium. Garante que o driver seja encerrado corretamente mesmo em caso de exceção.

> A página de resultados da Comunidade Sankhya é renderizada via JavaScript, por isso o Selenium é necessário para esta fonte.

---

### `src/comunidade_sankhya.py`
Pesquisa tópicos na **Comunidade Sankhya**. Usa o Selenium (via `browser.py`) para obter o HTML renderizado e extrai os links de posts válidos. Retorna apenas título e URL de cada resultado encontrado.

Suporta execução direta para validação manual: `python -m src.comunidade_sankhya "termo"`

---

### `src/ajuda_sankhya.py`
Pesquisa artigos na **Central de Ajuda Sankhya** (plataforma Zendesk). A página de resultados é HTML estático — sem necessidade de Selenium. Filtra apenas links correspondentes a artigos válidos. Retorna apenas título e URL de cada resultado.

Suporta execução direta para validação manual: `python -m src.ajuda_sankhya "termo"`

---

### `src/developer_sankhya.py`
Acessa páginas do **Sankhya Developer** e retorna o conteúdo limpo. O portal é baseado em plataforma de documentação com HTML estático — sem necessidade de Selenium. Como não existe rota de busca textual convencional no portal, o acesso é feito diretamente por URL. O modelo deve navegar pelas seções conhecidas descritas na seção de Rotas para localizar o conteúdo relevante.

Suporta execução direta para validação manual: `python -m src.developer_sankhya "https://developer.sankhya.com.br/docs/conhecendo-o-portal"`

---

### `src/leitor_paginas.py`
Módulo compartilhado entre todas as fontes. Acessa qualquer URL via HTTP, remove elementos de layout desnecessários e extrai o conteúdo textual principal. É reutilizado pelas tools de leitura da Comunidade, da Ajuda e do Developer.

---

## 🧹 Diretrizes de Processamento de Dados

**Módulos de busca** (Comunidade, Ajuda): retornar **apenas título e URL** dos resultados — sem HTML, sem metadados adicionais.

**Módulo de leitura** (`leitor_paginas.py`): ao acessar qualquer página, extrair todo o conteúdo textual relevante, removendo obrigatoriamente elementos de layout como cabeçalhos, menus, rodapés, scripts e outros elementos não-textuais.

---

## 🔗 Rotas e Endpoints

### Comunidade Sankhya (`community.sankhya.com.br`)

| Descrição | URL |
|-----------|-----|
| Pesquisa | `https://community.sankhya.com.br/search?query={TERMO}&type=posts&expanded=posts` |
| Post | `https://community.sankhya.com.br/wms/post/{SLUG}` |

---

### Central de Ajuda Sankhya (`ajuda.sankhya.com.br`)

| Descrição | URL |
|-----------|-----|
| Pesquisa | `https://ajuda.sankhya.com.br/hc/pt-br/search?utf8=%E2%9C%93&query={TERMO}&filter_by=knowledge_base` |
| Artigo | `https://ajuda.sankhya.com.br/hc/pt-br/articles/{ID}-{SLUG}` |

---

### Sankhya Developer (`developer.sankhya.com.br`)

O portal não possui uma rota de busca textual convencional — o conteúdo é acessado diretamente por URL. Ele é organizado em três grandes seções, cada uma com padrão de URL distinto:

| Seção | URL inicial | Padrão das páginas | Descrição do conteúdo |
|-------|-------------|--------------------|-----------------------|
| **Guias** | `/docs/conhecendo-o-portal` | `/docs/{slug}` | Documentação técnica estruturada para desenvolvedores: visão geral do portal, configuração de ambiente de desenvolvimento, DevKit e Addon Studio, criação de add-ons, tipos de personalização disponíveis na plataforma (telas adicionais, botões de ação, ações agendadas, eventos programados, dashboards, relatórios, EDIs), menus personalizados e gerenciamento de objetos. |
| **Receitas** | `/recipes` | `/recipes/{slug}` | Exemplos práticos e prontos para uso (code recipes), demonstrando como realizar operações específicas com as APIs e frameworks Sankhya — como consultas JAPE com SQL nativo, chamadas de serviços, manipulação de entidades e outros padrões de implementação recorrentes. |
| **Documentação API** | `/reference/guia-integracao` | `/reference/{slug}` | Referência completa das APIs REST do Sankhya Om: guia de integração e autenticação via API Gateway, endpoints organizados por produto (pessoal, fiscal, financeiro, etc.), parâmetros de requisição, exemplos de payload e respostas, além de FAQ sobre integração. |

> **Nota sobre navegação:** como não há busca nativa, a estratégia recomendada é acessar a URL inicial de cada seção para obter o índice de conteúdo, ou acessar diretamente URLs conhecidas com base no contexto da pergunta.

---

## 🤖 Estratégia de Consulta Multi-Fonte

Ao receber uma pergunta sobre o Sankhya, o modelo deve selecionar as fontes mais adequadas ao contexto:

- **Perguntas sobre uso do ERP, configurações ou funcionalidades** → priorizar a Central de Ajuda e a Comunidade.
- **Perguntas sobre desenvolvimento, integração, APIs ou add-ons** → priorizar o Sankhya Developer e a Comunidade.
- **Perguntas gerais ou ambíguas** → consultar todas as fontes disponíveis.

Em todos os casos, o modelo deve:

1. **Variar os termos de busca** se os primeiros resultados não forem suficientemente relevantes — tentando sinônimos, siglas ou termos mais específicos.
2. **Acessar o conteúdo completo** dos resultados mais promissores, utilizando as tools de leitura correspondentes.
3. **Sintetizar** as informações de todas as fontes consultadas para oferecer uma resposta completa e fundamentada.

---

## 🧪 Testes

Os testes utilizam `unittest.mock` para isolar o Selenium e as chamadas HTTP, garantindo execução sem dependências externas.

```bash
pytest tests/ -v
```

| Módulo de teste | O que é testado |
|-----------------|----------------|
| `test_browser.py` | Ciclo de vida do WebDriver, fechamento em caso de falha, propagação de exceções |
| `test_comunidade_sankhya.py` | Extração de links, deduplicação, query vazia, encoding da URL |
| `test_ajuda_sankhya.py` | Extração de links de artigos, filtro por padrão de href, deduplicação, query vazia |
| `test_developer_sankhya.py` | Extração de conteúdo de páginas do Developer, validação de domínio, erros de conexão |
| `test_leitor_paginas.py` | Remoção de tags de layout, fallback de seletores de conteúdo, erros de conexão |

---

## 🖥️ Integração com VS Code

O arquivo `.vscode/mcp.json` configura o servidor no modo `stdio`. Em Linux/macOS, substituir `Scripts/python.exe` por `bin/python`.