# AP-008 — SPRINT-001 execution profile

- **Status:** `Accepted`
- **Owner ADRs:** ADR-002, ADR-034 e ADR-026

## Aplicação

A SPRINT-001 é gate-oriented e termina por evidência, não por duração fixa. O escopo mínimo inclui scaffold por contracts, schemas iniciais finos, ambiente reproduzível, serviços reais nos tiers aplicáveis, walking skeleton diagnóstico ponta a ponta, CI progressivo e `SprintEvidenceSet` machine-readable.

Issues são escolhidas pelo grafo de gates e executadas em ondas verticais. O encerramento exige foundation checks, migrations exercitadas, autenticação quando houver rede, roots seguros, diagnóstico e autorização explícita da primeira fatia. Detalhes de branch, Project e DoR/DoD pertencem ao operating model de engenharia.
