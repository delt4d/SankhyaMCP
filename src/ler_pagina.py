import os
import requests
from markdownify import markdownify as md

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT: int = int(os.getenv("SANKHYA_REQUEST_TIMEOUT", "10"))

def ler_conteudo(url: str) -> str:
    try:
        response = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.RequestException:
        return ''
    
def ler_conteudo_markdown(url: str) -> str:
    html = ler_conteudo(url)
    conteudo = f"<!-- URL: {url} -->\n\n{md(html, heading_style="ATX", bullets="-")}"
    return conteudo

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Busca posts na Comunidade Sankhya.")
    parser.add_argument("--url",      required=True,  help="URL de busca")
    parser.add_argument("--output",   required=False, help="Arquivo para salvar o conteúdo")
    parser.add_argument("--markdown", action="store_true", default=False, help="Converte o conteúdo para Markdown")
    args = parser.parse_args()

    conteudo = ler_conteudo(args.url)
    
    if args.markdown:
        conteudo = ler_conteudo_markdown(args.url)
    else:
        conteudo = ler_conteudo(args.url)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"Conteúdo salvo em \"{args.output}\"")
    else:
        print(conteudo)