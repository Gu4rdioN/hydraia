from flask import Flask, render_template, request, Response, stream_with_context
from openai import OpenAI 
import os
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- IDs DAS IAS ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
# Usando o Llama 3.1 8B Instant por ser o recordista de velocidade para testes
MODELO_LEVE = "meta-llama/llama-3.1-8b-instant:free" 

IDENTIDADE_HYDRALYNX = (
    "Você é a HYDRALYNX, um especialista técnico descontraído. "
    "REGRAS: NUNCA se apresente como IA. NUNCA fale de sua origem. "
    "Use ## para títulos e 🔹 para tópicos. Termine sempre com uma pergunta técnica. "
    "Sempre pergunte o nome do usuário no início."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        chave = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=chave)
        
        dados = request.get_json()
        pergunta = dados.get('mensagem', '')
        ia_forcada = dados.get('ia_forcada', 'GLM')

        # Escolha do modelo
        modelo_escolhido = MODELO_PESADO if ia_forcada == 'NV' else MODELO_LEVE
        print(f"LOG: Iniciando Stream com {modelo_escolhido}")

        def generate():
            # Chamada com STREAM ativado
            response = client.chat.completions.create(
                model=modelo_escolhido,
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                stream=True, # A MÁGICA ACONTECE AQUI
                temperature=0.2
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    # Enviando apenas o texto puro para o front-end
                    yield chunk.choices[0].delta.content

        return Response(stream_with_context(generate()), mimetype='text/plain')
        
    except Exception as e:
        print(f"ERRO: {e}")
        return "Erro na matriz.", 500

if __name__ == '__main__':
    app.run(debug=True)
