## Visão Geral

Esse é um projeto backend que atende um sistema de RAG (Retrieval-Augmented Generation).
O projeto é basicamente uma API que recebe request HTTP para processamento. O arquivo ./app.py é o ponto de entrada da aplicação, onde as rotas são definidas e o servidor é iniciado.


# Funcionalidade do projeto e endpoints da API
- '/api/v1/home'
  - somente metodo GET para retornar ok

- '/api/v1/askme'
  - metodo POST que recebe um json com a pergunta do usuario e seus dados e retorna a resposta gerada pelo sistema RAG'. Esse endpoint é chamado a partir de integrações com whatsapp

- '/api/v1/askme-chat-online'
  - metodo POST que recebe um json com a pergunta do usuario e retorna a resposta gerada pelo sistema RAG, a diferença do endopoint /api/v1/askme é que nesse caso nós receberemos um historico de conversa pois as mensagens são enviadas diretamente de um front end e não do whatsapp podendo ser acessado por inumeras pessoas ao mesmo tempo

- '/api/v1/services'
  - metodo post que recebe um json com os dados dos servicos que a empresa oferece para que futuramente possam ser utilizados na base de conhecimento'

- '/api/v1/validate-key'
  - metodo POST que recebe um json com a api key do usuario e valida se a chave é valida'

- 'api/v1/contact'
  - metodo POST que recebe um json mensagens dos usuarios para contato.

- 'api/v1/register'
  - metodo POST que recebe um json com os dados do usuario para cadastro no sistema

## Funcionalidades Principais
o cliente informa os dados da empresa ou negocio dele, as informações sao enviadas para o banco de dados em vetor pinecone para que futuramente possam ser utilizadas na base de conhecimento do sistema RAG.
O usuário do sistema pode fazer perguntas e o sistema responde com base em um conjunto de documentos fornecidos.
A base de conhecimento é composta por documentos que são processados e armazenados em um vetor de embeddings para facilitar a recuperação rápida de informações relevantes.
O sistema utiliza a biblioteca LangChain para gerenciar a cadeia de processos, incluindo a recuperação de documentos e a geração de respostas.
O modelo de linguagem utilizado é o GPT-x da OpenAI, que é capaz de gerar respostas coerentes e contextualmente relevantes com base nos documentos recuperados.
O fluxo de trabalho do sistema é o seguinte:
1. O usuário faz uma pergunta.
2. O sistema utiliza um mecanismo de recuperação para encontrar documentos relevantes na base de conhecimento. 
3. Os documentos recuperados são então passados para o modelo de linguagem GPT-4, que gera uma resposta baseada nessas informações.
4. A resposta é então retornada ao usuário.

## Informações adicionais
O sistema também servira como um cadastrador de usuarios que informarao os dados da sua empresa para que futuramente possam ser utilizados na base de conhecimento.
o casdastro é feito no endpoint /api/v1/register