# ISSUE-0674 — auditoria final do EPIC-091

Este diretório é o locator canônico permitido pelo `TASK-0564` para a evidência
versionada da `STORY-0564`. O diff materializa somente auditoria executável; não
altera contratos, implementação, automação nem testes predecessores.

## Alvo e decisão da revisão

- candidato revisado: `4d3e5d69192b7b52b10e02af758dcf3b41727ee0`;
- tree do candidato: `ed7894a798841a18b15e07829a2e3f195436e233`;
- merge que integrou o predecessor: `a4d2579291d7e2868899127157f9205313cbc172`;
- implementação revisada: `ISSUE-0673` / GitHub `#61` / PR `#964`;
- Reviewer: `PASS` para o candidato acima;
- QA automatizada independente: `PASS` para o mesmo candidato, conjunto de
  evidências e riscos residuais.

O `REVIEW_EVIDENCE.json` fixa SHA, tree e SHA-256 canônico de todos os onze blobs
alterados pelo candidato. O teste confere os digests contra o worktree com finais
de linha normalizados e diretamente contra os blobs Git. A árvore do candidato é
idêntica à árvore do merge em `main`.

## Evidência por critério

| Critério | Evidência | Resultado |
|---|---|---|
| `AC-ISSUE-0674-01` | contrato congelado, ruleset, registry de dois checks únicos, CODEOWNERS, workflow e validadores no SHA exato | PASS |
| `AC-ISSUE-0674-02` | os cinco requisitos resolvem ao checkpoint final `test_epic_091_integracao` e aos respectivos testes canônicos | PASS |
| `AC-ISSUE-0674-03` | política insegura, check duplicado, CODEOWNERS incompleto, bypass parcial/stale, evidência divergente e workflow permissivo são rejeitados | PASS |
| `AC-ISSUE-0674-04` | QA hospedada e Reviewer registram `PASS` no mesmo candidato, evidence set e risco; aprovação implícita é rejeitada | PASS |

Os entrypoints públicos obrigatórios são:

- `test_epic_091_aceite_happy_path`;
- `test_epic_091_aceite_negative_paths`.

Eles reutilizam os checkpoints owner por subprocessos isolados. Nenhuma regra de
governança é copiada para este bundle.

## Validações

- contrato, fundação, automação e integração: `PASS`, 8 testes focados;
- runners diretos de automação e integração: `PASS`, JSON determinístico e
  fail-closed;
- checks hospedados `epic-091-main-ruleset-controls` e `foundation-ci`:
  `SUCCESS` no SHA candidato;
- sentinelas obrigatórias desta issue: `PASS`, 2 testes cobrindo happy path e
  negative paths;
- Ruff direcionado, mypy estrito, JSON/digests e `git diff --check`: `PASS`;
- `make verify`: avançou por qualidade Python e frontend, revisões A-F,
  arquitetura Python, licenciamento e fundação do monorepo; parou somente no E2E
  preexistente que requer `FOUNDATION_INTEGRATION=1` e PostgreSQL/RabbitMQ. O
  mesmo gate passou no `foundation-ci` do candidato exato.

## Independência, limites e risco residual

O Reviewer audita o commit produzido pela `ISSUE-0673`; esta evidência não aprova
o próprio diff da `ISSUE-0674`, que continua sujeito a revisão independente antes
de merge. A QA é executada por GitHub Actions, autoridade distinta do Reviewer,
no mesmo SHA candidato.

Além da ausência de enforcement remoto comprovável, permanecem apenas limitações
ambientais `LOW`: o Node local é 22.14.0 em vez do 24.20.0 pinado, e o E2E de
fundação requer os serviços disponíveis no CI. Nenhuma delas altera o resultado
dos testes focados ou abre risco arquitetural.

O risco residual `LOW` é a ausência de prova de enforcement remoto: a API de
rulesets/proteção é negada pelo plano atual do repositório. O contrato, ruleset,
automação e evidência dizem explicitamente `NOT_ASSERTED`; portanto não existe
fallback silencioso nem claim de proteção ao vivo. Não há risco arquitetural aberto.

## Contratos, migration e rollback

Impacto em contrato, schema, estado persistido, deployment e runtime: `NONE`.
Migration e rollback de dados não se aplicam. O rollback é reverter o commit de
evidência da `ISSUE-0674`.
