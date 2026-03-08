# comunidade_sankhya.py
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

def pesquisar_topicos(query: str) -> str:
    """
    Realiza a pesquisa na Comunidade Sankhya utilizando o Edge em modo headless para
    aguardar a renderização via JavaScript e retorna os links encontrados.
    """
    url = f"https://community.sankhya.com.br/search?query={query}&type=posts&expanded=posts"
    
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--log-level=3")
    
    try:
        driver = webdriver.Edge(options=edge_options)
        driver.get(url)
        
        time.sleep(7)
        
        html = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        resultados = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto = a_tag.get_text(strip=True)
            
            if texto and ('/post/' in href or '/question/' in href):
                link = f"https://community.sankhya.com.br{href}" if href.startswith('/') else href
                resultados.append(f"- Título: {texto}\n  URL: {link}")
                
        resultados_unicos = list(dict.fromkeys(resultados))
        
        if not resultados_unicos:
            return "Nenhum tópico encontrado ou a estrutura da página foi alterada."
            
        return "\n".join(resultados_unicos)
        
    except Exception as e:
        return f"Erro ao pesquisar na comunidade: {str(e)}"

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"A pesquisar por '{termo}' na comunidade com o Microsoft Edge (aguarde a renderização do JS)...")
    print(pesquisar_topicos(termo))