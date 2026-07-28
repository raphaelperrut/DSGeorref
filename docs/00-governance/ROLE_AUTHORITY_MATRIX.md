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
