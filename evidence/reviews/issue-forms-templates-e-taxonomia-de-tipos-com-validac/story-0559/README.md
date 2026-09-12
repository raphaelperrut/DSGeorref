# ISSUE-0669 — auditoria final do EPIC-090

Este diretório é o locator canônico permitido pelo `TASK-0559` para a evidência
versionada da `STORY-0559`. O diff materializa somente auditoria executável; não
altera contratos, implementação, automação nem testes predecessores.

## Alvo e decisão da revisão

- candidato revisado: `a3f0364ecedac56cde0dd76787970b987c8de41b`;
- tree do candidato: `9c577a32ee9ab3dddcc23c759304915d8fcc4139`;
- merge que integrou o predecessor: `6e3748dfd26f89b6345b6b2442091602420530bd`;
- implementação revisada: `ISSUE-0668` / GitHub `#56` / PR `#959`;
- Reviewer: `PASS` para o candidato acima;
- QA automatizada independente: `PASS` para o mesmo candidato, conjunto de
  evidências e riscos residuais.

O `REVIEW_EVIDENCE.json` fixa SHA, tree e SHA-256 canônico dos cinco blobs
alterados pelo candidato. O teste confere os digests contra o worktree com
finais de linha normalizados e diretamente contra os blobs Git. A árvore do
candidato é idêntica à árvore do merge em `main`.

## Evidência por critério

| Critério | Evidência | Resultado |
|---|---|---|
| `AC-ISSUE-0669-01` | contrato congelado, quatro Issue Forms, registry, validadores read-only e integração executável no SHA exato | PASS |
| `AC-ISSUE-0669-02` | `REQ-GOV-002` é resolvido ao checkpoint final `test_epic_090_integracao` e ao teste canônico do contrato | PASS |
| `AC-ISSUE-0669-03` | campos ausentes, tipos desconhecidos, bypasses, fallback permissivo, report malformado, timeout e drift de scope são rejeitados | PASS |
| `AC-ISSUE-0669-04` | QA automatizada e Reviewer registram `PASS` no mesmo candidato, evidence set e riscos; aprovação implícita é rejeitada | PASS |

Os entrypoints públicos obrigatórios são:

- `test_epic_090_aceite_happy_path`;
- `test_epic_090_aceite_negative_paths`.

Eles reutilizam os checkpoints owner por subprocessos isolados. Nenhuma regra
de governança é copiada para este bundle.

## Validações

- contrato, fundação, automação e integração: `PASS`, 14 testes focados;
- runners diretos de automação e integração: `PASS`, JSON determinístico e
  fail-closed;
- checks hospedados `epic-090-issue-form-governance`,
  `epic-090-issue-form-controls` e `foundation-ci`: `SUCCESS` no SHA candidato;
- sentinelas obrigatórias desta issue: cobrem o happy path e os negative paths;
- Ruff direcionado, JSON/digests e `git diff --check`: fazem parte do handoff
  do commit desta auditoria.

## Independência, limites e riscos residuais

O Reviewer audita o commit produzido pela `ISSUE-0668`; esta evidência não
aprova o próprio diff da `ISSUE-0669`, que continua sujeito a revisão
independente antes de merge. A QA é executada por GitHub Actions, autoridade
distinta do Reviewer, no mesmo SHA candidato.

Os dois riscos residuais são ambientais e `LOW`: no sandbox Windows local o
teste preexistente de automação não consegue materializar sua árvore temporária
por restrição de filesystem, e o E2E de fundação requer PostgreSQL/RabbitMQ não
disponíveis localmente. A suíte passa fora do sandbox e o gate completo passa
no GitHub Actions do SHA exato. Não há risco arquitetural aberto.

## Contratos, migration e rollback

Impacto em contrato, schema, estado persistido, deployment e runtime: `NONE`.
Migration e rollback de dados não se aplicam. O rollback é reverter o commit de
evidência da `ISSUE-0669`.
