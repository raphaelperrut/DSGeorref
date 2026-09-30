# Auditoria de implementação — ISSUE-0797 / GitHub #72 / STORY-0687

## Binding e baseline

- Task: `TASK-0687`; épico: `EPIC-110`; incremento: `EVIDENCE_ONLY`.
- Branch: `codex/issue-0797-final-audit`.
- Base limpa, igual a `origin/main` após fetch: `0b9ca097baa603c05d50c63592e96f20c690297b`.
- Predecessor `STORY-0686`: commit `c3371e67aedbc53c2a33596653464cdbb84dc69f`,
  ancestral da base, integrado pelo merge `43481e5`; GitHub #71 fechado.
- Inspeção de lanes: um checkout ativo em `git worktree list`, nenhuma PR aberta
  em `gh pr list --state open`; nenhum diff prévio ou colisão observada.
- `CANDIDATE_SHA: CONTAINING_COMMIT`. O SHA candidato é o commit que introduz
  este arquivo, informado no handoff; não é o SHA da base. Nenhum SHA é embutido
  no próprio commit. Inspecionar com `git show <candidate-sha>:evidence/reviews/governanca-continua-do-backlog-e-decomposicao-de-epico/story-0687/FINAL_AUDIT.md`.
- QA e Reviewer devem fazer checkout desse mesmo SHA e repetir o comando abaixo,
  usando este artifact e estes riscos. Alterações posteriores invalidam o binding
  para aprovação; evidência de candidato revisado é append-only.

Ponto inicial: [evidência da STORY-0686](../../../implementation/epic-110/story-0686/IMPLEMENTATION_EVIDENCE.md).
Os predecessores são fontes versionadas, sem promoção automática de suas aprovações.

| Fonte preservada | SHA-256 do blob Git na base/candidato (LF) |
|---|---|
| `evidence/implementation/epic-110/story-0686/IMPLEMENTATION_EVIDENCE.md` | `b9fbc226c45839fb32a985337934b09089a4fbd4ae320088844bdb0a3bb7789b` |
| `contracts/contexts/engineering_governance/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/contract-manifest.yaml` | `a4d8174217b98193eb3b4ba82e22600682850da7fa0904defabaa3b368b0531c` |

## Testes e validações

Comando autoritativo, repetido no commit candidato antes do handoff:

```powershell
.venv/Scripts/python.exe -B -m pytest -q -s -p no:cacheprovider tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/aceite/test_final_acceptance.py
```

| Teste obrigatório | Resultado | Provas existentes delegadas |
|---|---|---|
| `test_epic_110_aceite_happy_path` | PASS | `3 passed`: `test_epic_110_integracao`, `test_epic_110_automacao`, `test_epic_110_contrato`. |
| `test_epic_110_aceite_negative_paths` | PASS | `18 passed`: cinco diagnósticos de input inválido/ausente, regressão 6/6 determinística, rejeição 6/6 pelo sentinela de contrato, nove controles fail-open, rejeição de controle ausente/propriedade desconhecida/owner errado e incompatibilidade de versão/propriedades. |

Resultado externo: `2 passed`. O sentinela usa o mesmo interpretador/checkout,
exige exit code zero dos nodes explícitos e propaga stdout/stderr em falhas.
Fixtures temporárias são isoladas; nenhum validador, regra ou assertion upstream
é copiado ou enfraquecido. A integração também verifica inputs ausentes,
determinismo e ausência de escrita.

- Validações focadas: JSON do envelope e igualdade de allow/deny/evidence com
  `phase_f_review`, deny paths preservados, Ruff lint/format do único Python novo
  e `git diff --check`: `PASS`.
- Tentativa inicial no sandbox: dois erros de setup por `PermissionError` no
  diretório temporário do pytest, antes de qualquer assertion. Execução
  autoritativa fora do sandbox: `PASS`.
