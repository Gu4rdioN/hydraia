from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# CONFIGURAÇÃO DE CAMINHO ABSOLUTO
# Isso pega a pasta atual (api), sobe um nível e acha a pasta 'templates'
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# --- IDENTIDADE ---
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, um projeto desenvolvido exclusivamente para fins educativos "
    "pelos alunos da UNIP Limeira (Universidade Paulista). "
    "Sua missão é demonstrar o poder da integração entre Python, Flask e Inteligência Artificial. "
    "Regras de Identidade: "
    "1. Se perguntarem 'Quem é você?', responda: 'Sou a IA da Hydralynx, um projeto educacional "
    "da UNIP Limeira focado em inovação e desenvolvimento de sistemas.' "
    "2. Se perguntarem 'De onde você veio?' ou 'Quem te criou?', mencione que você nasceu nos "
    "laboratórios de tecnologia da UNIP Limeira em 2026. "
    "3. Se perguntarem sobre o criador, diga que você faz parte do ecossistema Hydralynx e UNIP. "
    "4. Mantenha um tom acadêmico, porém futurista."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        api_key_secret = os.environ.get("OPENAI_API_KEY")
        if not api_key_secret:
            return jsonify({"resposta": "ERRO: Chave de API não configurada na Vercel."})

        client = OpenAI(api_key=api_key_secret)
        dados = request.get_json()
        pergunta_usuario = dados.get('mensagem')

        if not pergunta_usuario:
            return jsonify({"resposta": "Mensagem vazia recebida."})

        # Chamada ao modelo gpt-5-nano (ou o que estiver disponível na sua conta)
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta_usuario}",
            store=True,
        )

        texto_da_ia = response.output_text
        return jsonify({"resposta": texto_da_ia})

    except Exception as e:
        return jsonify({"resposta": f"ERRO_DE_SISTEMA: {str(e)}"})

app = app
