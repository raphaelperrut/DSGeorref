# ISSUE-0135 — auditoria final do EPIC-005

Este diretório é o locator canônico permitido pelo `TASK-0025` para a evidência
versionada da `STORY-0025`. Ele normaliza o locator legado
`evidence/reviews/epic-005/story-0025/` sem alterar o TaskEnvelope, contratos,
código de produção ou suites predecessoras.

## Alvo da revisão

- implementação revisada: `780f45410d237f43b2658254fbe9742df96b9c28`;
- merge que integrou o predecessor: `82cb629a929bf5664206eb77a4d653d2b3b0ffc9`;
- issue implementadora: `ISSUE-0134` / GitHub `#36`;
- resultado do Reviewer: `PASS` para o candidato acima.

`REVIEW_EVIDENCE.json` fixa os SHA-256 dos cinco arquivos alterados pelo
candidato. O teste de aceite recalcula esses digests, evitando que a auditoria
seja reutilizada após drift do código, TaskEnvelope, documentação, testes ou
evidência de implementação.

## Evidência por critério

| Critério | Evidência |
|---|---|
| `AC-ISSUE-0135-01` | relatório JSON determinístico de `repository_integration.py`, workflow pinado e `test_epic_005_aceite_happy_path` |
| `AC-ISSUE-0135-02` | digests do candidato e entrypoints governados de `REQ-BEX-001`, `REQ-BEX-006` e `REQ-FS1-006` |
| `AC-ISSUE-0135-03` | oito mutações da automação, quality report malformado/falho, requisito desconhecido, proteção de imports, SHA divergente e aprovação implícita |
| `AC-ISSUE-0135-04` | coordenação explícita de QA e Reviewer no mesmo SHA, evidence set e risco residual; QA permanece `PENDING` |

Os entrypoints públicos exigidos são:

- `test_epic_005_aceite_happy_path`;
- `test_epic_005_aceite_negative_paths`.

Eles carregam as suites canônicas por referência. Nenhuma regra de negócio,
contrato, migration, scanner ou telemetria foi copiada para este bundle.

## Validações executadas

- suites canônicas do predecessor (`test_repository_integration.py` e
  `test_epic_005_automacao`): `PASS`, 7 testes;
- `py -3.12 -m pytest -q -p no:cacheprovider evidence/reviews/migrations-ci-secret-dependency-scan-e-telemetria-mini/story-0025/test_issue_0135_acceptance.py`:
  `PASS`, 2 testes;
- Ruff no teste de aceite: `PASS`;
- JSON parse, digests dos artefatos do candidato e ausência de drift em relação
  a `780f454`: `PASS`;
- `make verify PYTHON="py -3.12"`: executado conforme governança. Ruff, mypy,
  TypeScript, Vitest, Playwright, validação do repositório e reviews de
  arquitetura, requisitos, DDD, ADR, specifications, sprint e arquitetura
  Python passaram. O gate agregado encerrou no walking skeleton global porque
  `FOUNDATION_INTEGRATION=1` e os serviços PostgreSQL/RabbitMQ pinados não estão
  configurados nesta execução (`1 failed, 4 passed`); essa precondição não é
  alterada pelo diff somente de evidência.

## Independência, limites e risco residual

O Reviewer audita o commit produzido pela `ISSUE-0134`; esta evidência não
aprova a própria implementação da `ISSUE-0135`. A entrada de QA referencia o
mesmo candidato, evidence set e risco, mas permanece explicitamente pendente.
Nenhuma aprovação de QA é inventada ou inferida.

O único risco residual é `LOW`: os resultados de secret e dependency scan são
produzidos pela GitHub Actions hospedada. A auditoria local comprova o workflow
pinado, a composição fail-closed e os casos negativos, mas o merge ainda deve
exigir os checks hospedados do commit em revisão.

O diff é somente evidência executável. Não altera contrato, schema, estado
persistido, deployment ou runtime; migration não se aplica. O rollback é
reverter o commit de evidência da `ISSUE-0135`.
