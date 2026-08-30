# Design Review — consolidação dos contratos OpenAPI e runtime

## Escopo e decisão

`STORY-0016` consolida exclusivamente os contratos publicados por `STORY-0701`
e `STORY-0702`. Ambos pertencem a `BC-001`, usam a baseline
`SAR-v2.9-PHASE-F` e estão presentes no commit imutável
`94d72f3b324ea48891597e0db4cebdf78676f999`.

A composição preserva a extensão ordenada já declarada: o profile
`RUNTIME-SCHEMA-CONFORMANCE` estende o artifact publicado por
`OPENAPI-CONTRACT-FOUNDATION-CONFORMANCE`. Nenhum schema filho é mesclado,
copiado ou reescrito e nenhuma segunda autoridade normativa é criada.

## Rastreabilidade e compatibilidade

O contrato `openapi-runtime-slice-consolidation` fixa paths e SHA-256 dos sete
artifacts publicados, incluindo o checkpoint obrigatório de compatibilidade de
schemas. A matriz `ISSUE_REQUIREMENTS_REVIEW.csv` atribui dez requisitos à
`ISSUE-0811` e cinco à `ISSUE-0812`; a união possui quinze IDs sem interseção,
omissão ou duplicação.

Os IDs de contrato, `$id` dos schemas, profiles e controles são distintos. A
relação `extends` do segundo manifest referencia o exemplo congelado do primeiro
slice, e o checkpoint mantém OpenAPI, banco, eventos, manifests e artifacts em
categorias explícitas. A consolidação não altera OpenAPI, contratos de domínio,
estado persistido, banco, broker, runtime ou semântica geoespacial.

## Limite da ISSUE-0126

Esta história congela a integração contratual que antecede a materialização.
Implementação de OpenAPI, cliente TypeScript, CLI, jobs, eventos e artifacts
permanece nas histórias downstream já existentes `STORY-0018` e `STORY-0703` a
`STORY-0705`. Antecipar esses writes violaria o TaskEnvelope e duplicaria
ownership; nenhuma Story ou prerequisite nova é criada.

Migration e rollback operacional são `NOT_APPLICABLE`, pois não há mudança de
schema persistido ou runtime. O rollback contratual é revert antes do consumo ou
supersessão por nova versão; contratos congelados nunca são sobrescritos.

## Gate independente e riscos residuais

O candidato permanece `READY_FOR_INDEPENDENT_REVIEW`; o implementador não libera
dependentes. Somente `Reviewer` distinto pode registrar riscos residuais no mesmo
commit candidato e liberar os quatro nós derivados do DAG.

Riscos para avaliação independente:

- digests pinados exigem nova versão se um slice congelado for supersedido;
- o contrato prova composição e rejeição fail-closed, não runtime, geração do
  cliente ou E2E das histórias descendentes;
- o checkpoint registra majors suportadas, mas não autoriza fallback, bypass de
  compatibilidade nem reinterpretação dos contratos por superfície.

O teste `test_story_0016_slice_consolidation` valida schema, baseline, ancestry,
lineage, checkpoint, cobertura, ausência de colisão, DAG e gate fail-closed.

## TaskEnvelope

O TaskEnvelope foi corrigido somente para incluir seu próprio arquivo, registry
de ownership, teste focado e evidence já exigida. A correção mantém o control
plane separado e não amplia data plane ou requisitos.
