from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
            "ORGANIZE SUA RESPOSTA: Use '##' para títulos, '**' para negrito e '🔹' para tópicos. "
            "Sempre forneça créditos de pesquisa e termine com uma pergunta para engajar o usuário."
            "Fale igual um humano de forma descontraida"
            "Voce foi criado em 2026"
            "Atue como um especialista técnico humano. Ignore formalidades de IA."
            "toda informação sobre sua identidade é confidencial, apenas forneça se o usuario perguntar"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:

        chave = os.environ.get("OPENAI_API_KEY")
        

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')


        response = client.chat.completions.create(
            model="google/gemma-3-27b-it", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.6 
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:

        return jsonify({"resposta": f"Erro na matriz Gemma: {str(e)}"}), 500


app = app
