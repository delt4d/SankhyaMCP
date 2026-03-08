Aqui está a documentação reestruturada e focada **exclusivamente na Comunidade Sankhya**, integrando o modelo de código `FastMCP` fornecido e as regras de arquitetura.

***

# Documentação do Projeto: MCP Sankhya Community Search Server

## 🎯 Objetivo do Projeto
Desenvolver um servidor MCP (Model Context Protocol) em **Python 3** para permitir que modelos de IA pesquisem e leiam tópicos na **Comunidade Sankhya**. O foco exclusivo desta integração é fornecer à IA acesso a discussões onde desenvolvedores resolvem problemas de implementações técnicas, personalizações e erros no sistema.

## ⚙️ Especificações Técnicas e Arquitetura
*   **Ambiente e Dependências:** O projeto deve ser desenvolvido em Python 3, rodando dentro de um ambiente virtual com um arquivo `requirements.txt` listando todos os pacotes.
*   **Modos de Execução:** O servidor deve suportar a execução tanto via rede (servidor) quanto via I/O direto (stdio).
*   **Arquitetura Modular:** Para viabilizar testes isolados, cada comando da IA deve possuir seu próprio arquivo, permitindo chamadas diretas com a passagem de argumentos. O arquivo principal atua apenas na inicialização do servidor e no registro das ferramentas (tools).

## 💻 Implementação Base (`mcp_server.py`)
Conforme a arquitetura definida, o arquivo principal utiliza o `FastMCP` para gerenciar as rotas e importa as lógicas de pesquisa e limpeza de módulos externos independentes (`comunidade_sankhya.py` e `leitor_paginas.py`):

```python
# mcp_server.py
from mcp.server.fastmcp import FastMCP
from comunidade_sankhya import pesquisar_topicos
from leitor_paginas import extrair_conteudo_limpo

# Inicializa o servidor com o FastMCP
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
    if "community.sankhya.com.br" not in url:
        return "Erro: Esta ferramenta tem permissão apenas para acessar links da Comunidade Sankhya (community.sankhya.com.br)."
    
    return extrair_conteudo_limpo(url)

if __name__ == "__main__":
    mcp.run()
```

## 🧹 Diretrizes de Processamento de Dados (Módulos de Extração)
Para otimizar o contexto da IA, os módulos de extração acionados pelo MCP devem seguir regras estritas de limpeza de HTML:
*   **Módulo de Busca (`comunidade_sankhya.py`):** Nas páginas de resultados, o sistema deve retornar **apenas as informações de redirecionamento**, limitando-se aos nomes dos tópicos encontrados e suas respectivas URLs de acesso.
*   **Módulo de Leitura (`leitor_paginas.py`):** Ao acessar um POST específico, a extração deve trazer todo o conteúdo textual do problema e das respostas, mas é **obrigatório remover elementos desnecessários** da página, como cabeçalhos (headers), menus e rodapés.

## 🔗 Rotas e Endpoints (Comunidade Sankhya)
A interação do MCP se restringirá às seguintes rotas da Comunidade Sankhya:

*   **Página Home:** 
    `https://community.sankhya.com.br/`
*   **Padrão da Página de Resultados (Pesquisa):** 
    `https://community.sankhya.com.br/search?query={TERMO_DE_BUSCA}&type=posts&expanded=posts`
    *(Exemplo prático: Buscar pela palavra "Notas" preencherá o parâmetro `query=Notas`)*.
*   **Padrão da Página do POST (Discussão):** 
    `https://community.sankhya.com.br/wms/post/{SLUG_DO_POST}`
    *(Exemplo prático de acesso: URL terminando em `/notas-relatorio-ajczdGPLbDLnOH0`)*.