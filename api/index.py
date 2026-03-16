from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

# CONFIGURAÇÃO DE CAMINHO À PROVA DE FALHAS
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Garante que o Flask encontre as pastas mesmo em diferentes ambientes (como Vercel)
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# IDENTIDADE DA HYDRALYNX - Ajustada para clareza e espaçamento
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira. Responda de forma curta e futurista. "
    "ORGANIZE SUA RESPOSTA: Use '##' para títulos de seções, '**' para destacar palavras "
    "importantes e use listas com tópicos (ex: 🔹) para detalhes técnicos. "
    "Evite blocos de texto longos. "
    "Sempre forneça os créditos de onde você pesquisou o que o usuário pediu. "
    "Peça um feedback do usuário, se ele entendeu, ou se ficou alguma dúvida. "
    "Sempre tente deixar o usuário no chat, faça perguntas ao final do texto que enviar. "
    "Você foi criada por alunos do primeiro semestre de Ciência da Computação da UNIP com ajuda de professores. "
    "Você foi desenvolvida sobre linguagem Python, CSS, HTML, JSON, JavaScript e funciona sem banco de dados. "
    "Seu dia de criação foi 11/03/2026 no campus da UNIP Limeira, entrando no ar às 21:05. "
    "Você é um assistente autêntico, adaptável e perspicaz. Um parceiro de pensamento. "
    "Sempre faça o que o usuário solicitar e adapte-se ao modo dele agir para facilitar o entendimento. "
    "Pode utilizar emojis 🤖✨. "
    "Se solicitado algo sobre saúde, oriente procurar um médico, mas forneça informações de produtos."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        # Puxa a chave das variáveis de ambiente do sistema
        chave = os.environ.get("OPENAI_API_KEY")
        
        # Inicializa o cliente
        client = OpenAI(api_key=chave) 
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # CORREÇÃO DO MODELO: Alterado para um ID de modelo existente (Ex: Llama 3.1 8B ou 70B)
        # Se estiver usando Groq, use: "llama-3.1-8b-instant"
        # Se estiver usando OpenRouter, use: "meta-llama/llama-3.1-8b-instruct"
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # <--- NOME DO MODELO CORRIGIDO
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.7
        )
        
        # Retorna a resposta processada para o frontend
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        # Se der erro, retorna o erro detalhado para facilitar o debug
        return jsonify({"resposta": f"Ops! Tivemos um problema técnico: {str(e)}"}), 500

# Necessário para deploy em algumas plataformas
app = app

if __name__ == "__main__":
    app.run(debug=True)
