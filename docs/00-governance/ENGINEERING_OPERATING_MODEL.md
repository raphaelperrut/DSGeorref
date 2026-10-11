# Modelo operacional de engenharia orientada por IA

## Cadeia de entrega

`Product Owner → Arquiteto → Tech Lead → Implementador Especialista → QA → Reviewer → Autoridade Humana de Merge`

## Separação de responsabilidades

- Product Owner responde por valor, prioridade e aceitação de produto.
- Arquiteto responde por boundaries, contratos e decisões técnicas materiais.
- Tech Lead responde por decomposição, sequenciamento, integração e TaskEnvelopes.
- Implementadores respondem por código e testes dentro de escopos explícitos.
- QA responde por validação independente e completude da evidência.
- Reviewer realiza auditoria transversal final e não implementa a mudança revisada.
- A autoridade humana permanece responsável pelo merge.

## Workflow obrigatório

`Draft → Product Ready → Architecture Ready → Decomposed → In Progress → QA → Final Review → Merge Ready → Done`

Nenhum estado pode ser pulado. Gate reprovado devolve a mudança ao papel responsável pela etapa anterior. Cada transição deixa evidência na issue ou no pull request.

## Redução de contexto

O agente recebe apenas a seção relevante do PRD, ADR/profile/contrato, issue, TaskEnvelope, paths permitidos e testes necessários. Não deve carregar o repositório inteiro quando contexto de componente for suficiente.

## Paralelismo

Trabalho paralelo exige write scopes disjuntos ou contrato previamente integrado e imutável. Migrations compartilhadas, schemas públicos, manifests de dependência e clientes gerados são serializados.

## Modelo solo prospectivo — ADR-060

Uma pessoa humana pode acumular competências formalmente atribuídas de produto,
arquitetura, liderança técnica e autoridade humana de merge. Uma manifestação
autenticada pode exercer competências acumuláveis, sem repetição como pessoas
diferentes. Executor, QA e Reviewer permanecem em passes e contextos separados,
com evidências reais sobre o mesmo SHA. A independência pessoal é ausente e
declarada; sessões Codex não representam pessoas ou principais independentes.
DAA/trust e exigências expressas de independência estrita mantêm suas fontes.
Os gates obrigatórios de cada etapa permanecem. A exceção operacional da #1026
é de uso único e consta de CHANGE_CONTROL; não é READY, QA, final review ou merge.
