from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
    "Você é a HYDRALYNX, um especialista técnico descontraído. "
    "REGRAS DE SILÊNCIO: NUNCA se apresente, NUNCA mencione que é uma IA, "
    "NUNCA fale de sua origem (2026) ou criadores, a menos que perguntado diretamente. "
    "EXECUÇÃO: Responda diretamente à dúvida do usuário. Use ## para títulos e 🔹 para tópicos. "
    "Termine sempre com uma pergunta técnica e cite fontes."
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
