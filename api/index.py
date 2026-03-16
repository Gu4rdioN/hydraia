from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__, template_folder='templates')

# Configuração Segura da API
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

IDENTIDADE_HYDRALYNX = (
    "Você é a Hydralynx, o núcleo neural desenvolvido pelos alunos da UNIP Limeira. "
    "Sua missão é fornecer dados precisos e futuristas. "
    "REGRAS DE RESPOSTA: "
    "1. SEMPRE use Markdown para estruturar a resposta. "
    "2. Use títulos (##) para cada novo tópico. "
    "3. Use negrito (**) em conceitos fundamentais. "
    "4. Para listas, use tópicos com ícones (Ex: 🔹 ou 🚀). "
    "5. Mantenha parágrafos curtos e objetivos."
            "6. sempre peça feedback do usuario, se ele ficou com alguma duvida ou outra pergunta"
            "7. quando solicitado de gerar imagens diga que consegue apenas gerar imagens pequenas"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        if not client:
            return jsonify({"resposta": "⚠️ Erro: Conexão com Hydra não estabelecida."})

        dados = request.get_json()
        mensagem = dados.get('mensagem', '')

        # Lógica de Imagem
        gatilhos_img = ["gere", "imagem", "foto", "desenhe", "criar imagem"]
        if any(g in mensagem.lower() for g in gatilhos_img):
            img_res = client.images.generate(
                model="dall-e-3",
                prompt=f"Futuristic cinematic photo of {mensagem}, high detail, 8k",
                n=1, size="1024x1024"
            )
            return jsonify({"resposta": f"## 🎨 Geração Concluída\n\n![Hydralynx Vision]({img_res.data[0].url})"})

        # Lógica de Texto Estruturado
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Mais rápido e inteligente que o 3.5
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": mensagem}
            ],
            temperature=0.6 # Equilíbrio entre criatividade e precisão
        )
        return jsonify({"resposta": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"resposta": f"❌ Erro de Sistema: {str(e)}"}), 500

app = app
