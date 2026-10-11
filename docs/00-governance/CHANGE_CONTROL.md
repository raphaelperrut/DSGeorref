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
