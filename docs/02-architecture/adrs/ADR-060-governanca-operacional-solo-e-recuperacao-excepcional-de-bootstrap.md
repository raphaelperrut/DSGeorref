# ADR-060 — Governança operacional solo e recuperação excepcional de bootstrap

- **Status:** `Accepted`
- **Baseline:** `#1026 / d1e62d26b5902e82dda5b96744ce5ac9e45fd65b`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-060`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

- **Substitui:** `ADR-006`
- **Issue:** `#1026`
- **Decisão do Owner:** `https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6103942173`
- **Registro prévio de classificação:** `{"path":"docs/02-architecture/sar/SAR-040-DECISION-REGISTER.md","source_revision":"d1e62d26b5902e82dda5b96744ce5ac9e45fd65b","sha256":"b848e98486728be4fd7b116a7ab80c6d9864fdf957b2a4069ba8dede773503dd"}`
- **Seção prévia de classificação:** `Registro prévio de integração — recuperação #1026`
- **Autoridade da classificação:** `https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6113485169`

## Correspondência da prova de classificação — integração #1026

A classificação original e seus metadados são evidência histórica, sem reescrita
de sua origem. A referência ativa acima aponta para o registro de integração
com anterioridade Git real, sob a decisão 6113485169. Não há novo ID lógico,
alteração de decisão funcional, PASS retroativo ou transferência de QA/Review.
Metadados originais preservados:

    - **Baseline:** `#1026 / 19d5dd00064d03f581b45881a5db73ada8344a74`
    - **Registro prévio de classificação:** `{"path":"docs/02-architecture/sar/SAR-040-DECISION-REGISTER.md","source_revision":"19d5dd00064d03f581b45881a5db73ada8344a74","sha256":"2b8c72b35bdb518f8cb5981d84ceeaed213d3d65843941c452cc99d2eaa59e22"}`
    - **Seção prévia de classificação:** `Registro prévio à atribuição de ID — recuperação #1026`
    - **Autoridade da classificação:** `https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6102594277`

## Contexto

Esta ADR isola uma decisão arquitetural de alto impacto e alto custo de reversão. Ela substitui agrupamentos amplos da baseline anterior e possui responsabilidade normativa exclusiva sobre o boundary descrito no título.

## Decisão

- Cada papel do Codex possui prompt permanente versionado, responsabilidades, condições de parada e handoff.
- Cada execução usa TaskEnvelope tipado que referencia história, requisitos, ADRs, contratos, testes, evidências e dependências.
- A precedência é: políticas do repositório, ADRs/contratos, TaskEnvelope, história e instrução local; contradição interrompe a execução.
- Prompts não podem introduzir requisito, endpoint, estado ou decisão ausente da baseline normativa.

- Uma pessoa humana pode acumular competências formalmente atribuídas de produto,
  arquitetura, liderança técnica e decisão humana de integração.
- Executor, QA e Reviewer atuam em passes e contextos distintos sobre o mesmo SHA.
  A independência pessoal no regime solo é ausente e declarada.
- Uma manifestação humana autenticada pode representar competências acumuláveis.
  Sessões Codex não são pessoas ou principais criptográficos independentes.
- Independência estrita e DAA permanecem sob ADR-058/ADR-059 e seu trust vigente;
  esta ADR não emite bindings nem amplia políticas assinadas.
- Desenvolvimento, integração e produção exigem os gates aplicáveis em cada etapa.

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

`ADR-001`, `ADR-003`, `ADR-007`, `ADR-059`

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


## Eficácia e compatibilidade histórica

A direção foi aprovada pelo ato executivo https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6103942173.
A execução da #1026 decorre desse ato, com desvio declarado, não de PASS ordinário.
A política solo é prospectiva após formalização e integração humana. QA e final
review do candidato continuam pendentes. ADR-006 permanece referência histórica
em snapshots, requisitos, contratos e matrizes congelados, sem reinterpretação.
Seu boundary é sucedido prospectivamente pela ADR-060; refinamentos são herdados.

## Exceção de utilização única — #1026

O ato declara que não havia mecanismo emergencial previamente vigente.
Autoriza conferência manual documentada de atribuição de identificador, ativação
do envelope e formação/validação de checkpoint somente quando bloqueados pelos
defeitos comprovados. Resultado: MANUAL / DEVIATION_DECLARED, sem PASS automatizado.
A origem humana é raphaelperrut, GitHub user ID 110496238, obtida pelo conector
autenticado. Nenhum principal criptográfico, binding ou assinatura foi fabricado.

A conferência real encontrou 59 ADRs contínuas e 774 envelopes únicos, incluindo
nove operacionais. Por delegação executiva expressa foram atribuídos ADR-060 e
TASK-0775, livres e posteriores aos maiores IDs observados ADR-059/TASK-0774.
A classificação NEW_ADR já estava no commit 19d5dd00064d03f581b45881a5db73ada8344a74, anterior à atribuição.
O procedimento é manual; nenhuma autoridade automática é declarada.

TASK-0775 é o único envelope operacional da #1026. STORY-0688/EPIC-001/SPRINT-001
são sua linhagem existente do control plane, sem nova história ou autorização
de executar a história de linhagem. Não reutiliza TASK-0041 ou outra autorização.
O checkpoint administrativo será o SHA real do commit de materialização, com
digest canônico real do envelope e ancestralidade desde o candidato preservado.
A conferência mantém scope, denies, inventário, integridade e congelamento do
envelope. O scope técnico tem somente os quatro arquivos expressamente aprovados.

READY, DAA/trust, contratos, código funcional da #117 e gates de integração não
são alterados. Executor não emite QA/final review nem faz merge.
A exceção termina com recuperação integrada e validada ou revogação expressa;
não pode ser reutilizada em outra issue, branch ou implementação.
Rollback é reversão humana dos commits, preservando a trilha e os digests.
Não há mudança de estado de produto, migrations ou promessa de produção.

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
