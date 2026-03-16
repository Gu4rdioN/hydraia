from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# CONFIGURAÇÃO DE CAMINHO À PROVA DE FALHAS
# Isso força o Flask a olhar para a raiz do projeto (onde a Vercel monta o build)
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# TENTATIVA DE MAPEAR O CAMINHO REAL SE O DE CIMA FALHAR
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    # Se estiver rodando dentro da Vercel, às vezes o caminho raiz é o atual
    app.template_folder = os.path.join(os.getcwd(), 'templates')

IDENTIDADE_HYDRALYNX = (
            "Você é a IA da Hydralynx, da UNIP Limeira. Responda de forma curta e futurista."
            "quando solicitado uma imagem, diga ao usuario que voce consegue apenas fornecer imagens simples"
            "responda de forma educacional as perguntas, com os lugares de onde voce fez a pesquisa sobre a pergunta do usuario"
            "voce deve se adaptar ao usuario, se o usuario pedir para voce mudar seu estilo, mude."
            "REGRAS DE FORMATAÇÃO: "
            "1. Use títulos (##) para separar seções. "
            "2. Use listas (bullet points) para detalhes técnicos. "
            "3. Use negrito (**) para destacar termos importantes. "
            "4. Mantenha os parágrafos curtos. "
            "5. Sempre que listar itens, use uma estrutura de tópicos clara."
            "sempre peça feedback do usuario para saber se quer que deixe de forma mais clara, ou se teve alguma duvida"

)

@app.route('/')
def index():
    # Teste de diagnóstico: lista os arquivos para você ver no log se a pasta existe
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

        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta}",
            store=True,
        )
        return jsonify({"resposta": response.output_text})
    except Exception as e:
        return jsonify({"resposta": f"Erro: {str(e)}"}), 500

app = app
