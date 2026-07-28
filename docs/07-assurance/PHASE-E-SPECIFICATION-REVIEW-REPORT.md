# Fase E — Specification Review Report completo

- **Baseline:** `SAR v2.8`
- **Data da revisão:** `2026-07-27`
- **Resultado:** `APROVADO`
- **Pendências bloqueantes:** `0`
- **Decisões arquiteturais abertas:** `0`
- **Implementação de produção:** `BLOCKED_EXTERNAL`

## 1. Objetivo

A Fase E transformou conceitos arquiteturais ainda insuficientemente especificados em contratos executáveis. O foco não foi aumentar documentação por volume, mas impedir que implementadores ou agentes preencham lacunas de formato, ciclo de vida, ordem de operações, publicação ou compatibilidade por inferência. Cada especificação combina texto normativo, schema ou protocolo machine-readable, exemplos válidos, vetores negativos, ownership DDD, versionamento, regras de mudança e validador.

A revisão preservou as 57 ADRs definitivas. Nenhuma nova ADR foi criada, porque as decisões estruturais já existiam: a lacuna era de especificação. Os documentos da Fase E concretizam boundaries de ADRs existentes e passam a ocupar a hierarquia normativa entre ADRs e TaskEnvelopes.

## 2. Escopo auditado

| Elemento | Quantidade |
|---|---:|
| Especificações congeladas | 5 |
| Framework de especificações | 1 |
| Arquivos de contrato | 139 |
| JSON Schemas | 44 |
| Exemplos executáveis | 8 |
| TaskEnvelopes reconciliados | 758 |
| ADRs preservadas | 57 |
| Bounded Contexts | 16 |
| Requisitos cobertos | 376 |
| Histórias implementáveis | 758 |

## 3. Resultado geral

Todos os cinco tópicos solicitados foram promovidos a status `FROZEN`. O status significa que uma implementação pode começar somente usando as versões declaradas, sem alterar semântica localmente. Mudança breaking exige major version e revisão do Arquiteto. Os contracts são owned por Bounded Context e estão inventariados em `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`.

A Fase E também atualizou o TaskEnvelope para a versão 1.4. Cada tarefa agora declara `applicable_specifications`, `specification_review_status=PASS` e `specification_baseline=SAR-v2.8-PHASE-E`. O campo impede que um agente implemente uma história sem saber quais contratos devem governar a mudança.

## 4. SPEC-001 — Prompt Bundle Contract

O Prompt Bundle deixou de ser uma coleção informal de prompts. A especificação define source, fragments, inheritance, composition order, input/output contracts, runtime policy, integrity e signatures. JSON é a forma canônica; YAML é uma superfície autoral restrita que deve mapear sem ambiguidade para JSON.

O documento possui 7474 palavras, extensão equivalente a aproximadamente vinte páginas conforme diagramação. Ele cobre:

- estrutura JSON e YAML;
- SemVer independente para schema e conteúdo;
- canonicalização determinística;
- SHA-256 para fragment, payload, lock e prompt resolvido;
- assinatura Ed25519 e trust store;
- inheritance DAG, diamond handling e cycle detection;
- merge strategies e precedence;
- safe template profile;
- typed variables, redaction e limits;
- input/output schema e bounded repair;
- backward/forward compatibility e migrations;
- offline resolution, catalog, cache e publication ceremony;
- threat model, prompt injection, tool authorization e privacy;
- conformance levels, positive/negative corpus e replay.

O exemplo mínimo, o lock e o vetor de assinatura são criptograficamente coerentes. O validador recalcula payload digest, lock digest e verifica Ed25519 com a public key de teste. A chave é rotulada exclusivamente para teste e não é uma trust anchor operacional.

## 5. SPEC-002 — Edit Case Registry Contract

A especificação define `EditCase` como aggregate root, com `EditBundle`, `ReviewDecision`, `RollbackPlan` e eventos subordinados. O workflow possui doze estados: DRAFT, IN_REVIEW, CHANGES_REQUESTED, APPROVED, APPLYING, APPLIED, VALIDATING, ACCEPTED, REJECTED, ROLLED_BACK, SUPERSEDED e CANCELLED.

A state machine YAML declara todas as transições e guards. O validador verifica que não existem pares `from/event` ambíguos. A aplicação é idempotente, usa revision e lease/fencing, cria nova Attempt e exige validação completa. O SGV continua autoridade científica; um reviewer não pode sobrepor hard gate. Rollback cria nova visão corrente ou aponta para snapshot validado, sem reescrever bytes ou histórico.

O registry separa responsabilidades: Revisão e Correção owns intention/workflow; Georreferenciamento executa; Verificação Geométrica aceita/rejeita; Resultados publica a visão; Artifacts preserva bundles e evidence.

## 6. SPEC-003 — AIBackend Protocol Contract

Todo backend implementa exatamente:

```text
supports() → estimate() → execute() → validate() → publish()
```

`supports()` é puro e retorna decisão tipada; `estimate()` produz budget e faixa de duração; `execute()` escreve apenas em staging; `validate()` verifica invariantes do backend; `publish()` publica somente candidates e retorna `requires_independent_sgv=true`. Nenhum método pode aceitar resultado final ou mudar QualityProfile.

Os schemas separam CapabilityRequest, SupportDecision, ExecutionEstimate, ExecutionRequest, RawAIResult, BackendValidationResult, PublicationResult e AIBackendManifest. O protocolo YAML fixa order, purity, preconditions, postconditions e failure classes. ModelPacks continuam pinados, signed, licensed, opt-in e offline-capable.

## 7. SPEC-004 — Template Contract

