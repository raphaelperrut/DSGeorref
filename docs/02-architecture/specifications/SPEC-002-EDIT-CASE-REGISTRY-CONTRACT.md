# SPEC-002 — Edit Case Registry Contract

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-011`
- **ADRs governantes:** `ADR-024`, `ADR-048`, `ADR-025`
- **Bounded Contexts:** `BC-011`, `BC-012`, `BC-013`
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Propósito

O Edit Case Registry é a autoridade do ciclo de vida de uma correção humana ou assistida. Ele resolve a lacuna entre um Edit Bundle imutável e a necessidade operacional de rascunhar, revisar, aprovar, aplicar, validar, aceitar, rejeitar, superseder ou reverter uma correção. O registry não altera imagens ou resultados anteriores; ele coordena novas Attempts e snapshots.

## 2. Aggregate e autoridade

`EditCase` é o aggregate root. `EditBundle`, `ReviewDecision`, `RollbackPlan` e eventos são entidades ou value records subordinados. O contexto de Revisão e Correção é owner da intenção e do workflow; Georreferenciamento executa a nova tentativa; Verificação Geométrica decide aceitação científica; Resultados publica a visão; Artifacts guarda bundles e evidence.

## 3. Identidade e concorrência

`case_id` é UUID estável. `revision` cresce monotonicamente e é usado para optimistic concurrency. Comando com revisão antiga retorna conflito e não é aplicado. Cada bundle tem identidade própria e versão inteira. A mesma operação não pode ser reescrita; correção produz nova revisão.

## 4. Subject

O subject pode ser resultado de imagem, componente relativo ou mosaico. Ele referencia IDs, nunca paths. O `base_result_snapshot_id` fixa a visão sobre a qual a edição foi preparada. Se a base deixar de ser corrente antes da aplicação, o case volta para revisão ou exige rebase explícito; merge automático é proibido.

## 5. Edit Bundle

O bundle é uma lista ordenada de operações tipadas. Operações mínimas cobrem GCPs, anchors, máscaras, metadata override e notas. Cada operação tem ID idempotente, target, payload e rationale. Ordem é significativa e faz parte do hash. Operações desconhecidas são rejeitadas, não ignoradas.

## 6. Estados

Os estados são `DRAFT`, `IN_REVIEW`, `CHANGES_REQUESTED`, `APPROVED`, `APPLYING`, `APPLIED`, `VALIDATING`, `ACCEPTED`, `REJECTED`, `ROLLED_BACK`, `SUPERSEDED` e `CANCELLED`. O arquivo `edit-case-state-machine.yaml` é a tabela executável. Transição ausente é proibida.

## 7. Workflow

Um case nasce em DRAFT, recebe bundle válido, é submetido, passa por quorum, é aprovado e aplicado sob lease. Aplicação cria Attempt e candidate snapshot. A validação obrigatória executa SGV e validadores de artifacts. Somente PASS leva a ACCEPTED. Falha leva a REJECTED com diagnósticos. O lote principal não é bloqueado por cases de revisão.

## 8. Review Decision

Cada decisão registra actor, revisão, horário, rationale e condições. Decisão em revisão diferente é inválida. Quorum e segregação de funções são políticas versionadas. O autor pode revisar quando a política permitir, mas casos de alto risco exigem reviewer independente.

## 9. Aplicação

`APPLY` é idempotente por case/revision. Uma lease com fencing impede aplicação simultânea. O executor lê base e bundle imutáveis, cria uma nova Attempt, materializa inputs e nunca altera a Attempt original. Falha parcial é contida e registrada; artifacts em staging não são publicados.

## 10. Validação

Validação inclui schema, geometria, cobertura, incerteza, provenance, SGV, COG e integridade dos manifests aplicáveis. O registry armazena somente o status e referências; os relatórios pertencem aos contexts responsáveis. Nenhum reviewer pode sobrepor hard gate do SGV.

## 11. Aceitação

ACCEPTED significa que o candidate snapshot passou todos os gates e foi publicado de forma atômica. Ele se torna a visão corrente por uma operação transacional explícita. O snapshot anterior permanece disponível, com lineage e razão da substituição.

## 12. Rejeição

REJECTED é terminal para a revisão. Nova tentativa de correção cria novo case ou nova revisão antes de aplicação, conforme a fase. Diagnósticos são imutáveis. Rejeição não apaga bundle ou artifacts.

## 13. Rollback

Rollback não muta o snapshot aceito. Um `RollbackPlan` identifica origem, alvo, motivo, impact preview e aprovação. Executar rollback cria nova visão corrente apontando para snapshot já validado ou rematerializado de forma compatível. A operação é auditada e reversível por novo case, não por edição retroativa.

## 14. Supersession

Um case aceito pode ser SUPERSEDED somente por successor aceito. O vínculo é explícito e acíclico. Cases em rascunho podem ser cancelados. Histórico continua consultável.

## 15. Event log

Cada transição produz evento append-only com event hash, case revision e actor. O estado corrente pode ser persistido como projection, mas o event log e registros imutáveis permitem auditoria. Reprocessar evento deve ser idempotente; ordem é protegida pela revisão.

## 16. Versionamento de schema

Schemas seguem SemVer. Campo opcional compatível é minor; alteração de estados, significado ou operação obrigatória é major. Leitores preservam histórico de majors suportadas. Writers usam a versão pinada. Migrações não reescrevem eventos originais.

## 17. Compatibilidade de bundles

Um bundle declara schema e base snapshot. Executor verifica support antes da aplicação. Bundle de major desconhecida é armazenável, mas não aplicável. Operação depreciada pode ser lida durante janela e convertida por adapter versionado, com evidence.

## 18. Segurança e autorização

Comandos exigem política central. Criar, revisar, aprovar, aplicar e rollback são permissões distintas. Payloads são validados e limitados. Referências não podem escapar do projeto. Dados de auditoria não contêm secrets.

## 19. Idempotência

Comandos mutáveis usam idempotency key persistida. Repetição retorna o mesmo resultado. Eventos e outbox possuem deduplication key. O mesmo bundle não cria duas Attempts para a mesma revisão.

## 20. Erros

Códigos mínimos: `EDIT_CASE_NOT_FOUND`, `REVISION_CONFLICT`, `INVALID_TRANSITION`, `BUNDLE_INVALID`, `BASE_SNAPSHOT_STALE`, `REVIEW_QUORUM_MISSING`, `APPLICATION_LEASE_LOST`, `VALIDATION_FAILED`, `ROLLBACK_NOT_ALLOWED`, `SUBJECT_SCOPE_MISMATCH` e `UNSUPPORTED_SCHEMA`.

## 21. Artefatos

Edit Bundle, impact preview, diff preview, review decision, validation reports, application receipt e rollback receipt são artifacts tipados por `SPEC-005`. Paths e hashes nunca aparecem como autoridade de estado fora do manifest.

## 22. API e eventos

A API expõe commands e queries sem permitir update arbitrário do aggregate. Eventos publicados usam outbox. Consumers não inferem estado por nome de evento; usam versão e schema. O registry não expõe tabela interna.

## 23. Observabilidade

Métricas por estado, tempo de revisão, falha de aplicação e validação usam baixa cardinalidade. Traces ligam case, Attempt e ResultSnapshot por IDs. Rationale e payload não são labels.

## 24. Testes

A suíte cobre todas as transições válidas, cada transição inválida, concorrência, idempotência, base stale, falha antes/depois do staging, lease loss, SGV fail, rollback e supersession. Property tests verificam que estado terminal não retorna a estado mutável.

## 25. Critérios de aceite

- state machine é única e executável;
- cada mudança gera evento e revisão;
- aplicação cria nova Attempt;
- SGV permanece autoridade;
- rollback não reescreve histórico;
- schemas e exemplos validam;
- conflitos e ciclos são rejeitados;
- artifacts possuem manifest e lineage.

## 26. Condições de parada

A implementação para se o tipo de edição não estiver especificado, se houver dúvida de autoridade, se uma transição estiver ausente, se o rollback exigir mutação histórica, se o bundle não tiver schema/hash ou se a aplicação pretender contornar revalidação completa.
