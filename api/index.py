from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Ajuste de caminho para garantir que encontre os templates
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# --- CONFIGURAÇÃO DE IDENTIDADE ---
IDENTIDADE_HYDRALYNX = (
    "Você é a HYDRALYNX, um especialista técnico descontraído e focado em programação. "
    "REGRAS: NUNCA se apresente como IA. Responda diretamente. Use ## para títulos e 🔹 para tópicos. "
    "Sempre pergunte o nome do usuário no início. Termine com uma pergunta técnica. "
    "Se o usuário brincar, entre na brincadeira."
)

# --- IDs DAS IAS (OpenRouter) ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
MODELO_LEVE = "z-ai/glm-4.5-air:free"

def definir_modelo(pergunta):
    """
    Decide qual cérebro usar. 
    Gemma (Leve) para papo furado, Nvidia (Pesada) para código.
    """
    pergunta_min = pergunta.lower()
    
    # Lista de gatilhos para ativar a IA pesada da NVIDIA
    gatilhos_programacao = [
        'python', 'javascript', 'js', 'html', 'css', 'sql', 'codigo', 'script', 
        'bug', 'erro', 'api', 'função', 'class', 'import', 'def ', 'json', 'algoritmo'
    ]
    
    # Se a pergunta contiver termos técnicos, vai de NVIDIA
    if any(termo in pergunta_min for termo in gatilhos_programacao):
        print(f"DEBUG: Roteando para NVIDIA SUPER (Código detetado)")
        return MODELO_PESADO
    
    # Caso contrário, vai de GEMMA (Muito mais rápida para 'Olá', 'Tudo bem')
    print(f"DEBUG: Roteando para GEMMA 3 (Conversa casual)")
    return MODELO_LEVE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        # Pega a chave das variáveis de ambiente
        chave = os.environ.get("OPENAI_API_KEY")
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem', '')

        if not pergunta:
            return jsonify({"resposta": "Ei, você esqueceu de digitar a mensagem!"}), 400

        # Escolhe o modelo baseado na pergunta
        modelo_escolhido = definir_modelo(pergunta)

        response = client.chat.completions.create(
            model=modelo_escolhido, 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.6 # Aumentei um pouco para ela ser mais "descontraída" como você pediu
        )
        
        texto_resposta = response.choices[0].message.content
        
        return jsonify({
            "resposta": texto_resposta,
            "modelo": modelo_escolhido # Enviamos o ID para conferência
        })
        
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return jsonify({"resposta": f"Erro na matriz: {str(e)}"}), 500

if __name__ == '__main__':
    # Rodando em modo Debug para você ver os logs no terminal
    app.run(debug=True)
