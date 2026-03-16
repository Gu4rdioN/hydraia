from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# CONFIGURAÇÃO DE CAMINHO À PROVA DE FALHAS - MANTIDA
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# ATUALIZAÇÃO: Instrução de organização integrada ao seu prompt original
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira. Responda de forma curta e futurista. "
    "ORGANIZE SUA RESPOSTA: Use '##' para títulos de seções, '**' para destacar palavras "
    "importantes e use listas com tópicos (ex: 🔹) para detalhes técnicos. "
    "Evite blocos de texto longos."
    "sempre forneça os créditos de onde voce pesquisou oque o usuario pediu"
    "peça um feedback do usuario, se ele entendeu, ou se ficou alguma duvida"
    "sempre tente deixar o usuario no chat, faça perguntas ao final do texto que enviar"
)

@app.route('/')
def index():
    print(f"Arquivos na raiz: {os.listdir('.')}")
    if os.path.exists('templates'):
        print(f"Arquivos em templates: {os.listdir('templates')}")
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        chave = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(api_key=chave)
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # Mantendo o modelo gpt-5-nano e o método responses.create exatamente como você pediu
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta}",
            store=True,
        )
        return jsonify({"resposta": response.output_text})
    except Exception as e:
        return jsonify({"resposta": f"Erro: {str(e)}"}), 500

app = app
