from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__, template_folder='../templates')

api_key_secret = os.environ.get("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key_secret
)

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
        if not api_key_secret:
            return jsonify({"resposta": "ERRO: Chave de API não configurada nas variáveis de ambiente da Vercel."})

        dados = request.get_json()
        pergunta_usuario = dados.get('mensagem')

        if not pergunta_usuario:
            return jsonify({"resposta": "Mensagem vazia recebida."})

        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta_usuario}",
            store=True,
        )

        texto_da_ia = response.output_text
        return jsonify({"resposta": texto_da_ia})

    except Exception as e:
        print(f"Erro detectado: {e}")
        return jsonify({"resposta": f"ERRO_DE_SISTEMA: O núcleo neural não respondeu. ({str(e)})"})

app = app
