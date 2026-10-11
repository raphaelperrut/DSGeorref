# Controle de mudanças

- ADR exige autoria/aprovação arquitetural, aprovação do Product Owner e final review.
- Contratos públicos mudam por revisão de compatibilidade antes das lanes de implementação.
- Thresholds mudam somente por promoção baseada em corpus e evidência.
- Escopo de sprint/issue é controlado pelo Tech Lead; aceitação de produto pelo Product Owner.
- Mudança destrutiva de schema/artifact exige migration, janela de compatibilidade, rollback e restore.
- Somente fontes normativas e artefatos executáveis permanecem na documentação ativa; commits, tags e releases preservam mudanças.


<a id="issue-1026-owner-decision"></a>
## Registro administrativo da decisão consolidada — #1026

Fonte autoritativa: [decisão consolidada do Owner](https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6102594277).
Issue exclusiva: [#1026](https://github.com/raphaelperrut/DSGeorref/issues/1026).
Baseline de referência: `eb22e2e34d9080a6486851cc609b848df7871ae5`.

Este registro incorpora o ato já publicado, sem nova minuta ou solicitação de
autoridade. O comentário é de `raphaelperrut` (GitHub user ID `110496238`),
que declara exercer Project Owner, Product Owner, Arquiteto e Tech Lead.
Essa autoria verificável no GitHub registra a origem da decisão; não constitui
principal criptográfico, binding DAA ou autenticação do executor.

A decisão substitui as condições conflitantes dos comentários `6102463655`,
`6102496343` e `6102516141` somente quanto às condições de aprovação e
ao escopo ampliado pelo comentário `6102539043`.
As manifestações das competências acumuladas já constam do ato consolidado.
Não se exige sua repetição como se fossem pessoas diferentes.

### Modelo solo aprovado pelo Owner

Uma pessoa pode acumular competências de direção, produto, arquitetura e
liderança técnica formalmente atribuídas. ChatGPT/Codex são agentes técnicos,
sem independência humana. Executor, QA e Reviewer atuam em passes e contextos
distintos, com testes reais e avaliações rastreáveis sobre o mesmo SHA.
No regime solo, a ausência de independência pessoal deve ser declarada.

Aprovação humana autenticada pode representar competências acumuláveis.
Independência humana ou criptográfica expressamente exigida continua obrigatória.
ADR-058/ADR-059 e a política DAA/trust vigente conservam sua autoridade;
este registro não habilita regime DAA para outro TaskEnvelope.
A aplicação de gates acompanha desenvolvimento, integração e produção, sem
dispensar controles exigidos na etapa nem antecipar aprovação produtiva.

### Scope administrativo aprovado

A preparação e formalização normativa ficam limitadas a:

- `docs/02-architecture/adrs/ADR-006-prompts-permanentes-taskenvelope-e-precedencia-de-instrucoes.md`;
- uma única ADR sucessora, após atribuição legítima de ID e filename;
- `docs/00-governance/ROLE_AUTHORITY_MATRIX.md`;
- `docs/00-governance/CHANGE_CONTROL.md`;
- `docs/00-governance/ENGINEERING_OPERATING_MODEL.md`;
- `docs/00-governance/DEFINITION_OF_READY.md`;
- `docs/00-governance/DEFINITION_OF_DONE.md`;
- `GOVERNANCE.md`;
- `docs/00-governance/START_HERE.md`;
- `docs/00-governance/ADR_INDEX.csv`;
- `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`;
- `docs/02-architecture/sar/SAR-040-DECISION-REGISTER.md`;
- `tools/run_adr_review.py`;
- `tools/validate_repository.py`.

Os ajustes de inventário só acompanham registros legitimamente formalizados.
A decisão também permite preparar um único TaskEnvelope operacional da #1026
e os registros indispensáveis de autorização, evidência e checkpoint, após
identificação legítima dos IDs e destinos. O inventário numérico, isoladamente,
não atribui ID nem autoriza criar envelope com campos ou aprovações presumidos.

### Procedimento excepcional aprovado, condicionado à eficácia

A autoridade da diretriz é o Owner identificado na fonte acima. A atribuição
específica continua sob competência do Tech Lead; a conferência e o final
review respeitam a segregação funcional e os requisitos estritos aplicáveis.

1. Formalizar a única sucessora da ADR-006 em BC-001 e a reconciliação normativa
   mínima, conservando as decisões não substituídas, inclusive
   SharedPartialDeliveryGate. ADR-007 mantém allow/deny, isolamento, serialização
   e handoff. A formalização exige autoria/aprovação arquitetural, aprovação de
   produto e final review conforme o rito vigente; esta sessão executora não
   emite QA ou final review.
2. Registrar o ID legitimamente atribuído do único TaskEnvelope operacional,
   seu destino, executor e identidade real autenticada, papel, autoridade,
   scope, denies, testes e condições de parada. Não reutilizar TASK-0041.
3. Registrar separadamente cada etapa ordinária de atribuição, scope ou
   checkpoint inviabilizada pelos dois defeitos já reconhecidos na #1026,
   a autoridade responsável pela conferência e o resultado ordinário real.
   Substituir somente essas etapas; nenhuma falha ordinária recebe rótulo PASS.
4. Vincular a conferência excepcional à decisão eficaz e à autorização
   específica, aos bytes reais do envelope e dos artefatos, seus digests
   calculados, baseline, ancestralidade e candidato. As evidências equivalentes
   precisam demonstrar identidade, competência, integridade, allow/deny e
   ausência de colisão. O registro excepcional não se apresenta como checkpoint
   ordinário nem dispensa verificações não afetadas.
5. Somente após eficácia e autorização específica comprovadas, executar os
   reparos exclusivos nos três paths técnicos abaixo. Exigir casos positivos,
   negativos, denies e checkpoints, regressões pertinentes e `make verify`.
   QA e Reviewer avaliam o mesmo SHA em passes separados; PR, CI e merge humano
   permanecem sob os controles não excepcionados.

Scope técnico exclusivo:

- `.codex/policies/file-scopes.yaml`: alinhar `Architect` a `Arquiteto`, sem mudar permissões;
- `tools/governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/frz-gov-adr-gov-dec-parte-1/scope_validation.py`: aceitar envelopes operacionais legítimos em `.codex/tasks/operations/`;
- `tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_materialization.py`: verificar os reparos e controles preservados.

A exceção é de utilização única, exclusiva da #1026. Sua validade começa somente
com formalização eficaz e autorização específica verificável. Extingue-se
automaticamente após recuperação integrada e verificada, revogação ou abandono
formal, sem transferência, reutilização ou renovação tácita.
Não altera READY, DAA/trust, contratos de produto, EPIC-009 ou implementação
funcional da ISSUE-0151/#117. Não autoriza bypass permanente ou enfraquecimento
de deny-overrides-allow, inventário, integridade, checkpoints e fail-closed.

### Estado verificável deste registro

- `OWNER_SCOPE_APPROVAL = YES`, pela fonte consolidada;
- `SOLO_OPERATIONAL_MODEL = APPROVED_IN_PRINCIPLE`;
- `BOOTSTRAP_EXCEPTION = APPROVED_IN_PRINCIPLE / SUBJECT_TO_NORMATIVE_EFFECTIVENESS`;
- `NORMATIVE_CHANGE_EFFECTIVE = NO`;
- `TECHNICAL_PATCHES_AUTHORIZED = NO`;
- ID/filename da sucessora, TaskEnvelope, principal do executor, autorização
  específica e checkpoint excepcional: não formalizados por este registro;
- QA e final review do candidato: não emitidos por esta sessão.

A classificação prévia `NEW_ADR` está registrada em
`docs/02-architecture/sar/SAR-040-DECISION-REGISTER.md`, antes de qualquer
atribuição de identificador. O mecanismo vigente
`validate_classification_before_identifier`, em `decision_governance.py`,
rejeita a atribuição de ID a uma nova ADR com `IDENTIFIER_ALLOCATED_EARLY`
e não oferece neste boundary um caminho de reconhecimento de registro prévio.
O teste canônico `test_req_gov_dec_001` exige essa rejeição.
Esse controle não integra as etapas de atribuição/scope/checkpoint comprovadamente
defeituosas autorizadas para substituição e seu arquivo não pertence ao scope
técnico. Não é enfraquecido nem declarado satisfeito.

O limite da materialização administrativa é, portanto, o registro do ato aprovado
e da classificação anterior ao ID. A ausência de atribuição legítima da sucessora,
de envelope/autorização específicos e de final review impede declarar eficácia
ou iniciar os patches. Este registro conserva ADR-006 como autoridade vigente
e não modifica o inventário Accepted/Superseded.

## Decisão executiva emergencial eficaz para execução — #1026

Fonte: https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6103942173. Origem autenticada no GitHub: raphaelperrut, user ID 110496238,
obtida pelo conector autenticado. Competências acumuladas: Project Owner,
Product Owner, Arquiteto e Tech Lead. Candidato preservado: 19d5dd00064d03f581b45881a5db73ada8344a74;
branch exclusiva codex/issue-1026-control-plane-recovery.
Este ato autoriza execução supervisionada, com desvio declarado, e sucede os
impedimentos executivos anteriores, cujos registros são conservados como histórico.

Scope exato: arquivos normativos da decisão 6102594277, os três arquivos técnicos
daquela decisão, decision_governance.py pela ampliação 6103899107, uma ADR sucessora,
um TaskEnvelope operacional e os registros indispensáveis autorizados pela emergência.
Nenhuma norma fora desse scope, READY, DAA/trust, contrato, EPIC-009 ou código
funcional da #117 integra a execução.

Substituições documentadas: atribuição de ID, impedida por NEW_ADR não reconhecer
classificação prévia; ativação do envelope, impedida pela rejeição de operations;
formação/validação de checkpoint dependente desses mecanismos e do papel divergente.
Resultado substituído: MANUAL / DEVIATION_DECLARED; ORDINARY_GATE_PASS=NOT_CLAIMED.
Scope e checkpoint ordinários serão testados depois dos reparos; nenhum PASS é
presumido dessa substituição. Gates de integração, DAA, QA, final review e merge
não são substituídos.

A conferência usou inventário e Git reais, classificação prévia no commit 19d5dd00064d03f581b45881a5db73ada8344a74,
fonte autenticada, scope e denies explícitos. Atribuição manual ADR-060/TASK-0775
está registrada em SAR-040. Não há reuso de TASK-0041 ou de aprovação de outra tarefa.
O checkpoint administrativo é o SHA real de materialização, sem certificado
ordinário. Digests são calculados dos bytes Git e do envelope canônico.
O Executor é esta sessão Codex supervisionada pelo Owner; a origem humana é a
conta autenticada do ato. Nenhum principal criptográfico, binding ou assinatura
foi inventado, nem foi alegada independência pessoal.

EMERGENCY_EXECUTION_AUTHORIZED_BY_OWNER=YES;
NORMATIVE_CONFORMANCE=DEVIATION_DECLARED_PENDING_RECONCILIATION;
MERGE_AUTHORIZED=NO. A política ADR-060 é prospectiva após formalização e integração.
A sessão executora não emite QA/final review. QA/Reviewer separados avaliam o mesmo
SHA e a conformidade residual; integração exige decisão humana.
A exceção termina após recuperação integrada e validada ou revogação expressa,
sem reutilização. Rollback é reversão humana dos commits, mantendo a trilha.

## Relatório do candidato de recuperação — execução e desvio

Autoridade executiva: comentário 6103942173, corpo UTF-8 obtido pelo conector
com SHA-256 3599a77017239e2375e96823e6ea5575514b10ce132d1e047d9ba4a8cee54262; isso não é assinatura DAA.
Ancestral preservado: 19d5dd00064d03f581b45881a5db73ada8344a74.
Checkpoint administrativo real: 5eb0c5522365f27adbb159319c7a9abb3e1ab7ca.
TASK-0775 congelado: SHA-256 canônico d7d0ee005735bed5b33d5250cb5d659f5b3d60741e13c7d29f41f612dccf98a4.
Atribuição de ID, ativação do envelope e formação/validação de checkpoint foram
conferidas manualmente sob a exceção. Não recebem PASS automatizado retroativo.

Reparos: classificação prévia resolve registro SAR por Git/digest e exige anterioridade
à primeira adição do identificador; classifica ausências, posterioridade e adulteração
fail-closed. A policy só renomeia Architect para Arquiteto. Operations exige schema,
ID/filename coerentes, ausência de colisão canônica, role e checkpoint congelado;
preserva denies, ancestry e rejeição de mutação. Não há flag de bypass permanente.

Resultados reais: 36 testes focados PASS; oito validadores normativos/arquitetura
PASS; imports/erros Python dos módulos reparados PASS.
Regressão ampla: 9 PASS, 2 FAIL preexistentes (seleção 94/95 e data fixa de 2026-08-23),
interrompida pelo limite explícito de duas falhas. Reprodução no código histórico
do ancestral, com inputs inalterados e SHA histórico fixado, confirmou ambas.
DAA isolado: 3 PASS, 1 FAIL preexistente, expectativa que omite TASK-0738 do trust.
Nenhuma dessas assertions ou o trust foi alterado.

make verify terminou com exit 2, sem timeout e sem excluir targets.
Passaram qualidade Python, frontend, 77 delivery gates, oito validadores,
49 testes de licenciamento e o validador de foundation do monorepo.
Parou no teste que exige FOUNDATION_INTEGRATION=1 e serviços PostgreSQL/RabbitMQ:
falha ambiental real, sem flag artificial ou PASS global. Os targets posteriores
não foram executados. A interrupção Git anterior não se repetiu.
Runtime: CPython 3.12.13, Node 24.20.0 e pnpm 10.26.1; instalação pelo lock imutável.
Verificações Git limitadas a 20s; suítes limitadas a 240/300s e make a 600s.
Configuração Git byte-preserving para fixtures, sem alterar configuração do repo.

Conformidade residual: o verificador de owner/overlap sobre o ancestral retorna
OWNER_GATE_REQUIRED: a nova ADR não existia como autoridade Accepted naquela base.
O gate não foi enfraquecido nem declarado PASS; a emergência permite execução,
não conformidade ordinária integral. A direção ADR-060 é materializada sob o ato
do Owner, com integração prospectiva ainda dependente de avaliação explícita.
Nenhum binding/attestation DAA, QA, final review, READY ou merge foi emitido.
O módulo decision_governance.py tem 408 linhas, com revisão obrigatória pelo
padrão Python; os dois helpers adicionados têm 29/33 linhas e o módulo 19
definições top-level. A revisão separada deve abranger esse requisito.

Riscos: ausência de independência pessoal, desvio de bootstrap declarado,
OWNER_GATE_REQUIRED residual, regressões históricas e integração ambiental não
concluída. A integração continua bloqueada até os controles aplicáveis, avaliações
separadas no mesmo SHA e decisão humana. Nenhuma nova cadeia administrativa foi criada.
Rollback: reversão humana do commit técnico final e, se necessário, do checkpoint
5eb0c5522365f27adbb159319c7a9abb3e1ab7ca, preservando 19d5dd00064d03f581b45881a5db73ada8344a74, registros e evidências.
Não há migration, estado de produto ou alteração funcional da #117.

Os logs integrais ficam no diretório temporário dsgeorref-1026-validation-tools;
os resultados e digests abaixo são preservados neste registro versionado:
- focused: 1026-focused-1-attempt2.log; SHA-256 ea7c40dceca442770cc180a7c0bf9416cdffc99abdc7d1e197fc837255c78935; exit=0, timeout=False.
- normative: 1026-normative-1.log; SHA-256 c41fb8505e284d901df85e11a282c986c55c3990678d39f5ab8920d8fdfa2000; exit=0, timeout=False.
- normative: 1026-normative-2.log; SHA-256 f48889736bab128991fa356409bd825504e605c16af7598420bd600379fc0e24; exit=0, timeout=False.
- normative: 1026-normative-3.log; SHA-256 20d2be304bb0cf82dbf62b742a75a319a5c3ca719b721ad28ef4cecb154c641f; exit=0, timeout=False.
- normative: 1026-normative-4.log; SHA-256 b8eba27ee6b5eb4f5f727c066f866ae89400a0064484629710f9a3d81baaf734; exit=0, timeout=False.
- normative: 1026-normative-5.log; SHA-256 76439ec01a4a2cc01d68c47b2d01ad6b6a36d7737f7d1e54f11118b57d637984; exit=0, timeout=False.
- normative: 1026-normative-6.log; SHA-256 73e3364f4bc2414a818e4bc691f61e8413c3ebdaa6bf3a3bb977b523ed7caaf4; exit=0, timeout=False.
- normative: 1026-normative-7.log; SHA-256 599913df38a972474ede3b546e0aec389af752d40675ee1ab69fbae6d2ed90b5; exit=0, timeout=False.
- normative: 1026-normative-8.log; SHA-256 cdb36b0e1e4e8601839bd57923fa551c54ad44c61d1b960ffc6d36d7237826b7; exit=0, timeout=False.
- quality: 1026-quality-1-attempt2.log; SHA-256 a47ad41e8914addb3b14a8d4f259158474ddb580d4a5b510ed35efb3938bd21a; exit=0, timeout=False.
- regressions: 1026-regressions-1.log; SHA-256 43bc41c39cc8ca5907f7d4f9acc05d633d1150b90b3cd9969b0f92de4a41bfed; exit=1, timeout=False.
- daa: 1026-daa-1.log; SHA-256 d18ba2da25dc11284dc1db2c732160c4a40f01d315f122e67058d4af2589d2c1; exit=1, timeout=False.
- baseline: 1026-baseline-1.log; SHA-256 d2513712999e98731226804883ac36e73ccba9a5694e1245aaabfbb74278af10; exit=0, timeout=False.
- make: 1026-make-1.log; SHA-256 63a420cac73d233fed5f17c66e2f95e443c523cca7c8cce4b07beb90bef05925; exit=2, timeout=False.
- ADR owner/overlap: 1026-adr-conformance.log; SHA-256 9eddc86df19dbf72b9e284e95ecde1748dab33e412a0df2306be2fd4dcdc2292; OWNER_GATE_REQUIRED.


## Reconstrução autorizada da ancestralidade de integração — #1026

Fonte autenticada: https://github.com/raphaelperrut/DSGeorref/issues/1026#issuecomment-6113485169; raphaelperrut, GitHub user ID 110496238.
Digest SHA-256 do corpo UTF-8 obtido pelo conector: db1c10d82a9d246591a99d37acf68f91978d8d38cc78ef03e180231501a1ba67; não é assinatura DAA.
A decisão autoriza uma única reconstrução sobre origin/main be97cea01ea2a812e4206cfe0d446f5919b2a8dc,
reconstituição da anterioridade e um checkpoint substituto de TASK-0775.
O candidato original 8b8a97923bc573b08724a5aa9090f4b853417940, classificação
19d5dd00064d03f581b45881a5db73ada8344a74, checkpoint 5eb0c5522365f27adbb159319c7a9abb3e1ab7ca
e todos os registros históricos permanecem preservados, sem transferência de QA/Review.
Os IDs lógicos ADR-060/TASK-0775 serão rematerializados somente após conferência de
unicidade: main contém 59 ADRs e 774 envelopes únicos; maiores ADR-059/TASK-0774.
Não há outra ADR ou TaskEnvelope lógico, alteração funcional, DAA/trust, READY,
TASK-0041, push, PR ou merge nesta reconstrução. A nova classificação deve anteceder
a primeira adição da ADR; bytes/digests e checkpoint serão vinculados a commits reais.
A exceção administrativa permanece MANUAL / DEVIATION_DECLARED; não é PASS
ordinário retroativo. QA e Reviewer incrementais no novo SHA continuam obrigatórios.


### Correspondência verificável dos estados de integração

| Evidência original preservada | Substituta no histórico de integração |
|---|---|
| Baseline eb22e2e34d9080a6486851cc609b848df7871ae5, com artefatos TASK-0041 | origin/main be97cea01ea2a812e4206cfe0d446f5919b2a8dc, sem transplantar esses artefatos |
| Classificação 19d5dd00064d03f581b45881a5db73ada8344a74 | d1e62d26b5902e82dda5b96744ce5ac9e45fd65b |
| Blob SAR prévio 2b8c72b35bdb518f8cb5981d84ceeaed213d3d65843941c452cc99d2eaa59e22 | b848e98486728be4fd7b116a7ab80c6d9864fdf957b2a4069ba8dede773503dd |
| Checkpoint 5eb0c5522365f27adbb159319c7a9abb3e1ab7ca | bdae1d434e1e36373e58ef17305daef03cabfaff |
| TASK-0775, identidade lógica e bytes congelados | TASK-0775 no checkpoint substituto, mesmos bytes |
| Candidato 8b8a97923bc573b08724a5aa9090f4b853417940 | Commit final descendente do checkpoint substituto; SHA identificado pelo Git e relatório externo de validação |

Digest canônico recalculado de TASK-0775: d7d0ee005735bed5b33d5250cb5d659f5b3d60741e13c7d29f41f612dccf98a4.
Digest SHA-256 dos bytes Git do envelope: 607cb9aaff288cc3526d71c96802a22d757a5ff515778728535dbff573f4785f.
O congelamento deve ser verificado entre bdae1d434e1e36373e58ef17305daef03cabfaff e o candidato final.
A ADR-060 ativa referencia a classificação substituta e sua seção de integração;
os quatro metadados originais e todos os registros históricos foram preservados.

Diferenças permitidas contra o candidato original: CHANGE_CONTROL e SAR-040
recebem registros adicionais da reconstrução; ADR-060 substitui somente quatro
metadados de prova/baseline e preserva os originais; test_materialization deriva
classificação/checkpoint do histórico real, mantém as assertions e adiciona a
conferência checkpoint→HEAD. Policy, validadores técnicos e demais arquivos
permanecem byte a byte idênticos. Não há alteração funcional adicional.

Os resultados históricos acima pertencem ao histórico original. Verificações
reproduzidas deste candidato são registradas em logs novos com SHA real, comandos,
exits e hashes, sem sobrescrever logs anteriores. Não constituem QA ou Final Review.
O desvio histórico OWNER_GATE_REQUIRED não recebe PASS retroativo; a verificação
prospectiva usa o checkpoint substituto. Exceção de formação do checkpoint é
MANUAL / DEVIATION_DECLARED sob 6113485169; controles automatizados reparados
devem ser executados e classificados pelo resultado real.

QA e Reviewer incrementais devem avaliar o mesmo novo SHA, as quatro diferenças
de evidência, anterioridade, unicidade, frozen envelope, scope/denies, conservação
de SharedPartialDeliveryGate/ADR-007/DAA, testes negativos e riscos residuais.
Nenhuma aprovação anterior é transferida; não há push, PR ou merge autorizado.