O Template Contract admite `LITERAL`, `MUSTACHE_SAFE` e `STRUCTURED`. O subset Mustache não admite lambdas, helpers, expressions, reflection, dynamic include, environment, network, clock ou randomness. Variables são tipadas e allowlisted; extra ou missing variables falham. JSON/YAML estruturado é produzido por serializer, não concatenação textual.

Output validation é obrigatória e inclui maximum bytes, JSON Schema ou required Markdown sections. Golden vectors cobrem success, missing required variable e unknown variable. Templates são dados versionados; não podem virar arquivos Python de lógica escondida.

## 8. SPEC-005 — Artifact Contract

O Artifact Contract introduz `ArtifactDescriptor`, `ArtifactSetManifestV2`, `ArtifactValidationProfile`, `ArtifactPublicationRecord` e um registry versionado. A taxonomia diferencia COG, GeoTIFF intermediário, analysis/validity masks, GPKG, GeoJSON preview, GCP/footprint vectors, quality/deformation/SGV/audit/validation reports, provenance, snapshots, edit artifacts, AI report, thumbnail e previews.

Cada descriptor contém kind, media type, path relativo seguro, size, SHA-256, role, profile, timestamps e metadata geoespacial quando aplicável. O manifest agrega producer, inputs, lineage, publication e root digest. Publicação usa staging, fsync, validation e rename atômico. Preview nunca é autoridade científica.

A major 1 do manifest foi preservada em `contracts/artifacts/compatibility/` para leitura. Novos writers produzem somente v2. Migração não inventa metadata ausente.

## 9. Integração com ADRs e DDD

A Fase E não criou decisions artificiais. Foram adicionadas referências normativas às ADRs já responsáveis por prompts/TaskEnvelope, contract freeze, artifacts, edit bundles, AI Router/Inference e audit. Owners primários:

- SPEC-001 e SPEC-004: BC-001 — Governança de Engenharia e Entrega;
- SPEC-002: BC-011 — Revisão e Correção;
- SPEC-003: BC-009 — Recuperação Assistida por IA;
- SPEC-005: BC-013 — Artifacts, Proveniência e Lifecycle.

Consumers acessam os contracts por published models; não importam modelos internos de outro context.

## 10. Achados e resoluções

| ID | Severidade | Achado | Resolução |
|---|---|---|---|
| SE-001 | Alta | Prompt Bundle sem canonicalização, lock e trust | SPEC-001 + schemas + vetor Ed25519 |
| SE-002 | Alta | Edit Bundle sem registry, workflow e rollback | SPEC-002 + aggregate + state machine |
| SE-003 | Alta | Backends IA sem interface e autoridade uniforme | SPEC-003 + cinco métodos tipados |
| SE-004 | Média | Templates com risco de lógica arbitrária | SPEC-004 + safe engines e output validation |
| SE-005 | Alta | Artifacts genéricos e manifest insuficiente | SPEC-005 + registry + manifest v2 |
| SE-006 | Média | Tarefas sem specification applicability | TaskEnvelope 1.4 em 758 tasks |
| SE-007 | Média | ADRs sem referência aos contracts executáveis | Seções normativas adicionadas |

Todos os achados estão resolvidos. Não há waiver aberto.

## 11. Compatibilidade e versionamento

As cinco especificações usam SemVer. Patch não pode alterar significado; minor adiciona comportamento opcional compatível; major remove, reinterpreta ou torna obrigatório. Readers podem manter janela de leitura; writers produzem apenas a versão pinada. Major desconhecida é armazenável para transporte quando seguro, mas não executável.

Schemas usam Draft 2020-12 e `additionalProperties: false` nos objetos normativos. Isso evita que consumers ignorem campos de segurança. Migrations são determinísticas, preservam source e lineage e não usam IA para inventar dados.

## 12. Segurança e prevenção de alucinação

Os controles acrescentados reduzem três fontes de erro:

1. **instrução ambígua:** precedence, fragments, lock e signature;
2. **comportamento inventado:** state machines, typed protocol e artifact registry;
3. **output formalmente incorreto:** schemas, safe templates e validation profiles.

Eles não presumem que um modelo é infalível. Tool sandbox, write scopes, testes, SGV independente, atomic publication e Reviewer continuam sendo controles externos ao prompt.

## 13. Validações executadas

| Validador | Resultado |
|---|---|
| Specification Review | PASS |
| Architecture Review | PASS |
| Requirements Review | PASS |
| Domain-Driven Design Review | PASS |
| ADR Definitive Review | PASS |
| Python Architecture fitness functions | PASS |
| Repository validation | PASS |
| Prompt payload/lock/signature vector | PASS |
| Edit Case deterministic state machine | PASS |
| AIBackend method order | PASS |
| Contract ownership coverage | PASS |

## 14. Riscos residuais

### SER-001 — Drift entre texto e schema

Residual baixo. O CI valida schemas e examples, mas semantic drift ainda exige review. Qualquer mismatch bloqueia merge.

### SER-002 — Prompt injection

Residual médio. Assinatura prova origem, não neutraliza conteúdo malicioso em input. A separação data/instruction, delimiters, tool sandbox, allow paths e reviewer limitam impacto.

### SER-003 — Migração do manifest v1

Residual baixo. Alguns sets antigos podem não possuir metadata para v2; o adapter permanece read-only e promoção bloqueia quando evidence não existe.

### SER-004 — Resource estimates de AIBackend

Residual médio. Estimate pode errar antes de corpus real. Benchmarks e profiles calibrados ajustam parâmetros; scheduler mantém admission authority.

## 15. Gate de saída

A Fase E é aprovada. A entrada arquitetural na próxima fase está liberada, mas isso não autoriza produção. O `ImplementationAuthorizationRecord` permanece requisito externo. Uma task futura deve parar se faltar specification aplicável, schema, version, hash, signature, state transition, protocol response ou artifact profile.
