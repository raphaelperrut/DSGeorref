# Design review — Runtime and schema conformance

- **Candidate:** `ISSUE-0812` / `STORY-0702` / `TASK-0702`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; QA e revisão independente pendentes
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela o menor profile declarativo que torna verificáveis
`REQ-RUNTIME-008`, `REQ-SCM-001`, `REQ-TOOL-003`, `REQ-TOP-001` e `REQ-UX-002`.
Ele estende o profile da primeira parte da capacidade e não implementa API, CLI,
frontend, registry em runtime, persistência, migration ou algoritmo.

OpenAPI, `ProcessingPlan`, `QualityReport` e `FailureDiagnostic` são referenciados sem
alteração. Nenhum endpoint, tabela, estado, evento, capability concreta, parâmetro
científico ou janela quantitativa de compatibilidade foi criado.

## Contrato publicado

`runtime-schema-conformance.schema.json` define cinco controles fail-closed:

1. frontend, API e CLI preservam semântica sobre application services compartilhados;
2. schemas de banco, API, eventos, manifests e artifacts entram em registry versionado
   com matriz de readers/writers e janela de majors declarada por contrato;
3. FastAPI e Pydantic permanecem no adapter HTTP fino, governado por OpenAPI 3.1;
4. capabilities compõem o `ProcessingPlan` versionado sem modos duplicados;
5. `ProcessingPlan`, `QualityReport` e `FailureDiagnostic` preservam versão publicada.

O exemplo positivo contém todos os controles. Campo ausente, propriedade desconhecida,
semântica por superfície, major não registrada, framework fora do adapter, capability
duplicada e bypass de gate são rejeitados.

## Reuso e autoridade

O controle de superfícies é verificado contra `application_boundaries` do profile
`OPENAPI-CONTRACT-FOUNDATION-CONFORMANCE` já congelado no mesmo ownership. O profile
novo referencia os contratos canônicos e não copia seus payloads. O OpenAPI commitado
continua sendo a fonte do transporte; os schemas de domínio continuam sendo a fonte dos
artifacts. Este slice publica política de conformidade, não uma segunda autoridade de
runtime ou domínio.

## Compatibility window

A janela não recebe tamanho inferido. Cada contrato declara explicitamente as majors
suportadas por readers; writers emitem apenas a major corrente registrada. Major fora da
lista é erro terminal `UNKNOWN_SCHEMA_MAJOR`, sem warning ou fallback. Mudança breaking
exige nova major e revisão do Arquiteto.

## Failure modes e hardening

O manifest liga cada requisito ao teste canônico e enumera falhas rejeitadas. A suíte
valida o JSON Schema Draft 2020-12, o exemplo, o OpenAPI 3.1, os três schemas de artifacts,
o `uniqueItems` de `ProcessingPlan`, o round-trip canônico, o ownership registry e a
contenção do TaskEnvelope. Testes negativos cobrem controle ausente/desconhecido,
semântica best-effort, janela implícita, major desconhecida, adapter permissivo, modo
duplicado e bypass de gate científico.

## Impacto, riscos e rollback

- **Control plane:** novo manifest, schema, exemplo, registry, teste, evidence e esta revisão.
- **Contratos existentes:** referenciados e inalterados; nenhum frozen contract foi reescrito.
- **HTTP:** OpenAPI 3.1 referenciado e inalterado; nenhum endpoint mudou.
- **Banco/migration:** não aplicável; registry e compatibilidade são declarativos neste slice.
- **Runtime/frontend/Geo/IA:** nenhuma implementação foi criada.
- **Risco residual:** a suíte prova contrato e rejeição fail-closed; implementação operacional,
  geração do cliente e E2E permanecem nas histórias descendentes do `EPIC-004`.
- **Rollback:** antes de consumo, reverter o candidato. Depois de consumo pinado, preservar a
  versão histórica e publicar sucessora; sobrescrita é proibida.
- **Review:** QA e Reviewer independentes permanecem pendentes no mesmo commit candidato.

## TaskEnvelope

O TaskEnvelope foi ajustado somente para incluir seu próprio arquivo, o registry de
ownership, o teste focado, a evidence já exigida e os contratos diretamente validados.
A correção mantém control plane separado e não amplia data plane ou requisitos.
