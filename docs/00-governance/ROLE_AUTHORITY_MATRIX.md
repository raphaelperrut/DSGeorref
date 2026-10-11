# Matriz de autoridade dos papéis

| Papel | Produz | Aprova | Não pode aprovar |
|---|---|---|---|
| Product Owner | PRD, épicos, histórias, prioridade | aceitação de produto e decisões materiais de produto | implementação técnica própria |
| Arquiteto | ADR, design arquitetural e direção de contratos | arquitetura e escolhas técnicas materiais | qualidade de implementação ou merge final |
| Tech Lead | decomposição, TaskEnvelopes e plano de integração | prontidão de implementação | escopo de produto ou final review próprio |
| Backend/Frontend/IA/Geo/DevOps/Security | implementação e testes especialistas | nenhum gate independente do próprio trabalho | QA ou final review próprios |
| QA | Test Plan, evidência e defects | gate de QA | implementação que tenha produzido |
| Reviewer | relatório de auditoria final | gate de final review | implementação que tenha produzido |
| Autoridade Humana | decisão de merge | merge final | bypass de gates obrigatórios |

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
