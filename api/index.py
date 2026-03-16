from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# Forçando o Flask a achar a pasta templates dentro de /api
app = Flask(__name__, template_folder='templates')

# Puxa a chave da Vercel
api_key_secret = os.environ.get("OPENAI_API_KEY")

# Inicializa o cliente apenas se a chave existir para não travar o app
client = None
if api_key_secret:
    client = OpenAI(api_key=api_key_secret)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        if not client:
            return jsonify({"resposta": "Erro: API Key não configurada na Vercel."})

        dados = request.get_json()
        pergunta = dados.get('mensagem', '').lower()

        # Detecção de imagem
        palavras_imagem = ["gere", "imagem", "foto", "desenhe", "crie"]
        if any(p in pergunta for p in palavras_imagem):
            # MOTOR DE IMAGEM (DALL-E 3)
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"Realistic cinematic photo of {pergunta}, 8k resolution",
                n=1,
                size="1024x1024"
            )
            url = response.data[0].url
            return jsonify({"resposta": f"Processando imagem...<br><img src='{url}'>"})

        # MOTOR DE TEXTO
        # Usei o modelo 'gpt-3.5-turbo' por segurança, pois o 'gpt-5-nano' 
        # pode ainda não estar liberado na sua conta específica da OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a IA da Hydralynx UNIP Limeira."},
                {"role": "user", "content": pergunta}
            ]
        )
        return jsonify({"resposta": completion.choices[0].message.content})

    except Exception as e:
        # Esse print ajuda a ver o erro real nos Logs da Vercel
        print(f"Erro Real: {e}")
        return jsonify({"resposta": f"Erro no núcleo: {str(e)}"}), 500

app = app
