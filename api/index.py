from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# Configuração de pastas para a estrutura que você tem no GitHub (api/templates)
app = Flask(__name__, template_folder='templates')

# --- CONFIGURAÇÃO DA API ---
# A chave deve estar nas Environment Variables da Vercel para segurança
api_key_secret = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key_secret)

IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira. "
    "Se o usuário pedir uma imagem, crie um prompt detalhado em inglês para o DALL-E, "
    "pois ele entende melhor descrições técnicas nessa língua."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        if not api_key_secret:
            return jsonify({"resposta": "Erro: Chave de API não configurada na Vercel."})

        dados = request.get_json()
        pergunta_usuario = dados.get('mensagem', '').lower()

        # LÓGICA DE DETECÇÃO: O usuário quer uma imagem?
        palavras_chave_imagem = ["gere", "imagem", "foto", "desenhe", "crie uma imagem"]
        quer_imagem = any(palavra in pergunta_usuario for palavra in palavras_chave_imagem)

        if quer_imagem:
            # 1. Gerar a imagem usando DALL-E 3
            # O DALL-E 3 cria imagens fotorrealistas de alta qualidade
            response_image = client.images.generate(
                model="dall-e-3",
                prompt=f"Realistic high quality image of: {pergunta_usuario}. Cinematic lighting, 8k, detailed.",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            url_imagem = response_image.data[0].url
            
            # Retornamos um HTML especial que o seu JavaScript vai renderizar
            return jsonify({
                "resposta": f"Hydralynx Gerador Ativo. Aqui está sua imagem:<br><img src='{url_imagem}' style='width:100%; border-radius:10px; margin-top:10px;'>"
            })

        # 2. Fluxo Normal de Texto (se não pediu imagem)
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{IDENTIDADE_HYDRALYNX}\n\nUsuário: {pergunta_usuario}",
            store=True,
        )

        return jsonify({"resposta": response.output_text})

    except Exception as e:
        return jsonify({"resposta": f"ERRO_DE_SISTEMA: {str(e)}"})

app = app
