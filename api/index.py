from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
    "Fale de forma fluida como um humano. "
    "ORGANIZE SUA RESPOSTA: Use '##' para títulos, '**' para destaque e '🔹' para tópicos. "
    "REGRA CRÍTICA DE CÓDIGO: Nunca utilize marcações de negrito '**' ou títulos '##' dentro de blocos de código (code blocks). "
    "O código deve ser puro para garantir a leitura correta no HTML. "
    "Sempre cite fontes e termine com uma pergunta sobre tecnologia ou futuro."

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
            model="nvidia/nemotron-3-super-120b-a12b:free", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.7
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        return jsonify({"resposta": f"Erro técnico na Hydralynx: {str(e)}"}), 500

app = app
