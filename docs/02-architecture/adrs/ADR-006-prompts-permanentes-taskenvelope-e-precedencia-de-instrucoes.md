# ADR-006 — Prompts permanentes, TaskEnvelope e precedência de instruções

- **Status:** `Accepted`
- **Baseline:** `SAR v2.8 — Fase E`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-006`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Cada papel do Codex possui prompt permanente versionado, responsabilidades, condições de parada e handoff.
- Cada execução usa TaskEnvelope tipado que referencia história, requisitos, ADRs, contratos, testes, evidências e dependências.
- A precedência é: políticas do repositório, ADRs/contratos, TaskEnvelope, história e instrução local; contradição interrompe a execução.
- Prompts não podem introduzir requisito, endpoint, estado ou decisão ausente da baseline normativa.

## Invariantes

- nenhuma implementação pode criar uma segunda autoridade para este boundary;
- parâmetros quantitativos permanecem em Application Profiles ou Benchmark Profiles;
- detalhes locais e reversíveis pertencem a issues, contratos ou código;
- contradição entre esta ADR e outro artifact interrompe a execução até reconciliação pelo Arquiteto.

## Alternativas consideradas

- manter a decisão agregada em uma ADR ampla: rejeitado por ocultar drivers, trade-offs e owners independentes;
- delegar a escolha à implementação: rejeitado por permitir divergência entre agentes e superfícies;
- transformar parâmetros reversíveis em ADR: rejeitado; profiles e benchmarks continuam sendo os owners desses valores.

## Racional da seleção

A opção selecionada reduz ambiguidade, limita o espaço de inferência dos agentes, permite auditoria independente e mantém um único owner normativo para uma decisão material.

## Consequências e trade-offs

- aumenta o número de ADRs e a disciplina de rastreabilidade;
- reduz o tamanho de cada contexto decisório e o risco de implementações redundantes;
- mudanças futuras precisam identificar exatamente qual boundary será substituído;
- integração entre decisões ocorre somente pelas dependências declaradas abaixo.

## Dependências arquiteturais

`ADR-001`, `ADR-003`

## Gate de mudança

Mudança que altere a autoridade, tecnologia estrutural, formato público, trust boundary, modelo de consistência ou direção de dependências deste boundary exige ADR substituta. Ajustes compatíveis e reversíveis seguem profiles, contratos e issues.

## Verificação de conformidade

- validators devem confirmar referência a IDs existentes e sequência contínua;
- histórias e TaskEnvelopes devem listar esta ADR quando modificarem o boundary;
- contratos, migrations, testes e evidence aplicáveis devem ser versionados no mesmo commit candidato;
- nenhuma decisão aberta pode ser completada por inferência do implementador.

## Rastreabilidade SAR

- **Requisitos owned:** `REQ-GOV-002`, `REQ-GOV-003`, `REQ-GOV-005`, `REQ-GOV-ADR-002`, `REQ-GOV-ADR-018`, `REQ-GOV-DEC-001`, `REQ-GOV-DEC-002`, `REQ-ISM-002`, `REQ-ISM-003`, `REQ-ISM-004`, `REQ-ISM-005`, `REQ-ISM-007`, `REQ-ISM-008`, `REQ-ISM-009`, `REQ-ISM-010`, `REQ-WORKER-001`
- **Épicos relacionados:** `EPIC-001`, `EPIC-002`, `EPIC-014`, `EPIC-039`, `EPIC-086`, `EPIC-090`, `EPIC-092`, `EPIC-110`
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`
- **Revisão:** `docs/07-assurance/PHASE-D-ADR-REVIEW-REPORT.md`


## Especificações normativas — Fase E

Este boundary é concretizado por `SPEC-001`, `SPEC-004`. Texto, schemas, exemplos e validadores dessas especificações são obrigatórios. Divergência bloqueia implementação e exige reconciliação pelo Arquiteto.

<a id="owner-decision-shared-partial-delivery"></a>
## Owner Decision — SharedPartialDeliveryGate

Decisão do Project Owner aprovada: `OPTION_A — SharedPartialDeliveryGate`,
`CANONICAL_GATE_MODEL_APPROVED`; refinamento `REFINE_EXISTING` de ADR-006 / BC-001.
Esta seção materializa a autorização recebida para a ISSUE-0148 / ISSUE-0848,
sem criar outra autoridade normativa. Sequenciamento: SAR-120.

TaskEnvelope 1.7.0 estende 1.6.0 aditivamente: `delivery_gate_dependencies` é opcional
(ausência = lista vazia); `delivery_gate_scope` identifica entrega parcial do owner
por `gate_id` e `definition_sha256`. No snapshot de aprovação, exige também
`acceptance_manifest_sha256`. `dependencies` permanece exclusivamente igual aos
predecessores Story→Story; o registry não altera esse grafo nem conclui a Story owner.

O registry canônico é `docs/06-delivery/DELIVERY_GATES.json`, validado por seu schema
2020-12 fechado. Satisfação é derivada de definição vigente, outputs, checks PASS,
AcceptanceManifest, snapshot do envelope, aprovação independente pelo verifier DAA
existente e IntegrationReceipt com integração humana verificável na baseline exigida.
Não existe campo autoral de satisfação. Gate desconhecido, inválido ou pendente
bloqueia READY/execução do consumer, mas pendência não invalida o planejamento.

Autoriza-se somente `DG-TASK-0738-A`: fundação técnica compartilhada de BC-016 / EPIC-031,
executada por TASK-0738 no SPRINT-002, sem dependências funcionais de Story para essa
etapa. Os outputs, checks e paths autorizados constam de SAR-120 e TASK-0738.
Stage B preserva escopo, requisitos e dependência STORY-0185 no SPRINT-009.
STORY-0038 / TASK-0038 preserva STORY-0036 e seu write scope exclusivo de identidade,
consumindo a fundação integrada sem recriá-la.

ADR-013/014 permanecem autoridades da fundação. A seleção de gerador cabe ao Tech Lead
com Frontend como detalhe local e reversível compatível com ADR-013; escolha material
exige decisão adicional. Este passe não seleciona ferramenta nem executa Stage A.
Não altera contratos HTTP, autoridade/trust DAA ou ownership de requisitos.
