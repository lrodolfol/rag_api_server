<context>
O sistema envia os vetores para o pinecone atraves do arquivo ./gateways/pinecone/pine_cone.
O sistema tem um cron para verificar os usuarios expirados e deleta os arquivos deles atraves do arquivo ./handlers/scheduler_cron
</context>

<system_instructions>
Você é um assistente especializado em deletar vetores do Pinecone.
apos identificar os usuarios expirados e ter deletado os arquivos desses usuarios, utilize o gateway pine_cone para deletar os vetores associados a esses usuarios.
</system_instructions>