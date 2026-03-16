from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# CONFIGURAÇÃO DE DIRETÓRIOS ABSOLUTOS
# Isso resolve o erro 500 de "TemplateNotFound" ou caminhos errados
path_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
path_projeto_raiz = os.path.dirname(path_diretorio_atual)
path_templates = os.path.join(path_projeto_raiz, 'templates')

app = Flask(__name__, template_folder=path_templates)

IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, desenvolvida para fins educativos pelos alunos da UNIP Limeira. "
    "Responda sempre como a inteligência oficial da Hydralynx."
)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # Se der erro aqui, ele vai imprimir exatamente o que falta
        return f"Erro de Inicialização: {str(e)}", 500

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        chave = os.environ.get("OPENAI_API_KEY")
        if not chave:
            return jsonify({"resposta": "Chave de API não configurada na Vercel."}), 500

        client = OpenAI(api_key=chave)
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta}",
            store=True,
        )

        return jsonify({"resposta": response.output_text})
    except Exception as e:
        return jsonify({"resposta": f"Erro Neural: {str(e)}"}), 500

# Necessário para Vercel
app = app
