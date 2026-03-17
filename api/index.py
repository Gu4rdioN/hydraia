from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- IDs DAS IAS (ATUALIZADO) ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
# Trocamos GLM pelo Gemini 2.0 Flash Lite (Alta Velocidade)
MODELO_LEVE = "google/gemini-2.0-flash-lite-preview-02-05:free" 

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
        ia_forcada = dados.get('ia_forcada', 'GLM') # O botão no HTML ainda envia 'GLM', mas o Python usará o Gemini

        # --- LÓGICA DE ESCOLHA ---
        if ia_forcada == 'NV':
            modelo_escolhido = MODELO_PESADO
            print("LOG: Usuário forçou NVIDIA SUPER")
        else:
            # Aqui ele ignora o nome 'GLM' vindo do botão e usa o Gemini configurado acima
            modelo_escolhido = MODELO_LEVE
            print("LOG: Usuário forçou GEMINI FLASH LITE")

        try:
            response = client.chat.completions.create(
                model=modelo_escolhido, 
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.4,
                timeout=20.0 # Define um limite de espera de 20 segundos
            )
        except Exception as e:
            print(f"ALERTA: Erro no modelo principal: {e}. Tentando reserva...")
            modelo_reserva = MODELO_PESADO if modelo_escolhido == MODELO_LEVE else MODELO_LEVE
            response = client.chat.completions.create(
                model=modelo_reserva,
                messages=[{"role": "system", "content": IDENTIDADE_HYDRALYNX}, {"role": "user", "content": pergunta}]
            )
            modelo_escolhido = f"{modelo_reserva} (Reserva)"

        return jsonify({
            "resposta": response.choices[0].message.content,
            "modelo": modelo_escolhido
        })
        
    except Exception as e:
        print(f"ERRO: {e}")
        return jsonify({"resposta": f"Erro na matriz: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