- Gate global obrigatório, executado uma vez: `make verify PYTHON=.venv/Scripts/python.exe`.
  Resultado: `EXECUTED_WITH_PREEXISTING_ENVIRONMENT_FAILURE` (exit code 1).
  Ruff/mypy, frontend typecheck/Vitest/Playwright, validação do repositório,
  reviews A–F, arquitetura Python, licença/contribuição (6 testes) e validador
  monorepo passaram. A suíte monorepo teve `1 failed, 5 passed`, parando em
  `test_walking_skeleton_end_to_end_and_vertical_slice_definition_of_done`
  (`tests/fnd/monorepo-greenfield-com-cli-api-web-minimos-e-checks-r/test_foundation.py:67`):
  `FOUNDATION_INTEGRATION` ausente. O teste exige flag e PostgreSQL/RabbitMQ
  fixados e parou antes de tentar os serviços. O arquivo é idêntico à base;
  a mesma limitação consta na evidência da STORY-0686. Gates posteriores não
  executados; nenhuma falha de assertion do diff. Status dos reviews automáticos
  não é aprovação independente deste candidato.

## ACs e rastreabilidade

| Critério | Resultado da implementação | Evidência objetiva no candidato |
|---|---|---|
| `AC-ISSUE-0797-01` | PASS | Happy path observa contrato congelado `1.0.0`, owner `BC-001`, referências/ownership válidos e relatório `PASS`, `FAIL_CLOSED`, `READ_ONLY`, zero findings; integração chama a consolidação dos slices existentes. |
| `AC-ISSUE-0797-02` | PASS | Consolidação verifica cobertura exata dos 53 requisitos do épico, 53 testes/control keys únicos, outputs/scopes disjuntos, policies e merges ancestrais. As seis fontes abaixo preservam os bindings requisito→teste; a story não possui requisito exclusivo (`DERIVED_CONTROL`). |
| `AC-ISSUE-0797-03` | PASS | Negative path rejeita ausência/corrupção de inputs, fallback silencioso, mapeamento ausente, contrato ausente e duplicidade 6/6, com exit code 1, diagnóstico acionável e snapshots inalterados nos testes de CLI; schema rejeita owner/versão/propriedades e controles fail-open. |
| `AC-ISSUE-0797-04` | READY — aprovação pendente | Binding único acima, comandos, evidências e riscos comuns abaixo. `QA_INDEPENDENT=PENDING`, `FINAL_REVIEW=PENDING`; nenhum gate humano aprovado ou autoaprovação. |

Fontes dos bindings já versionados, todas verificadas por
`test_story_0684_slice_consolidation`, chamado pelo happy path:

| História / quantidade | Requisitos | Fonte exata do mapping |
|---|---|---|
| STORY-0683 / 5 | REQ-ISM-004, REQ-ISS-002, REQ-PLN-009, REQ-PRJ-004, REQ-SPRINT-001-004 | `contracts/contexts/engineering_governance/fnd/governanca-continua-do-backlog-e-decomposicao-de-epico/contract-manifest.yaml` → `requirements` e `proof.required_tests` |
| STORY-0754 / 10 | REQ-ISM-001, REQ-ISM-002, REQ-ISM-003, REQ-ISM-005, REQ-ISM-007, REQ-ISM-008, REQ-ISM-009, REQ-ISM-010, REQ-ISS-001, REQ-ISS-003 | `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/ism-iss-parte-1/foundation-policy.json` → `requirement_evidence` |
| STORY-0755 / 10 | REQ-ISS-004, REQ-PLN-001, REQ-PLN-002, REQ-PLN-003, REQ-PLN-004, REQ-PLN-005, REQ-PLN-006, REQ-PLN-007, REQ-PLN-008, REQ-PLN-010 | `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/iss-pln-parte-2/foundation-policy.json` → `requirement_evidence` |
| STORY-0756 / 10 | REQ-PRJ-001, REQ-PRJ-002, REQ-PRJ-003, REQ-PRJ-005, REQ-PRJ-006, REQ-PRJ-007, REQ-PRJ-008, REQ-PRJ-009, REQ-PRJ-010, REQ-PRM-001 | `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prj-prm-parte-3/foundation-policy.json` → `requirement_evidence` |
| STORY-0757 / 10 | REQ-PRM-002, REQ-PRM-003, REQ-PRM-004, REQ-PRM-005, REQ-PRM-006, REQ-PRM-007, REQ-PRM-008, REQ-PRM-009, REQ-PRM-010, REQ-SPRINT-001-001 | `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/prm-sprint-001-parte-4/foundation-policy.json` → `requirement_evidence` |
| STORY-0758 / 8 | REQ-SPRINT-001-002, REQ-SPRINT-001-003, REQ-SPRINT-001-005, REQ-SPRINT-001-006, REQ-SPRINT-001-007, REQ-SPRINT-001-008, REQ-SPRINT-001-009, REQ-SPRINT-001-010 | `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/sprint-001-parte-5/foundation-policy.json` → `requirement_evidence` |

