# SPEC-003 — AIBackend Protocol Contract

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-009`
- **ADRs governantes:** `ADR-051`, `ADR-052`, `ADR-053`
- **Bounded Contexts:** `BC-009`, com integração a `BC-006`, `BC-007`, `BC-010`, `BC-013`
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Propósito

`AIBackend` é o protocolo único para qualquer mecanismo de inferência integrado ao DSGeorref. Ele elimina adapters ad hoc, funções com semântica sobreposta e backends que misturam capability discovery, alocação, inferência, validação e publicação. Todo backend implementa exatamente cinco operações na ordem `supports()`, `estimate()`, `execute()`, `validate()` e `publish()`.

## 2. Autoridade

O AI Router escolhe candidatos de backend, mas não aceita resultado. O backend executa e valida invariantes próprias. O SGV, fora do backend, mantém a autoridade geométrica. O contexto de Artifacts publica bundles imutáveis. Jobs concede leases e budgets. Nenhuma operação do protocolo pode alterar a fonte de verdade desses contexts.

## 3. Identidade

Backend possui `backend_id` estável, SemVer, protocol version, capabilities, determinism e resource classes. A identidade de uma execução inclui execution id, request id, backend id/version, model pack id/hash, seed, inputs e policy. O mesmo conjunto sob idempotency key não cria execução paralela divergente.

## 4. Manifest

O manifest é assinado ou incluído em pacote assinado. Ele declara capabilities, constraints de ModelPack, CPU/GPU, offline, determinism e protocolo. Capability não declarada não pode ser inferida pelo Router. Mudança de semântica exige major.

## 5. Sequência obrigatória

Uma chamada posterior exige saída válida da anterior. Pular `estimate` ou `validate` é erro. Repetir `supports` e `estimate` deve ser seguro. `execute` e `publish` são idempotentes por IDs persistidos. A máquina de orquestração registra cada transição.

## 6. supports()

`supports(request) -> SupportDecision` é pura: não baixa modelo, não aloca GPU, não lê payload raster completo e não publica artifact. Ela verifica capability, perfil de input, disponibilidade declarada, versão, ModelPack e policy. Retorna booleano, reason code e constraints. Exceção para “não suportado” é proibida; isso é decisão normal e tipada.

## 7. Semântica de support

`SUPPORTED` significa que o backend reconhece o contrato e pode estimar sob o resource profile atual, não que a execução será aceita. `RESOURCE_UNAVAILABLE` pode mudar; `POLICY_DENIED` é terminal para a requisição; `MODEL_PACK_MISSING` orienta import governado, nunca download implícito.

## 8. estimate()

`estimate(request) -> ExecutionEstimate` é read-only e pode consultar metadados locais. Produz budgets de CPU, RAM, GPU, VRAM, artifact bytes e faixa de duração min/mode/max com confidence e assumptions. Deve ser conservadora e monotônica: input maior sob perfil equivalente não pode reduzir arbitrariamente o upper bound.

## 9. Admission

Scheduler compara estimate com quotas e breakers. Aceitar estimate cria reservation/lease; backend não se autoagenda. Estimativa fora dos limites retorna diagnóstico, não executa parcialmente. Profiles calibrados fornecem coeficientes; valores não são hardcoded no backend.

## 10. execute()

`execute(request) -> RawAIResult` consome apenas artifacts verificados e ModelPack pinado. Usa seed quando aplicável, respeita deadline/cancelamento e escreve somente em staging. O retorno contém candidates, diagnostics e runtime record. Não cria ResultSnapshot aceito, não modifica original e não publica path final.

## 11. Isolamento

Crash nativo, OOM ou device loss devem ficar contidos no worker. Backend não mantém estado global mutável entre execuções. Cache é content-addressed e governado. Recursos são liberados em finally/cleanup idempotente. Processo pode ser reciclado.

## 12. Determinismo

Backends declaram `DETERMINISTIC`, `SEEDED` ou `BOUNDED_NONDETERMINISTIC`. Seed e inventory de RNG entram no runtime record. Bounded nondeterminism exige consensus ou tolerance profile e não pode prometer igualdade bitwise. Replays usam as mesmas versões e artifacts.

## 13. validate()

`validate(raw) -> BackendValidationResult` valida schema, shapes, finitude, ranges, correspondência com inputs, artifact integrity e invariantes específicas do backend. Não repete SGV nem reduz thresholds. Resultado FAIL impede publicação e inclui failure code seguro.

## 14. Independência do SGV

Mesmo após PASS do backend, todo candidato geométrico passa pelo SGV independente. O backend não recebe autoridade para alterar QualityProfile, aceitar gray zone ou marcar resultado final. Consensus de múltiplos modelos também não substitui o SGV.

## 15. publish()

`publish(validation) -> PublicationResult` publica apenas `AI_CANDIDATE_ONLY`. Preconditions incluem validation PASS, lease, manifest e hashes. Publicação usa staging, fsync e rename atômico. O retorno declara `requires_independent_sgv=true`. Se artifacts já existem com os mesmos hashes, a operação retorna o receipt anterior.

## 16. Failure model

Falhas são classificadas como retryable ou terminal. Retryable não inclui input inválido ou model pack corrupto. O backend retorna códigos estáveis, não mensagens usadas como lógica. Stack trace é evidence protegida e redigida.

## 17. Cancelamento

Execute observa safe points e deadline. Cancelamento cooperativo produz status CANCELLED e limpa staging. Kill forçado é contido pelo worker, e reconciliação detecta lease expirada. Publish não é cancelável após o ponto de rename; o receipt permite reconciliar.

## 18. ModelPack

Pesos, tokenizer/config, licença, hashes, runtime requirements e compatibilidade pertencem ao ModelPack. Backend não aceita path arbitrário. Import verifica assinatura e SBOM. Offline é baseline; egress continua DENY salvo policy explícita.

## 19. Segurança

Inputs não confiáveis são tratados por parsers isolados e allowlists. Model deserialization evita execução arbitrária. Backends não carregam pickle irrestrito. GPU isolation, path safety, size budgets e timeouts são obrigatórios.

## 20. Privacidade

Nenhum input operacional treina modelo automaticamente. Telemetria não inclui imagens, prompts ou coordinates sensíveis. Export de pesquisa é fluxo separado, consentido e com provenance. Diagnostics são allowlisted.

## 21. Versionamento

Protocol major muda assinatura ou semântica de método. Minor adiciona campos opcionais ou reason codes extensíveis. Backend major muda interpretação ou output. ModelPack version é independente. Compatibility matrix combina as três dimensões.

## 22. Backward compatibility

Router pode manter adapter para uma major anterior durante janela declarada, mas novos writers usam major atual. Adapter é testado e não pode preencher campo científico por default inventado. Replay preserva formato original e versão do adapter.

## 23. Performance

Estimate deve ser barato em relação a execute. Supports não realiza inferência. Validate pode reutilizar metadata e checksums, não rerodar modelo. Batching é capability separada e deve preservar IDs e resultados por item.

## 24. Observabilidade

Métricas: backend id/major, capability, status, duração, budget ratio e reason code. ModelPack completo, project id e artifact id não são labels. Traces ligam cinco métodos e lease. Logs não contêm tensors ou dados brutos.

## 25. Teste de conformidade

Uma suíte comum executa: capability suportada/não suportada, estimate ordenada, idempotência, deadline, cancelamento, ModelPack inválido, OOM contido, result schema inválido, validation fail, publish atomic, replay e prova de que SGV ainda é exigido.

## 26. Mock e fake

Fakes de teste implementam o protocolo completo e são claramente identificados. Não podem ser promovidos como backend real. Golden fixtures têm hashes. Testes de Router não devem monkeypatch funções internas específicas de um backend.

## 27. Extensões

Nova capability usa string namespaced e schemas versionados. Não cria sexto método sem major e ADR. Streaming interno pode existir dentro de execute, mas a saída pública continua RawAIResult. Distributed execution permanece responsabilidade de Jobs.

## 28. Critérios de aceite

- ordem exata implementada;
- schemas válidos;
- supports puro;
- estimate bounded;
- execute somente staging;
- validate obrigatório;
- publish candidate-only;
- SGV independente;
- idempotência, cancelamento, offline e evidence testados.

## 29. Condições de parada

A implementação para se capability, inputs, outputs, ModelPack, budget, failure code ou authority não estiverem especificados; se um backend exigir download implícito; se publish pretender aceitar resultado; ou se houver tentativa de compartilhar estado global mutável entre execuções.
