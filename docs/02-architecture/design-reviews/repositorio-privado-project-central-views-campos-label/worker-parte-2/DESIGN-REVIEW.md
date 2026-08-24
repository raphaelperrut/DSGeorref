# Design review — worker governance conformance

- **Candidate:** `ISSUE-0801` / `STORY-0691` / `TASK-0691`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; revisão independente pendente
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela uma policy de conformidade para os dois requisitos atribuídos à
ISSUE-0801. Ele não implementa worker, scheduler, endpoint, persistência ou ferramenta de
fault injection. O data plane continua pertencendo às histórias descendentes e aos seus
bounded contexts.

O contrato referencia o schema existente `.codex/tasks/TASK_ENVELOPE.schema.json` em vez
de duplicar sua autoridade. Para o lifecycle, ele consolida somente as invariantes já
publicadas: readiness verifica dependências, drain recusa trabalho novo e reconcilia work
units, shutdown é cooperativo, e retomada aceita apenas checkpoints compatíveis.

## Contrato e falhas explícitas

`worker-governance-conformance.schema.json` é fail-closed: objetos desconhecidos são
rejeitados e cada decisão normativa usa valor constante. O manifest liga os controles aos
testes canônicos e enumera falhas de versão/conteúdo do TaskEnvelope, readiness sem prova,
drain permissivo, abandono no shutdown, checkpoint incompatível, cenário de fault
injection ausente e fallback silencioso.

Os cenários obrigatórios cobrem perda de dependência durante readiness, drain com trabalho
em andamento, shutdown durante work unit e retomada com checkpoint incompatível. Nenhum
timeout, threshold, fila, estado persistido ou estratégia de retry novo é definido.

## Compatibilidade e ownership

O contrato segue SemVer e JSON Schema Draft 2020-12. Adição opcional compatível pode usar
a major atual. Remoção, renomeação, relaxamento ou mudança de authority exige nova major e
revisão do Arquiteto. Os três artefatos estão registrados em
`CONTEXT_CONTRACT_OWNERSHIP.csv` com owner `BC-001`.

## Impacto, risco e rollback

- **Control plane:** novo contrato declarativo, manifest, exemplo, registry, testes e esta
  revisão.
- **Data plane:** nenhuma mudança; não há runtime, HTTP, banco, broker ou migration.
- **Risco residual:** os testes provam contrato e rejeição fail-closed, não o comportamento
  operacional dos workers; essa materialização permanece nas histórias descendentes.
- **Rollback:** antes de consumo, reverter o candidato. Depois de consumo pinado, preservar
  a versão histórica e publicar uma sucessora; sobrescrita é proibida.
- **Review:** QA e Reviewer independentes permanecem pendentes no mesmo commit candidato.

## TaskEnvelope

O TaskEnvelope foi corrigido somente para incluir seu próprio arquivo de controle, o
registry de ownership, o teste obrigatório e a evidence já declarada. A correção não
amplia data plane, dependências ou requisitos.
