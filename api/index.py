from flask import Flask
from openai import OpenAI
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Modelo 8B é drasticamente mais rápido para testes no plano free
MODELO_ESTAVEL = "meta-llama/llama-3.1-8b-instant:free"

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
        client = OpenAI(base_url="https://openrouter.ai/api/v1/chat/completions", api_key=chave)
        
        dados = request.get_json()
        pergunta = dados.get('mensagem', '')

        print(f"LOG: Processando pergunta com {MODELO_ESTAVEL}")

        def generate():
            response = client.chat.completions.create(
                model=MODELO_ESTAVEL,
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                stream=True,
                temperature=0.4
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return Response(stream_with_context(generate()), mimetype='text/plain')
        
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        return "Erro na conexão com a matriz.", 500

if __name__ == '__main__':
    app.run(debug=True)
