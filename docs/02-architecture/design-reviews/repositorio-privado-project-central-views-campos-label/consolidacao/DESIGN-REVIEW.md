# Design Review — consolidação dos contratos da fundação de engenharia

## Escopo e decisão

`STORY-0006` consolida exclusivamente os contratos publicados por `STORY-0690`
e `STORY-0691`. Os dois slices pertencem a `BC-001`, usam as baselines
`SAR-v2.9-PHASE-F` e estão presentes juntos no commit imutável
`3d7581b07dacf84db0a55f53a0f30cf8ff9be372`.

A composição escolhida é lado a lado: o perfil
`ENGINEERING-FOUNDATION-CONFORMANCE` mantém os controles de fundação e o perfil
`WORKER-GOVERNANCE-CONFORMANCE` mantém TaskEnvelope e ciclo de vida do worker.
Não há merge de schemas, cópia de controles nem nova autoridade normativa.

## Rastreabilidade e compatibilidade

O contrato `engineering-foundation-slice-consolidation` fixa os paths e SHA-256
dos seis artifacts publicados pelos slices no baseline comum. A matriz
`ISSUE_REQUIREMENTS_REVIEW.csv` atribui dez requisitos a `ISSUE-0800` e dois a
`ISSUE-0801`; a união possui doze IDs, sem interseção, omissão ou duplicação.

Os IDs dos contratos, `$id` dos schemas, profiles e namespaces de controles são
distintos. A consolidação não altera os contratos congelados, OpenAPI, estado
persistido, banco, broker, runtime ou semântica geoespacial. Migration e rollback
operacional são `NOT_APPLICABLE`; rollback contratual é revert antes do consumo
ou supersessão por nova versão compatível.

## Limite da ISSUE-0116

Esta história congela a integração contratual que antecede a materialização. A
configuração operacional do repositório, Project, views, campos, labels, Issue
Forms, templates, ruleset e checks continua pertencendo às histórias downstream
já existentes `STORY-0692` a `STORY-0700`. Antecipar esses writes aqui violaria o
TaskEnvelope e duplicaria ownership; nenhuma nova Story ou prerequisite é criada.

## Gate independente e riscos residuais

O implementador entrega o candidate como `READY_FOR_INDEPENDENT_REVIEW` e não
libera dependentes. Somente `Reviewer` distinto do executor pode registrar riscos
residuais, vincular a revisão ao mesmo commit candidato e liberar os dependentes
derivados do grafo: `STORY-0008` e `STORY-0692` a `STORY-0700`.

Riscos para o Reviewer avaliar:

- os digests pinados exigem nova versão da consolidação se um slice congelado for
  legitimamente supersedido;
- a capacidade operacional ainda não é claim desta entrega e permanece sujeita
  aos testes, checks e restrições das histórias downstream;
- regras de proteção/rulesets dependem do plano e das capacidades disponíveis no
  provedor GitHub, sem reduzir os gates declarativos ou permitir fallback aberto.

O teste obrigatório `test_story_0006_slice_consolidation` valida schema, baseline,
lineage dos artifacts, cobertura, ausência de colisão, grafo e gate fail-closed.
