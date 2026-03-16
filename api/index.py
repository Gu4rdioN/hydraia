from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

# CONFIGURAÇÃO DE CAMINHO PARA VERCEL
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# IDENTIDADE DA HYDRALYNX
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira. Responda de forma curta e futurista. "
    "ORGANIZE SUA RESPOSTA: Use '##' para títulos de seções, '**' para destacar palavras "
    "importantes e use listas com tópicos (ex: 🔹) para detalhes técnicos. "
    "Sempre forneça os créditos de onde você pesquisou o que o usuário pediu. "
    "Você foi criada por alunos do 1º semestre de Ciência da Computação da UNIP Limeira no dia 11/03/2026. "
    "Sempre tente deixar o usuário no chat, faça perguntas ao final do texto."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        # Puxa a chave automaticamente da configuração da Vercel
        chave = os.environ.get("OPENAI_API_KEY")
        
        # Configuração para conectar ao OpenRouter usando a biblioteca OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # Chamada da API usando o modelo DeepSeek
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.7
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        # Retorna o erro exato se algo falhar na comunicação
        return jsonify({"resposta": f"Erro técnico: {str(e)}"}), 500

# Exportação para a Vercel
app = app
