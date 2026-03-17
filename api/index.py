from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Ajuste de caminho para garantir que encontre os templates
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# --- CONFIGURAÇÃO DE IDENTIDADE HYDRALYNX ---
IDENTIDADE_HYDRALYNX = (
    "Você foi desenvolvida para ajudar em scripts, códigos de programação e tecnologia. "
    "Você é a HYDRALYNX, um especialista técnico descontraído. "
    "REGRAS: NUNCA se apresente como IA. NUNCA fale de sua origem. "
    "Use ## para títulos e 🔹 para tópicos. Termine sempre com uma pergunta técnica. "
    "Sempre pergunte o nome do usuário no início e use-o durante a conversa."
)

# --- IDs DAS IAS (OpenRouter) ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
MODELO_LEVE = "zhipuai/glm-4.5-air:free"

def definir_modelo(pergunta):
    """
    Roteador de Inteligência:
    - Se a pergunta for curta (ex: 'teste', 'oi'), vai para o GLM (Rápido).
    - Se tiver termos de programação pesada, vai para NVIDIA (Potente).
    """
    pergunta_min = pergunta.lower()
    palavras = pergunta_min.split()
    
    # 1. Gatilhos de Programação Real
    gatilhos_tecnicos = [
        'def ', 'class ', 'import ', 'python', 'javascript', 'html', 'css',
        'sql', 'algoritmo', 'refatore', 'api', 'docker', 'json', 'deploy',
        'função', 'variável', 'loop', 'array', 'backend'
    ]

    # Regra 1: Se for uma mensagem muito curta (menos de 3 palavras), vai de GLM
    if len(palavras) < 3:
        print("DEBUG: Mensagem curta. Roteando para GLM-4.5-Air")
        return MODELO_LEVE

    # Regra 2: Se contiver termos técnicos, chama a NVIDIA
    if any(termo in pergunta_min for termo in gatilhos_tecnicos):
        print("DEBUG: Código/Técnico detectado. Roteando para NVIDIA SUPER")
        return MODELO_PESADO

    # Regra 3: Conversas longas mas não técnicas vão de GLM
    print("DEBUG: Conversa geral. Roteando para GLM-4.5-Air")
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
            return jsonify({"resposta": "Nenhum comando recebido."}), 400

        # Seleção automática de modelo
        modelo_escolhido = definir_modelo(pergunta)

        try:
            # TENTATIVA 1: Modelo ideal
            response = client.chat.completions.create(
                model=modelo_escolhido, 
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.4
            )
        except Exception as e:
            # TENTATIVA 2: Fallback (Se o modelo principal falhar/429)
            print(f"ALERTA: Erro no modelo {modelo_escolhido}. Tentando backup...")
            modelo_reserva = MODELO_PESADO if modelo_escolhido == MODELO_LEVE else MODELO_LEVE
            
            response = client.chat.completions.create(
                model=modelo_reserva,
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.4
            )
            modelo_escolhido = f"{modelo_reserva} (Backup)"

        return jsonify({
            "resposta": response.choices[0].message.content,
            "modelo": modelo_escolhido
        })
        
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return jsonify({"resposta": f"Erro na matriz neural: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
