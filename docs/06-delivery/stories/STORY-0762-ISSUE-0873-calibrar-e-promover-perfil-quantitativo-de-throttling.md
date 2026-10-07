# STORY-0762 / ISSUE-0873 — Calibrar e promover o perfil quantitativo de throttling

- **Tipo:** `História implementável — prerequisite técnica`
- **Estado:** `CLOSED_AS_DEFERRED` — obrigação consumida pela SPRINT-012; sem PASS de execução pendente
- **Épico pai:** `EPIC-008`
- **Sprint:** `SPRINT-002`
- **Domínio:** `PLT`
- **Bounded Context:** `BC-002 — Identidade e Controle de Acesso`
- **Papel executor:** `Security` — `ROLE-010`
- **TaskEnvelope:** `.codex/tasks/TASK-0769.json`

## História de usuário

Como responsável por segurança, preciso calibrar e promover o perfil quantitativo
de throttling requerido por REQ-AUTH-IMPL-007 conforme AP-003/BP-003, para que
STORY-0712 implemente o contrato existente sem inventar limites ou usar exemplos
sintéticos como política de runtime.

## Contexto

O diagnóstico está preservado no commit
`11df6dff79e7eaa33ac287cd576bcafd5344391c`, na evidência
`evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/auth-impl-dbschema-parte-1/throttling-correction-7424467.md`.
AP-003 promove valores somente após BP-003; BP-003 não contém valores promovidos.
O contrato exige APPROVED_PROFILE_ONLY e missing/invalid profile => DENY.
ISSUE-0822 e ISSUE-0150 permanecem bloqueadas.

Padrão de decomposição: STORY-0761/ISSUE-0871 publica uma prerequisite com
TaskEnvelope próprio e arestas `blocks` antes da implementação consumidora.
Esta issue é representada por este documento e pelo ISSUE_INDEX, como as demais
histórias implementáveis; não se cria outro envelope de épico. STORY-0762 e
ISSUE-0873 são novos IDs locais; TASK-0762 a TASK-0768 já estão alocados em
`.codex/tasks/operations/`, por isso o envelope usa o próximo ID livre TASK-0769.

## Resultado verificável

Calibração reproduzível do recorte de throttling de BP-003 e perfil aprovado,
versionado em AP-003, com cada valor ligado à evidência e interpretação explícita
para consumo determinístico pela STORY-0712. A materialização desta prerequisite
não executa benchmark, não promove valores e não aprova sua própria entrega.

## Escopo / allow paths

- `docs/04-quality/benchmark-profiles/BP-003-security-runtime-calibration.md`
- `docs/03-engineering/application-profiles/AP-003-web-security-runtime-profile.md`
- `tests/security/throttling_calibration/**`
- `evidence/security/throttling-calibration/**`
- `.codex/tasks/TASK-0769.json`

Somente throttling, janelas, cooldown, atraso/lockout e concorrência estritamente
necessária ao recorte. Um comando/script focado no path de testes e evidência
versionada bastam; não criar framework de benchmark, serviço, registry ou
infraestrutura permanente. No AP-003, publicar dados declarativos versionados,
com unidades, limites de validade e rastreabilidade, sem nova autoridade.

## Fora de escopo / não objetivos

- Implementar enforcement, estado persistente ou migrations de STORY-0712.
- Alterar código de produção, contratos compartilhados, ADRs ou pisos de segurança.
- Calibrar sessões, Argon2id ou outros parâmetros de BP-003; considerar custo de
  autenticação existente como carga medida não autoriza recalibrá-los.
- Alterar o piso da replay key já entregue em AP-003.
- Criar infraestrutura permanente ou subir a plataforma inteira.
- Declarar BP-003 integralmente concluído ou readiness de produção do EPIC-008.

## Requisitos, ADRs e profiles

- `REQ-AUTH-IMPL-007`; prerequisite de sua implementação, não evidência de enforcement.
- `ADR-006`, `ADR-007`, `ADR-008`, `ADR-028`, `ADR-031`, `ADR-034`.
- `AP-003` é a autoridade operacional versionada; `BP-003` governa calibração.
- Contrato congelado `identity-access-local-auth-freeze`, policies.throttling e
  boundary-evidence.schema.json; nenhuma alteração compartilhada nesta entrega.

## Dependências

`STORY-0036`, `STORY-0767`, `STORY-0768`, `STORY-0769`

STORY-0767 / ISSUE-0874 / TASK-0770 está satisfeita no baseline aprovado
`4b634381328bd969679abe48ee6936aaf8fe4319`, que contém os dois perfis 1.0.0 e
o vínculo formal em BP-003. Aprovações independentes architecture/QA/final
re-review PASS e ausência de decisões materiais foram confirmadas pelo usuário.
TASK-0769 não tem decisão aberta nos perfis hardware/workload, mas está bloqueada operacionalmente por grafo/lock e venue. Security/ROLE-010
permanece executor; os predecessores são preservados como rastreabilidade.

