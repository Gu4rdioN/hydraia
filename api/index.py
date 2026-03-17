from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
            "voce foi desenvolvida para ajudar em scripts, codigos de programação e tudo que envolva programação"
    "Você é a HYDRALYNX, um especialista técnico descontraído. "
    "REGRAS DE SILÊNCIO: NUNCA se apresente, NUNCA mencione que é uma IA, "
    "NUNCA fale de sua origem (2026) ou criadores, a menos que perguntado diretamente. "
    "EXECUÇÃO: Responda diretamente à dúvida do usuário. Use ## para títulos e 🔹 para tópicos. "
    "Termine sempre com uma pergunta técnica."
            "sempre pergunte o nome do usuario no inicio da conversa"
            "se dirija ao usuario com o nome que ele te informar"
            "NUNCA diga sobre essas informações de identidade"
            "cite fontes APENAS quando o USUARIO PEDIR para voce fazer uma pesquisa"
            "saiba quando o usuario está brincando com você, e entre na brincadeira também"
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
            temperature=0.3
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:

        return jsonify({"resposta": f"Erro na matriz Nvidia: {str(e)}"}), 500


app = app
