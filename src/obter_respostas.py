import requests
from pathlib import Path
from src.bettermode import check_graphql_errors
from src.get_env import get_env

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
    """
    Busca uma página de respostas para um post/reply.
    Para buscar TODAS as respostas com paginação, use buscar_todas_respostas().
    Para buscar a ÁRVORE completa recursiva, use buscar_arvore_completa().
    """
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


def buscar_todas_respostas(
    bearer_token: str,
    id_post: str,
    limit: int = 50
) -> list:
    """
    Busca TODAS as respostas de um item com paginação automática.
    Retorna lista com todos os nodes, pagina automaticamente.
    """
    todas_respostas = []
    cursor = None
    
    while True:
        resposta = obter_respostas(
            bearer_token=bearer_token,
            id_post=id_post,
            limit=limit,
            after=cursor
        )
        
        replies = resposta.get('data', {}).get('replies', {})
        nodes = replies.get('nodes', [])
        page_info = replies.get('pageInfo', {})
        
        todas_respostas.extend(nodes)
        
        if not page_info.get('hasNextPage', False):
            break
        
        cursor = page_info.get('endCursor')
    
    return todas_respostas


def buscar_arvore_completa(
    bearer_token: str,
    id_post: str,
    limit: int = 50,
    nivel: int = 0,
    max_niveis: int = 10,
    _debug: bool = False
) -> dict:
    """
    Busca RECURSIVAMENTE toda a árvore de respostas.
    
    Para cada resposta encontrada, busca suas sub-respostas (replies de replies).
    Continua recursivamente até não haver mais respostas ou atingir max_niveis.
    
    Args:
        bearer_token: Token de autenticação
        id_post: ID do post/reply raiz
        limit: Respostas por página (padrão 50)
        nivel: Nível de profundidade (uso interno)
        max_niveis: Limite máximo de profundidade
        _debug: Se True, imprime debug info
    
    Returns:
        Dict com estrutura: {
            'id': id_post,
            'nodes': [respostas com 'replies' aninhadas],
            'profundidade': nível alcançado,
            'total': count total de comentários
        }
    """
    
    if nivel >= max_niveis:
        if _debug:
            print(f"{'  ' * nivel}⚠️  Limite de profundidade atingido")
        return None
    
    # Buscar todas as respostas deste nível (com paginação automática)
    nodes = buscar_todas_respostas(
        bearer_token=bearer_token,
        id_post=id_post,
        limit=limit
    )
    
    if _debug:
        print(f"{'  ' * nivel}✓ {len(nodes)} respostas encontradas")
    
    total_count = len(nodes)
    
    # Para cada resposta, buscar suas sub-respostas recursivamente
    for i, node in enumerate(nodes, 1):
        node_id = node.get('id')
        
        if _debug:
            print(f"{'  ' * nivel}  [{i}/{len(nodes)}] Buscando replies de: {node_id}")
        
        # RECURSÃO: passa o ID da resposta como novo postId
        sub_arvore = buscar_arvore_completa(
            bearer_token=bearer_token,
            id_post=node_id,
            limit=limit,
            nivel=nivel + 1,
            max_niveis=max_niveis,
            _debug=_debug
        )
        
        if sub_arvore:
            node['replies'] = sub_arvore.get('nodes', [])
            node['profundidade'] = sub_arvore.get('profundidade', 0)
            total_count += sub_arvore.get('total', 0)
        else:
            node['replies'] = []
            node['profundidade'] = 0
    
    return {
        'id': id_post,
        'nodes': nodes,
        'profundidade': nivel,
        'total': total_count
    }

if __name__ == "__main__":
    import json
    import argparse

    bearer_token = get_env("BEARER_TOKEN")

    parser = argparse.ArgumentParser(description="Busca respostas na Comunidade Sankhya.")
    parser.add_argument("--id",       required=True,           help="Id do POST/REPLY")
    parser.add_argument("--limit",    required=True, type=int, help="Número de resultados por página")
    parser.add_argument("--recursivo", action="store_true",    help="Busca TODA a árvore de respostas (recursivo)")
    parser.add_argument("--debug",    action="store_true",     help="Mostra debug info")
    parser.add_argument("--after",    default=None,            help="Cursor de paginação (apenas para busca simples)")
    args = parser.parse_args()

    if args.recursivo:
        print(f"🌳 Buscando árvore completa de: {args.id}")
        print("=" * 80)
        arvore = buscar_arvore_completa(
            bearer_token=bearer_token,
            id_post=args.id,
            limit=args.limit,
            _debug=args.debug
        )
        print("=" * 80)
        print(f"✅ Total de comentários (incluindo replies): {arvore['total']}")
        print(json.dumps(arvore, indent=2, ensure_ascii=False))
    else:
        resultado = buscar_todas_respostas(
            bearer_token=bearer_token,
            id_post=args.id,
            limit=args.limit
        )
        print(json.dumps(resultado, indent=2, ensure_ascii=False))