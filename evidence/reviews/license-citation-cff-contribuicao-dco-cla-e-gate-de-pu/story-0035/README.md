# ISSUE-0145 — auditoria final do EPIC-007

Este diretório é o locator canônico permitido pelo `TASK-0035` para a evidência
versionada da `STORY-0035`. Ele materializa a evidência obrigatória sem alterar
contratos, código de produção ou suites predecessoras.

## Alvo da revisão

- implementação revisada: `8cd5884ec495b6e23a57d22eccba25e30a7d6d53`;
- merge que integrou o predecessor: `dbe1341abae1bddeecd82d28de2f93f15182f2d4`;
- issue implementadora: `ISSUE-0144` / GitHub `#46`;
- resultado do Reviewer: `PASS` para o candidato acima.

`REVIEW_EVIDENCE.json` fixa os SHA-256 dos blobs Git canônicos dos cinco arquivos
alterados pelo candidato. O teste de aceite confirma os digests tanto no
worktree com finais de linha normalizados quanto nos blobs do commit revisado,
impedindo reutilização da auditoria após drift entre plataformas.

## Evidência por critério

| Critério | Evidência |
|---|---|
| `AC-ISSUE-0145-01` | relatório de integração determinístico, contratos versionados, artifacts públicos e `test_epic_007_aceite_happy_path` |
| `AC-ISSUE-0145-02` | digests do candidato e rastreio explícito de `REQ-CIT-001`, `REQ-EPIC-042`, `REQ-OSS-001` e `REQ-PUB-002` |
| `AC-ISSUE-0145-03` | mutações de contrato/automação, relatórios predecessores falhos ou malformados, timeout, drift de ownership/SHA/digest e aprovação implícita |
| `AC-ISSUE-0145-04` | QA e Reviewer referenciam o mesmo SHA, evidence set e risco residual; QA independente concluiu `PASS` |

Os entrypoints públicos obrigatórios são:

- `test_epic_007_aceite_happy_path`;
- `test_epic_007_aceite_negative_paths`.

Eles carregam as suites canônicas por referência. Nenhuma regra de licença,
citação, contribuição, DCO/CLA ou publicação foi copiada para este bundle.

## Validações executadas

- suites canônicas do EPIC-007 e teste sentinela desta issue: `PASS`, 2 testes;
- Ruff no teste de aceite: `PASS`;
- parse do JSON, blobs/digests do candidato e ausência de drift: `PASS`;
- `make verify`: executado uma vez por exigência de `AGENTS.md`; Ruff, mypy e
  TypeScript passaram, mas o gate parou quando o worker Vitest não iniciou por
  `spawn EPERM`. O host usa Node 22.14.0 e o repositório exige Node 24.20.0;
  trata-se de falha ambiental fora do diff somente de evidência. O gate local
  não foi repetido.

## Independência, limites e risco residual

O Reviewer audita o commit produzido pela `ISSUE-0144`; esta evidência não
aprova a própria implementação da `ISSUE-0145`. A decisão independente de QA
referencia o mesmo candidato, evidence set e risco e conclui `PASS`. Nenhuma
aprovação de publicação é inventada ou inferida.

O gate de publicação permanece `BLOCKED` e fail-closed. A auditoria não declara
prontidão para distribuição e não substitui as evidências de release candidate,
DCO, revisão jurídica, segurança, licenças, restore, compatibilidade ou ciência.

O risco `LOW` registrado no handoff do Reviewer era a decisão independente de
QA ainda pendente. A decisão `PASS` para o mesmo candidato resolve esse risco
sem alterar o gate de publicação.

O diff é somente evidência executável. Não altera contrato, schema, estado
persistido, deployment ou runtime; migration não se aplica. O rollback é
reverter o commit de evidência da `ISSUE-0145`.
