import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# 1) Baixar a página
html = requests.get(URL_PAGINA).text

# 2) Ler a tabela de clientes
soup = BeautifulSoup(html, "html.parser")
linhas = soup.select("#clientes tbody tr")

clientes = []

for linha in linhas:
    colunas = linha.find_all("td")

    cliente = {
        "nome":  colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }

    clientes.append(cliente)

# 3) Mostrar o resultado
print(f"Total de clientes extraídos: {len(clientes)}")
for cliente in clientes:
    print(cliente)

# 4) Enviar para o Webhook do n8n via POST (Túnel ngrok)
# Dica: use /webhook-test/clientes quando estiver no modo 'Test step' do n8n
# ou /webhook/clientes se o workflow estiver ativado
N8N_WEBHOOK = "https://owl-reconfirm-grading.ngrok-free.dev/webhook-test/clientes"

try:
    resposta = requests.post(N8N_WEBHOOK, json={"clientes": clientes}, timeout=20)
    print(f"\nStatus Code: {resposta.status_code}")
    import json
    print("Resposta N8N:")
    print(json.dumps(resposta.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"\nErro na requisição ao n8n: {e}")
