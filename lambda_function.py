import requests
from bs4 import BeautifulSoup
import json
import logging


SEARCH_URL = "https://www.periodicos.capes.gov.br/index.php/acervo/buscador/component/users/"
BASE_URL = "https://www.periodicos.capes.gov.br"
OPENAI_API_KEY = "CHAVE AQUI"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Função para extrair artigos e links do HTML principal (HTML 1)
def extract_articles_from_search_page(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = soup.find_all("div", class_="result-busca")
    artigos = []

    for resultado in resultados:
        titulo_tag = resultado.find("a", class_="titulo-busca")
        if titulo_tag:
            titulo = titulo_tag.text.strip()
            link = BASE_URL + titulo_tag['href']  # Adicionar BASE_URL ao link
            artigos.append({"titulo": titulo, "link": link})
    
    return artigos

# Função para extrair detalhes do HTML acessado a partir do link (HTML 2)
def extract_details_from_article_page(html):
    soup = BeautifulSoup(html, "html.parser")
    
    detalhes = {
        "publicacao": soup.find("strong", id="type-publicacao").text.strip() if soup.find("strong", id="type-publicacao") else "Não informado",
        "titulo_completo": soup.find("h5", id="item-titulo").text.strip() if soup.find("h5", id="item-titulo") else "Sem título",
        "ano": soup.find("strong", id="item-ano").text.strip() if soup.find("strong", id="item-ano") else "Não informado",
        "instituicao": soup.find("strong", id="item-instituicao").text.strip() if soup.find("strong", id="item-instituicao") else "Não informado",
        "volume": soup.find("strong", id="item-volume").text.strip() if soup.find("strong", id="item-volume") else "Não informado",
        "issue": soup.find("strong", id="item-issue").text.strip() if soup.find("strong", id="item-issue") else "Não informado",
        "linguagem": soup.find("strong", id="item-language").text.strip() if soup.find("strong", id="item-language") else "Não informado",
        "doi": soup.find("p", class_="small text-muted mb-3 block").text.strip() if soup.find("p", class_="small text-muted mb-3 block") else "Não informado",
        "issn": soup.find("p", class_="text-muted mb-3 block").text.strip() if soup.find("p", class_="text-muted mb-3 block") else "Não informado",
        "autores": soup.find("p", id="item-autores").text.strip() if soup.find("p", id="item-autores") else "Não informado",
        "topicos": soup.find("p", id="item-autores").text.strip() if soup.find("p", id="item-autores") else "Não informado",
        "resumo": soup.find("p", id="item-resumo").text.strip() if soup.find("p", id="item-resumo") else "Não informado",
        "acessar_link": soup.find("a", id="item-acessar")['href'] if soup.find("a", id="item-acessar") else "Não disponível"
    }
    
    return detalhes

# Função para enviar o resumo para a API do OpenAI e obter o resumo simplificado
def summarize_with_openai(resumo):
    prompt = f"Resuma esse texto desse artigo para facilitar um leigo entender o seu conteúdo e facilite o entendimento.\n\nResumo: {resumo}"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",  # Trocar o modelo aqui
        "messages": [
            {"role": "system", "content": "Você é um assistente que resume artigos para facilitar o entendimento."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()


# Função para enviar o resumo para a API do OpenAI e obter o resumo simplificado
def summarize_with_openai_for_kids(resumo):
    prompt = f"Resuma esse texto desse artigo para facilitar uma criança entender o seu conteúdo e facilite o entendimento de forma ludica, mas sem fuga de tema.\n\nResumo: {resumo}"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",  # Trocar o modelo aqui
        "messages": [
            {"role": "system", "content": "Você é um assistente que resume artigos para facilitar o entendimento para crianças."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()


# Função Lambda Handler
def lambda_handler(event, context):
    logging.info(f"Evento recebido: {json.dumps(event, indent=4)}")
    print(event)
    query = event.get('queryStringParameters', {}).get('q', None)
    if not query:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "O parâmetro 'q' é obrigatório."}, ensure_ascii=False)
        }
    
    try:
        # Realizar a busca e processamento
        artigos = fetch_and_process_articles(query)
        return {
            "statusCode": 200,
            "body": json.dumps(artigos, ensure_ascii=False)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}, ensure_ascii=False)
        }

# Função para realizar a requisição inicial e acessar os links detalhados
def fetch_and_process_articles(query):
    # Fazer a requisição para o site com o termo de busca
    response = requests.get(SEARCH_URL, params={"q": query})
    response.raise_for_status()  # Levantar exceção em caso de erro na requisição
    html_content = response.text

    # Extrair artigos e links
    artigos = extract_articles_from_search_page(html_content)

    # Limitar a segunda consulta a apenas 1 artigo para testes
    if artigos:
        artigo = artigos[0]  # Pega apenas o primeiro artigo
        response = requests.get(artigo["link"])
        response.raise_for_status()
        detalhes = extract_details_from_article_page(response.text)
        artigo.update(detalhes)  # Mesclar os detalhes no artigo
        
        # Adicionar o resumo gerado pela API do OpenAI
        if "resumo" in artigo and artigo["resumo"] != "Não informado":
            artigo["resumo_ia"] = summarize_with_openai(artigo["resumo"])
            artigo["resumo_ia_for_kids"] = summarize_with_openai_for_kids(artigo["resumo"])
            
        else:
            artigo["resumo_ia"] = "Não disponível"
            artigo["resumo_ia_for_kids"] = "Não disponível"
            
        return [artigo]  # Retorna apenas o primeiro artigo com detalhes

    return []