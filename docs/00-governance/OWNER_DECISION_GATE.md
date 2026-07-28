# Gate de decisão do Product Owner

Encaminhar ao Product Owner somente quando todas as condições forem verdadeiras:

1. existem pelo menos duas alternativas materialmente diferentes;
2. a escolha altera escopo, trust boundary, topologia, ownership de dados, semântica de aceitação ou promessa pública de compatibilidade;
3. o impacto é duradouro ou caro de reverter;
4. ADRs, profiles, benchmarks, contratos e issues vigentes não resolvem a escolha.

Não escalar versão de ferramenta, threshold, detalhe reversível, sizing, estrutura de testes ou refatoração compatível. Esses assuntos pertencem ao Arquiteto, Tech Lead, evidência de benchmark ou owner da issue.

O registro deve conter contexto, alternativas, recomendação, consequências, artifacts afetados e aprovação explícita. Após aprovação, a decisão é incorporada ao owner normativo e o registro temporário é removido da árvore ativa.
