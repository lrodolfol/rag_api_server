# Soluções para o período gratuito de 14 dias

1. **Monitoramento de elegibilidade**
   - Registrar a data exata de cadastro do cliente e calcular o último dia gratuito consultando a diferença com a data atual.
   - Validar o campo `is_premium` para garantir que apenas clientes com a inscrição gratuita ativa tenham acesso aos recursos premium.

2. **Automação de notificações**
   - Enviar alertas automáticos por e-mail ou webhook quando o cliente atingir o décimo terceiro dia de acesso gratuito para lembrá-lo do término.
   - Programar avisos internos para revisão manual caso o sistema detecte inconsistência na data ou no status `is_premium`.

3. **Encerramento suave do acesso**
   - Bloquear ou reduzir gradualmente os recursos premium no décimo quinto dia até que o plano pago seja confirmado.
   - Atualizar o campo `is_premium` com um estado `trial_expired` para facilitar auditoria e evitar confusões futuras.

4. **Relatórios e métricas**
   - Gerar relatórios periódicos sobre quantos clientes estão em período gratuito, quantos ainda não converteram e quais serviços utilizaram.
   - Usar essas métricas para ajustar as campanhas de retenção e os fluxos de comunicação.

5. **Configuração e testes**
   - Centralizar essas regras em uma camada de configuração reutilizável para facilitar ajustes no tempo de duração ou nos gatilhos de notificação.
   - Criar testes automatizados que confirmem o corte do acesso após 14 dias e a ativação correta do status `is_premium`.
