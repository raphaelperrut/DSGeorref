# Design review — OpenAPI contract foundation conformance

- **Candidate:** `ISSUE-0811` / `STORY-0701` / `TASK-0701`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; QA e revisão independente pendentes
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela o menor profile declarativo que torna verificáveis os dez requisitos
atribuídos à ISSUE-0811. Ele não implementa cliente TypeScript, frontend, API, CLI, worker,
persistência ou migration. A materialização de runtime permanece nas histórias descendentes
do EPIC-004.

O profile referencia, sem alterar, o OpenAPI 3.1 congelado, o schema de `ProcessingPlan`, o
Problem Details e o profile de fundação já publicado pelo `BC-001`. Nenhum endpoint, estado
de produto, tabela, transição concreta, capability ou parâmetro científico novo é definido.

## Contrato publicado

`contract-foundation.schema.json` define dez controles fail-closed:

1. coordenadas externas declaram CRS, eixos, unidade e precisão; adapters usam `always_xy`;
2. JSONB serve somente à extensibilidade versionada e não substitui invariantes relacionais;
3. estados são tipados e somente transições registradas são aceitas;
4. cliente gerado do OpenAPI exige gates de componente, acessibilidade e E2E;
5. a primeira fatia processa exatamente uma imagem ponta a ponta com contrato batch-compatible;
6. `ProcessingPlan` é persistido, imutável, versionado e explicável pelo schema existente;
7. CLI, API e worker são adapters finos sobre application services compartilhados;
8. erros tipados mapeiam para o Problem Details versionado, sem fallback genérico;
9. o cliente TypeScript deriva exclusivamente do OpenAPI e usa diff gate determinístico;
10. registry local e versionado não contorna autorização, compatibilidade ou quality gates.

O exemplo positivo contém todos os controles. Objetos desconhecidos, campos ausentes e
valores permissivos são rejeitados pelo JSON Schema Draft 2020-12 e por testes negativos.

## Reuso e ausência de autoridade duplicada

Os controles de `REQ-RUN-001`, `REQ-RUN-006`, `REQ-RUN-008` e `REQ-RUN-010` reproduzem a
published language de `ENGINEERING-FOUNDATION-CONFORMANCE`; os testes exigem igualdade
estrutural com esse profile. `ProcessingPlan`, Problem Details e OpenAPI são referenciados
por path e validados diretamente, sem copiar seus payloads ou relaxar contratos congelados.

## Failure modes e hardening

O manifest liga cada requisito ao teste canônico e enumera as falhas rejeitadas. A suíte
cobre CRS inválido ou sem normalização, JSONB permissivo, estado/transição desconhecido,
gate de frontend ausente, expansão implícita da primeira fatia, plano inválido, namespace
divergente, erro genérico, cliente manual e capability fail-open. Também rejeita controle
ausente ou desconhecido e verifica registro de ownership e contenção do TaskEnvelope.

## Compatibilidade e ownership

O contrato segue SemVer. Adição opcional compatível pode usar a major atual. Remoção,
renomeação, relaxamento de invariante, mudança de authority ou alteração incompatível exige
nova major e revisão do Arquiteto. Manifest, schema e exemplo são registrados em
`CONTEXT_CONTRACT_OWNERSHIP.csv` com owner `BC-001`.

## Impacto, riscos e rollback

- **Control plane:** novo manifest, schema, exemplo, registry, teste, evidence e esta revisão.
- **HTTP:** referenciado e inalterado; nenhum endpoint ou schema congelado mudou.
- **Banco/migration:** não aplicável; o requisito de persistência é declarativo neste slice.
- **Runtime/frontend/Geo/IA:** nenhuma implementação foi criada.
- **Risco residual:** os testes provam contrato e rejeição fail-closed, não o comportamento
  operacional das histórias descendentes nem performance, acessibilidade real ou E2E real.
- **Rollback:** antes de consumo, reverter o candidato. Depois de consumo pinado, preservar
  a versão histórica e publicar sucessora; sobrescrita é proibida.
- **Review:** QA sentinela e Reviewer independentes permanecem pendentes no mesmo commit.

## TaskEnvelope

O TaskEnvelope foi corrigido somente para incluir seu próprio arquivo, o registry de
ownership, o teste focado, a evidence já exigida e as referências normativas diretamente
validadas. A correção mantém control plane separado e não amplia data plane ou requisitos.
