from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Garante que o Flask localize as pastas no ambiente da Vercel
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# IDENTIDADE DA HYDRALYNX (Mantida e organizada)
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira. Responda de forma curta e futurista. "
    "ORGANIZE SUA RESPOSTA: Use '##' para títulos, '**' para negrito e '🔹' para tópicos. "
    "Você foi criada por alunos do 1º semestre de Ciência da Computação da UNIP Limeira. "
    "Sempre forneça créditos de pesquisa e termine com uma pergunta para engajar o usuário."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        # Puxa a chave configurada no painel da Vercel
        chave = os.environ.get("OPENAI_API_KEY")
        
        # Conexão via OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # ATUALIZAÇÃO: Agora usando o potente Google Gemma 3 27B
        response = client.chat.completions.create(
            model="google/gemma-3-27b-it", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.6 # Um pouco mais baixo para respostas mais precisas
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        # Retorna o erro amigável se a chave ou o modelo falharem
        return jsonify({"resposta": f"Erro na matriz Gemma: {str(e)}"}), 500

# Export para a Vercel
app = app
