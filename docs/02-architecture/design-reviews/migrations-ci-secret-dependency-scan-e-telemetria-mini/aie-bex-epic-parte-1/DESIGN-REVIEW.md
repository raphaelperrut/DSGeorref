# Design review — Migrations, CI e observabilidade mínima

- **Candidate:** `ISSUE-0816` / `STORY-0706` / `TASK-0706`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; QA e revisão independente pendentes
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela o menor profile declarativo que torna verificáveis os dez requisitos
atribuídos à ISSUE-0816. Ele não implementa runtime, migration, CI, scanner, exporter ou
backend de telemetria. Essa materialização permanece nas histórias executáveis do EPIC-005.

O profile referencia contratos existentes de `FailureDiagnostic`, `Job`, `Attempt`,
`ProcessingPlan`, readiness e versionamento/rollback sem alterá-los. Nenhum endpoint, tabela,
estado, evento, taxonomia concreta de produto ou parâmetro científico novo é definido.

## Contrato publicado

`contract-foundation.schema.json` define dez controles fail-closed:

1. falha clássica e elegibilidade neural são tipadas, versionadas e apoiadas em evidência;
2. checkpoints e artifacts somente são reutilizados quando canônicos e compatíveis;
3. cada veredito de imagem é preservado e o agregado admite `partially_succeeded`;
4. retry técnico permanece distinto de nova tentativa algorítmica versionada;
5. schema PostgreSQL evolui apenas por migration versionada, com preflight e rollback;
6. a primeira fatia processa uma imagem ponta a ponta com forma compatível com lote;
7. `ProcessingPlan` é persistido, imutável, versionado e explicável;
8. readiness exige evidência por estágio e canary sintético, inclusive no modo offline;
9. aceite e evidência derivam de contratos e mudança exige revisão explícita;
10. telemetria usa OpenTelemetry, backend substituível e correlação até `ArtifactSet`, sem
    substituir PostgreSQL como autoridade.

O schema rejeita campos ausentes, controles desconhecidos e valores permissivos. O manifest
liga cada requisito ao teste canônico e enumera as falhas cobertas.

## Failure modes e hardening

A suíte negativa rejeita classificação ou elegibilidade implícita, reuso sem compatibilidade,
perda de veredito, retry ambíguo, migration implícita, expansão da primeira fatia, plano
inválido, readiness sem evidência/canary, aceite sem contrato e quebra silenciosa de correlação
ou exporter. Referências de contrato, ownership e contenção do TaskEnvelope também são
validadas.

## Compatibilidade e ownership

O contrato segue SemVer. Adição opcional compatível pode usar a major atual. Remoção,
renomeação, relaxamento de invariante, mudança de authority ou alteração incompatível exige
nova major e revisão do Arquiteto. Manifest, schema e exemplo são registrados em
`CONTEXT_CONTRACT_OWNERSHIP.csv` com owner `BC-001`.

## Impacto, riscos e rollback

- **Control plane:** novo manifest, schema, exemplo, registry, teste, evidence e esta revisão.
- **HTTP:** readiness é somente referenciada; nenhum endpoint ou schema congelado mudou.
- **Banco/migration:** requisito e rollback são congelados declarativamente; nenhuma migration
  física ou tabela foi criada neste slice.
- **Runtime/CI/scanners/IA/telemetria:** nenhuma implementação operacional foi criada.
- **Risco residual:** os testes provam contrato e rejeição fail-closed, não execução real das
  histórias descendentes, disponibilidade de exporters ou migration em banco vivo.
- **Rollback:** antes de consumo, reverter o candidato. Depois de consumo pinado, preservar a
  versão histórica e publicar sucessora; schema físico segue rollback antes de `contract` ou
  forward fix/restore coordenado depois desse ponto.
- **Review:** QA sentinela e Reviewer independentes permanecem pendentes no mesmo commit.

## TaskEnvelope

O TaskEnvelope foi corrigido somente para incluir seu próprio arquivo, o registry de ownership,
o teste focado e a evidence já exigida pela issue. A correção mantém control plane separado e
não amplia data plane, threat model ou requisitos.
