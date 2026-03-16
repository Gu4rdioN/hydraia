from flask import Flask, render_template, request, jsonify  # ADICIONADO AQUI
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
    "Evite blocos de texto longos. "
    "Sempre forneça os créditos de onde você pesquisou o que o usuário pediu. "
    "Peça um feedback do usuário, se ele entendeu, ou se ficou alguma dúvida. "
    "Sempre tente deixar o usuário no chat, faça perguntas ao final do texto que enviar."
"você foi criada por alunos do primeiro semestre de ciencia da computação da unip com ajuda de professores da unip"
            "voce foi desenvolvida sobre linguagem, python, css, html, json, javascript e funciona sem banco de dados"
            "se dia de criação foi dia 11/03/2026 no campus da unip limeira"
            "voce entrou no ar às 21:05 da noite do dia 11/03/2026"
)

@app.route('/')
def index():
    # Diagnóstico para logs da Vercel
    print(f"Arquivos na raiz: {os.listdir('.')}")
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
        # Retorna o erro real para ajudar no debug
        return jsonify({"resposta": f"Erro: {str(e)}"}), 500

app = app
