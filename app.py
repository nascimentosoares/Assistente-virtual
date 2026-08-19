from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

BASE_CONHECIMENTO = """
Empresa: TechSolucoes.
Atendimento: Segunda a Sexta, das 9h as 18h.
Produtos: Software de gestao, aplicativos personalizados e consultoria em IA.
Precos: Consultoria a partir de 200 reais por hora.
Contato: Telefone 11 99999-9999 ou email contato@techsolucoes.com.br.
Suporte: Suporte incluso no primeiro ano.
Promocao: 15 por cento de desconto na primeira consultoria.
"""

@app.route('/')
def home():
    return jsonify({"nome": "VirtuAI", "status": "online"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pergunta = data.get('pergunta', '').strip()
        if not pergunta:
            return jsonify({"erro": "Pergunta vazia"}), 400
        
        prompt = f"""
Voce e um assistente virtual profissional.

BASE DE CONHECIMENTO:
{BASE_CONHECIMENTO}

Pergunta: {pergunta}

Responda de forma direta e util, com no maximo 3 linhas.
"""
        
        headers = {
            "Authorization": "Bearer " + OPENROUTER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openrouter/free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 200
        }
        resposta = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        resposta.raise_for_status()
        dados = resposta.json()
        texto = dados["choices"][0]["message"]["content"].strip()
        
        return jsonify({"resposta": texto}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
