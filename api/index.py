from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# IDENTIDADE DA HYDRALYNX (Mantida conforme sua solicitação)
IDENTIDADE_HYDRALYNX = (
    "Você é a IA da Hydralynx, da UNIP Limeira... (seu texto aqui)"
)

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        # No OpenRouter, você precisa passar a URL base
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"), # Sua chave do OpenRouter
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # MODELO CORRIGIDO: Usando o Llama 3.1 8B (Estável e rápido no OpenRouter)
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct", 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ]
        )
        
        return jsonify({"resposta": response.choices[0].message.content})
        
    except Exception as e:
        return jsonify({"resposta": f"Erro na Hydralynx: {str(e)}"}), 500
