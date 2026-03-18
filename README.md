# Hydra IA

projeto de chatbot desenvolvido em .py, .html e .json, utilizando api nvidia nemotron 3 super
biblioteca flask para criação do servidor web e comunicação usuario
biblioteca jsonify para comunicação do chatbot com o usuario

identidade do chatbot definida totalmente para se comportar como um humano,
responder perguntas de forma objetiva, prender o usuario ao chat,
desenvolver conhecimento e fortificar codigos de linguagens de programação

a API utilizada foi a Nvidia Nemotron 3 Super 120b, melhor escolha que encontrei
para os requisitos que a interface irá ajudar o usuário,
pode ser modificada facilmente na linha 40 do arquivo api/index.py, podendo ser utilizada
qualquer api que for melhor para você

o host utilizado está sendo o Vercel (vercel.com) de forma gratuita pode se hospedar seu chatbot
criei uma variavel dentro do vercel com a key gerada pelo openrouter e chamei a variavel na linha 27
o arquivo vercel.json fará a ponte entre python e o html, arquivo necessário para esse host funcionar com sua ia
o arquivo requirements.txt é usado para "avisar" ao vercel quais bibliotecas instalar, tambem é necessario para qualquer tipo de hospedagem

o arquivo templates/index.html utilizado no site também está disponivel, voce pode fazer qualquer alteração para melhorar fluidez ou partes do site que vão ficar a mostra ao usuario

por ser uma IA pesada (120bilhões) ela é um pouco lenta para responder, porém a resposta é profunda e certeira, diferente de modelos 12b, 6b, 2b... que priorizam velocidade

resumo doque foi utilizado no chatbot:

openrouter (openrouter.ai) para geração da key

vercel (vercel.com) para hospedagem do site


o site que foi desenvolvido com esse mesmo codigo estara disponivel nesse endereço:
https://hydraia.vercel.app/
Nvidia Nemotron 3 Super 120b (API da IA Nvidia)

bibliotecas flask e openai

