from flask import Flask, render_template, request, Response, stream_with_context
from openai import OpenAI 
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- CONFIGURAÇÃO ÚNICA ---
MODELO_NVIDIA = "nvidia/nemotron-3-super-120b-a12b:free"

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
        # Configuração do cliente voltada para o OpenRouter
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=chave)
        
        dados = request.get_json()
        pergunta = dados.get('mensagem', '')

        print(f"LOG: Iniciando Stream com NVIDIA Nemotron")

        def generate():
            response = client.chat.completions.create(
                model=MODELO_NVIDIA,
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                stream=True,
                temperature=0.2
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    # Envia o fragmento de texto em tempo real
                    yield chunk.choices[0].delta.content

        return Response(stream_with_context(generate()), mimetype='text/plain')
        
    except Exception as e:
        print(f"ERRO: {e}")
        return "Erro na matriz.", 500

if __name__ == '__main__':
    app.run(debug=True)
