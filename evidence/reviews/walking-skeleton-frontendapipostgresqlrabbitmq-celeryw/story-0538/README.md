# ISSUE-0648 — auditoria final do EPIC-086

Este diretório é o locator canônico permitido pelo `TASK-0538` para a evidência
versionada da `STORY-0538`. O diff materializa somente auditoria executável; não
altera contratos, código de produção nem suites predecessoras.

## Alvo e decisão da revisão

- candidato revisado: `94c073428be1e8bbe49d078767651ec9237594b7`;
- tree do candidato: `095d8195a77d2ad78266fc938c37f9b43d1897f9`;
- merge que integrou o predecessor: `21e7b73d3e6e75ab9d18eaf098e8ec22db7ffdc3`;
- implementação revisada: `ISSUE-0647` / GitHub `#51` / PR `#954`;
- Reviewer: `PASS` para o candidato acima;
- QA independente: `PASS` para o mesmo candidato, evidence set e riscos.

O `REVIEW_EVIDENCE.json` fixa SHA, tree e SHA-256 canônico dos cinco blobs
alterados pelo candidato. O teste confere os digests contra o worktree com
finais de linha normalizados e diretamente contra os blobs Git, impedindo
reutilização da auditoria após drift entre plataformas. A árvore do candidato
é idêntica à árvore do merge em `main`.

## Evidência por critério

| Critério | Evidência | Resultado |
|---|---|---|
| `AC-ISSUE-0648-01` | contrato congelado, runner determinístico e `foundation-ci/verify-foundation` com PostgreSQL 18.4 e RabbitMQ 4.3.4 no SHA exato | PASS |
| `AC-ISSUE-0648-02` | 14 requisitos resolvidos aos checkpoints canônicos; slices, consolidação, automação e integração validados | PASS |
| `AC-ISSUE-0648-03` | mutações de contrato, fallback, publicação em erro, timeout, output malformado, escrita indevida, drift de scope/SHA/digest e coordenação ambígua | PASS |
| `AC-ISSUE-0648-04` | QA e Reviewer independentes registram `PASS` no mesmo candidato, evidence set e riscos; aprovação implícita é rejeitada | PASS |

Os entrypoints públicos obrigatórios são:

- `test_epic_086_aceite_happy_path`;
- `test_epic_086_aceite_negative_paths`.

Eles reutilizam as suites owner por subprocessos isolados. Nenhuma regra de
produto, persistência, mensageria, artifact ou cutover foi copiada para este
bundle. O E2E que exige serviços não é inferido do relatório de integração: a
auditoria o vincula ao `foundation-ci` bem-sucedido do PR `#954`, cujo
`headRefOid` é exatamente o candidato revisado.

## Validações

- suite de integração da `ISSUE-0647`: `PASS`, 6 testes;
- contrato, slices, conclusão, consolidação e automação: `PASS`,
  respectivamente 3, 7, 7, 1 e 8 testes na QA independente;
- runner direto: `PASS`, exit code zero, 14 requisitos e fluxo completo;
- sentinelas obrigatórias desta issue: `PASS`, 2 testes;
- Ruff direcionado, mypy strict da integração, JSON/digests e
  `git diff --check`: `PASS`;
- `make verify`: Ruff, mypy, frontend, governança, arquitetura, requisitos,
  DDD, ADR, especificações, sprint, arquitetura Python, licença e o validator
  da fundação passaram; o gate parou antes do E2E porque
  `FOUNDATION_INTEGRATION` está ausente e PostgreSQL/RabbitMQ não estão
  disponíveis localmente. O mesmo gate passou no CI hospedado do candidato
  exato com ambos os serviços pinados.

## Independência, limites e riscos residuais

O Reviewer e a QA auditam o commit produzido pela `ISSUE-0647`; esta evidência
não aprova o próprio diff da `ISSUE-0648`. O PR desta issue continua sujeito a
revisão independente antes de merge. Não há review GitHub no PR `#954`, e seu
merge não é usado como substituto para a QA independente registrada aqui.

O gate de fundação permanece `PENDING_PR_MERGE` e fail-closed; nenhuma primeira
fatia funcional é autorizada por este commit isoladamente. Os riscos residuais
`LOW` são a indisponibilidade local dos serviços pinados, mitigada pelo CI no
SHA exato, e a necessidade já contratada de executar as suites dos dois slices
em processos isolados devido ao nome top-level compartilhado
`foundation_expectations`.

O teste novo de integração da `ISSUE-0647` ainda não integra `make verify`; este
bundle o executa explicitamente. O warning de escopo default do
`pytest-asyncio` e a diferença entre Python local 3.12.10 e o pin 3.12.13 do CI
são preexistentes e não bloqueantes.

## Contratos, migration e rollback

Impacto em contrato, schema, estado persistido, deployment e runtime: `NONE`.
Migration e rollback de dados não se aplicam. O rollback é reverter o commit de
evidência da `ISSUE-0648`; PostgreSQL permanece autoritativo para estado e
RabbitMQ/Celery permanece somente transporte.
