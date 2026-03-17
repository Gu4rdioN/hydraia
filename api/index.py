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
    "REGRAS DE SILÊNCIO: NUNCA se apresente, NUNCA mencione que é uma IA. "
    "NUNCA fale de sua origem ou criadores, a menos que perguntado diretamente. "
    "EXECUÇÃO: Responda diretamente à dúvida do usuário. Use ## para títulos e 🔹 para tópicos. "
    "Termine sempre com uma pergunta técnica. "
    "Sempre pergunte o nome do usuário no início da conversa e use-o para se dirigir a ele. "
    "Saiba quando o usuário está brincando e entre na brincadeira."
)

# --- IDs DAS IAS ---
MODELO_PESADO = "nvidia/nemotron-3-super-120b-a12b:free"
MODELO_LEVE = "google/gemma-3-12b-it:free"

def definir_modelo(pergunta):
    """
    Analisa se a pergunta é sobre programação para escolher a melhor IA.
    """
    termos_tecnicos = [
        'python', 'javascript', 'js', 'html', 'css', 'sql', 'codigo', 'script', 
        'bug', 'erro', 'api', 'função', 'class', 'import', 'servidor', 'deploy'
    ]
    pergunta_min = pergunta.lower()
    
    # Se encontrar qualquer termo técnico, vai para a Nvidia Super
    if any(termo in pergunta_min for termo in termos_tecnicos):
        return MODELO_PESADO
    return MODELO_LEVE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        chave = os.environ.get("OPENAI_API_KEY")
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=chave
        )
        
        dados = request.get_json()
        pergunta = dados.get('mensagem')

        # --- LÓGICA DE ROTEAMENTO ---
        modelo_escolhido = definir_modelo(pergunta)
        # 🔹 Exemplo Prático: Se o usuário digitar "olá", usa o Gemma. 
        # Se digitar "como fazer um loop?", usa o Nemotron.

        response = client.chat.completions.create(
            model=modelo_escolhido, 
            messages=[
                {"role": "system", "content": IDENTIDADE_HYDRALYNX},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.3
        )
        
        # Adicionei uma informação extra no log do servidor para você ver qual IA respondeu
        print(f"HYDRALYNX selecionou: {modelo_escolhido}")
        
        return jsonify({
            "resposta": response.choices[0].message.content,
            "modelo_usado": modelo_escolhido # Opcional: enviar pro front qual IA respondeu
        })
        
    except Exception as e:
        return jsonify({"resposta": f"Erro na matriz de processamento: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