Consumir os arquivos imutáveis e seus digests a partir desse SHA:
- `docs/04-quality/benchmark-profiles/BP-003-throttling-hardware-reference.yaml`
- `docs/04-quality/benchmark-profiles/BP-003-throttling-threat-workload.yaml`

Versões, file/definition SHA-256, aplicabilidade e origem das aprovações estão em
`evidence/security/throttling-calibration/readiness-reconciliation-v1.json`.
Hardware é reference_benchmark sem claim minimum_supported; carga e critérios
são do experimento post_auth_session, sem política runtime. Os flags PENDING
dos artifacts v1 são históricos e preservados; esta reconciliação consome as
aprovações posteriores confirmadas, sem repetir QA/review. O gate de produção
em hardware mínimo suportado continua fora da prontidão deste experimento.

## Relação de desbloqueio

STORY-0768 / ISSUE-0875 / TASK-0771 decide o grafo Python e o handoff para DevOps materializar uv.lock com scope autorizado. STORY-0769 / ISSUE-0876 / TASK-0772 provisiona e evidencia o venue exato. As duas prerequisites são paralelas, sem aresta entre si; STORY-0239 não é predecessor. TASK-0769 permanece BLOCKED até ambos os handoffs aprovados, uv.lock efetivamente materializado e preflight de runtime/venue conforme os perfis. A aprovação de ISSUE-0874 permanece válida, mas não atesta disponibilidade operacional.

`STORY-0767 / ISSUE-0874 / TASK-0770` blocks
`STORY-0762 / ISSUE-0873 / TASK-0769` blocks
`STORY-0712 / ISSUE-0822 / TASK-0712` blocks
`STORY-0040 / ISSUE-0150 / TASK-0040`.
Os predecessores existentes são preservados. Só integrar e aprovar o perfil
libera a correção da STORY-0712; concluir esta prerequisite não conclui throttling
nem o aceite final do EPIC-008.

## Critérios de aceitação

- [ ] AC-ISSUE-0873-01: Executar somente a calibração de throttling de BP-003 no hardware reference_benchmark aprovado em STORY-0767 e vinculado por BP-003, sem claim minimum_supported, registrando comandos, runtime/dependências, carga, concorrência, entradas, configurações candidatas, resultados brutos e digests para reprodução.
- [ ] AC-ISSUE-0873-02: Justificar cada valor selecionado por medições e threat tests de brute force, carga legítima e abuso; demonstrar preservação dos pisos de segurança, ausência de enumeração/bypass e ausência de DoS operacional evidente por CPU/memória, documentando limites da evidência sem inventar metas.
- [ ] AC-ISSUE-0873-03: Promover em AP-003 somente valores sustentados pela calibração, com versão, unidades, aplicabilidade, semântica de contagem/janela/cooldown/lockout e validade explícitas conforme o contrato; verificar consumo determinístico e rejeição de perfil ausente/inválido sem implementar throttling funcional.
- [ ] AC-ISSUE-0873-04: Produzir evidência reproduzível e obter revisão técnica aplicável do Arquiteto e validações independentes de QA e Reviewer no mesmo commit candidato, antes da promoção/integração que libera STORY-0712; preservar demais parâmetros e registrar rollback do perfil.

## Testes / validações obrigatórias

- Reexecutar comando focado de calibração e conferir configurações/entradas/digests e resultados sob o ambiente declarado; variação de medições deve ser registrada.
- Threat tests e carga legítima/abusiva: resistência a brute force, preservação de pisos e medição de CPU/memória/concurrency para o recorte de throttling.
- Verificar correspondência valor -> medição -> versão AP-003 e leitura determinística; perfil ausente/inválido não se torna elegível.
- `make verify` antes do handoff; revisão independente do mesmo candidato.

## Evidências obrigatórias

- `evidence/security/throttling-calibration/`: comandos/script versionado, ambiente e hardware de referência aprovado, fixtures atribuíveis, configurações candidatas e resultados brutos, hashes, análise de segurança/DoS e limitações.
- Manifest de promoção ligando versão do AP-003, valores/unidades e evidências por path/digest ao candidato; sem secrets, identidades/IPs reais ou credenciais.
- Resultados de reprodução e revisões independentes; a evidência atual do diagnóstico permanece intacta.

## UX e estados de erro

Não há UI ou endpoint novo. Perfil ausente/inválido permanece DENY; nenhuma
configuração candidata ou fixture ganha autoridade operacional sem promoção.

## Métrica ou evidência

Medições reproduzíveis de custo CPU/memória, comportamento sob carga legítima e
brute force, justificativa por parâmetro e resultado das revisões. Não há valor
quantitativo ou benchmark executado nesta materialização.

## Migration, compatibilidade e rollback

