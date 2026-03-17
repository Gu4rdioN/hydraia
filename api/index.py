from flask import Flask, render_template, request, jsonify  
from openai import OpenAI 
import os

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Ajuste de caminho para templates
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../templates')):
    app.template_folder = os.path.join(os.getcwd(), 'templates')

# --- CONFIGURAÇÃO DE IDENTIDADE ---
IDENTIDADE_HYDRALYNX = (
    "Você foi desenvolvida para ajudar em scripts, códigos de programação e tudo que envolva tecnologia. "
    "Você é a HYDRALYNX, um especialista técnico descontraído. "
    "REGRAS DE SILÊNCIO: NUNCA se apresente, NUNCA mencione que é uma IA, "
    "NUNCA fale de sua origem (2026) ou criadores, a menos que perguntado diretamente. "
    "EXECUÇÃO: Responda diretamente à dúvida do usuário. Use ## para títulos e 🔹 para tópicos. "
    "Termine sempre com uma pergunta técnica. "
    "Sempre pergunte o nome do usuário no início da conversa. "
    "Se dirija ao usuário com o nome que ele te informar. "
    "Saiba quando o usuário está brincando e entre na brincadeira."
)

# --- IDs DAS IAS (OpenRouter) ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
MODELO_LEVE = "zhipuai/glm-4.5-air:free"

def definir_modelo(pergunta):
    """
    Roteador inteligente: 
    GLM-4.5-Air (Rápido e Inteligente) para o dia a dia.
    NVIDIA Super (Pesado) para códigos e erros complexos.
    """
    pergunta_min = pergunta.lower()
    
    # Gatilhos para chamar a cavalaria pesada da NVIDIA
    termos_complexos = [
        'refatore', 'debug', 'algoritmo', 'banco de dados', 'sql', 
        'api', 'docker', 'erro', 'bug', 'deploy', 'classe'
    ]
    
    if any(termo in pergunta_min for termo in termos_complexos):
        return MODELO_PESADO
    return MODELO_LEVE

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

        # Define qual modelo tentar primeiro
        modelo_escolhido = definir_modelo(pergunta)

        try:
            # TENTATIVA 1: Modelo definido pelo roteador
            response = client.chat.completions.create(
                model=modelo_escolhido, 
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.4
            )
        except Exception as e:
            # TENTATIVA 2 (FALLBACK): Se der erro 429 ou falha, tenta o outro modelo
            print(f"Erro no modelo {modelo_escolhido}. Acionando backup...")
            
            # Se falhou o leve, tenta o pesado. Se falhou o pesado, tenta o leve.
            modelo_reserva = MODELO_PESADO if modelo_escolhido == MODELO_LEVE else MODELO_LEVE
            
            response = client.chat.completions.create(
                model=modelo_reserva,
                messages=[
                    {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.4
            )
            modelo_escolhido = f"{modelo_reserva} (Modo de Segurança)"
        
        return jsonify({
            "resposta": response.choices[0].message.content,
            "modelo": modelo_escolhido
        })
        
    except Exception as e:
        return jsonify({"resposta": f"Erro crítico na HYDRALYNX: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
