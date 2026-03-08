# leitor_paginas.py
import sys
import requests
from bs4 import BeautifulSoup

def extrair_conteudo_limpo(url: str) -> str:
    """
    Acede a uma URL e extrai apenas o conteúdo principal, 
    removendo elementos de navegação, cabeçalhos e scripts.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tags_lixo = ['header', 'footer', 'nav', 'script', 'style', 'aside', 'noscript', 'meta', 'svg', 'button']
        for tag in tags_lixo:
            for elemento in soup.find_all(tag):
                elemento.decompose()
                
        conteudo_principal = soup.find('main') or soup.find('article') or soup.find('div', role='main') or soup.find('body')
        
        if not conteudo_principal:
            return "Não foi possível identificar o corpo da página."
            
        texto_limpo = conteudo_principal.get_text(separator='\n', strip=True)
        return texto_limpo
        
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão ao aceder à página: {str(e)}"
    except Exception as e:
        return f"Erro inesperado ao extrair conteúdo da página: {str(e)}"

if __name__ == "__main__":
    url_alvo = sys.argv[1] if len(sys.argv) > 1 else "https://developer.sankhya.com.br/reference"
    print(f"A ler o conteúdo de: {url_alvo}\n" + "-"*50)
    resultado = extrair_conteudo_limpo(url_alvo)
    if len(resultado) > 1500:
        print(resultado[:1500] + "\n\n[... CONTEÚDO TRUNCADO PARA VISUALIZAÇÃO ...]")
    else:
        print(resultado)