As evidências da STORY-0683, STORY-0684 e STORY-0685 permanecem em
`evidence/implementation/epic-110/story-0683/IMPLEMENTATION_EVIDENCE.yaml`,
`evidence/implementation/epic-110/story-0684/IMPLEMENTATION_EVIDENCE.md` e
`evidence/operations/epic-110/story-0685/IMPLEMENTATION_EVIDENCE.md`.
Esta execução verifica sua integração e os bindings; não repete as 48 suítes
dos slices nem afirma execução runtime ou reconciliação remota de GitHub Project.

## Diff e contenção

| Arquivo alterado | Justificativa |
|---|---|
| `.codex/tasks/TASK-0687.json` | Correção administrativa autorizada: único local de evidence dentro do escopo da story, autorização do próprio envelope e apenas do arquivo sentinela omitido; espelhos da Fase F consistentes. |
| `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/aceite/test_final_acceptance.py` | Materializa somente os dois testes obrigatórios, delegando a executáveis existentes. |
| `evidence/reviews/governanca-continua-do-backlog-e-decomposicao-de-epico/story-0687/FINAL_AUDIT.md` | Único artifact de auditoria/handoff e resultados, vinculado ao containing commit. |

O path `evidence/reviews/epic-110/story-0687/` foi substituído nos dois campos
do envelope pelo path canônico da story; não existe evidência duplicada.
Todos os deny scopes permanecem intactos (`src/**`, `contracts/**`, `tests/**`
e paths de produção orientados por épico/issue). A exceção administrativa é
somente `.codex/tasks/TASK-0687.json`; não autoriza outro control plane.
Não há novo requisito, prerequisite, primitive, checker de produção, registry,
contrato, camada, ADR ou regra de produto. `NEW_PREREQUISITE_CREATED=NO`.

## Limitações, riscos e próximo gate

- `CONTRACT_IMPACT=NONE`: contrato congelado apenas consumido; nenhuma mudança
  em API, schema, evento, persistência, estado, runtime ou deployment.
- `MIGRATION_ROLLBACK=NOT_APPLICABLE`: somente evidence, sentinela e ajuste
  administrativo; revert do incremento não exige migração ou ação operacional.
- `BLOCKER_FINDINGS=NONE`; `HIGH_FINDINGS=NONE`; nenhuma stop condition aberta.
- `ARCHITECTURAL_RISK_OPEN=NONE` dentro deste incremento EVIDENCE_ONLY.
- MEDIUM/LOW não bloqueante: completar o gate global em ambiente de integração
  fixado; warning de Node local `22.14.0` versus pin `24.20.0`; STORY-0756 tem
  policy/suíte/merge e `prj-prm-parte-3/HANDOFF.md` versionados, mas não possui
  arquivo separado no diretório de evidence do seu envelope (limitação já
  registrada na STORY-0684). Nenhum desses itens amplia esta issue.
- Prova limitada ao control plane versionado, sem claims novos de custo, escala,
  latência, segurança, RPO/RTO ou operação de serviços externos.
- QA independente e Review final: `PENDING`, ambos sobre o containing commit,
  este mesmo artifact e os riscos acima. `AC_04_IMPLEMENTATION_EVIDENCE=READY`;
  aceite independente de AC-04 ainda pendente. `READY_FOR_QA=YES`.