Nenhuma migration. Compatibilidade preserva contrato e parâmetros já entregues.
Rollback desabilita o consumo da versão rejeitada e mantém DENY quando não houver
perfil válido aprovado; não substitui valores por defaults silenciosos.

## Condições de parada

- Perfis aprovados de hardware/workload ausentes, inválidos ou inaplicáveis, ou pisos/runtime/observáveis requeridos ausentes: parar sem defaults nem extrapolação a minimum_supported.
- Qualquer valor não pode ser ligado à calibração reproduzível ou requer reduzir piso, permitir enumeração ou contornar autorização/CSRF.
- Acoplamento normativo inevitável com outro parâmetro de BP-003 não está explicitamente demonstrado: retornar ao owner antes de ampliar o slice.
- Semântica necessária exige alterar contrato compartilhado ou decisão material de produto/arquitetura: retornar ao owner.
- Write scope colide com lane ativa ou exige código de produção/infraestrutura permanente.
- Revisões independentes não existem para o candidato: não promover/integrar o perfil nem liberar consumers.

## Prompt de execução Codex

Leia AGENTS.md, ROLE-010, este documento, TASK-0769, AP-003/BP-003 e contrato de
throttling. Execute somente o recorte de calibração descrito. Não implemente
STORY-0712, não escolha valores arbitrários e não aprove seu próprio trabalho.

## Gates de planejamento e revisão

Estado Blocked por prerequisites operacionais; a prontidão anteriormente registrada se limitava ao planejamento do experimento. Após resolver os blockers e integração administrativa
do envelope/índices no consumer base; hardware/workload e suas aprovações estão
satisfeitos. Security deve conferir runtime, locks, pisos e observáveis fixados
pelos perfis antes de medir, sem escolher outro baseline. Arquiteto valida a
promoção técnica; QA e Reviewer validam independentemente o mesmo candidato.
Campos PASS constantes exigidos pelo schema do envelope identificam sua baseline
estrutural; não atestam benchmark, promoção ou aprovação independente realizada.
O review independente do candidato de calibração permanece BLOCKED até a
execução do benchmark e evidência real; isso não reabre a prerequisite aprovada.

## Verificação da materialização

Validar JSON Schema, IDs sem colisão, índices sincronizados, DAG acíclico,
dependencies iguais aos predecessores, allow/deny paths e preservação do commit
do diagnóstico. Registrar resultado e limitações da verificação antes do handoff.

Verificação realizada nesta materialização com `.venv/Scripts/python.exe` e
`jsonschema.Draft202012Validator`:

- TASK-0769, TASK-0712 e TASK-0040: JSON Schema, referências existentes e campos de dependências espelhados — PASS.
- Grafo e índices: 762 nós, 1173 arestas, 91 ondas, zero ciclos; todos os predecessores do índice correspondem ao grafo — PASS.
- IDs de TaskEnvelope em `.codex/tasks/**` sem colisão; nova issue não reutiliza ID operacional — PASS.
- Índices CSV/JSON, owner, allow/deny paths, critérios e dependências da prerequisite consistentes — PASS.
- TASK-0712/TASK-0040 alterados somente nos campos de predecessores e seus espelhos; scopes anteriores preservados — PASS.
- Commit 11df6dff preservado como ancestral, evidência do diagnóstico intacta e diff vazio em código de produção, contratos e AP-003/BP-003 — PASS.
- `make verify`: ruff, mypy, OpenAPI check/diff e frontend typecheck passaram; exit 1 no Vitest por EPERM ao renomear temporários, antes de coletar testes.
- `tools/validate_repository.py`: iniciado separadamente e interrompido após percurso prolongado do repositório sem saída; resultado global não verificado. Não foram alterados validators, contadores de baselines históricas ou registros de aprovação para forçar PASS.

Estes checks verificam a materialização, não a calibração nem sua promoção.
Os registros históricos de revisão não foram ampliados para aprovar esta entrega.
Antes de Ready, o Tech Lead deve reconciliar as revisões/inventários aplicáveis e
validar a baseline conforme a Definition of Ready; não há autorização implícita
de execução ou promoção por um check de JSON Schema.

## Disposição administrativa vigente — 2026-10-07

CLOSED_AS_DEFERRED / DEFERRED_TO_SPRINT_012, por decisão explícita do usuário.
[Obrigação canônica que absorve o trabalho pendente](../../07-assurance/PHASE-G-CTO-REVIEW-REPORT.md#epic-008-req-auth-impl-007-production-readiness):
EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS. Este item deixa de bloquear o
 desenvolvimento corrente; suas instruções de execução anteriores descrevem o
escopo técnico futuro e não autorizam retomar infraestrutura nesta fase.
Não há PASS de execução/produção. Evidências anteriores permanecem imutáveis.
Retomada na fase de readiness exige autoridade operacional e gates existentes.