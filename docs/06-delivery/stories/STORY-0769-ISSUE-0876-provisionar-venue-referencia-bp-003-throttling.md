# STORY-0769 / ISSUE-0876 — Provisionar e evidenciar o venue de referência do benchmark de throttling BP-003

- **Tipo:** `História implementável — prerequisite técnica`
- **Estado:** `CLOSED_AS_DEFERRED` — obrigação consumida pela SPRINT-012; sem PASS de execução pendente
- **Épico pai:** `EPIC-008`
- **Sprint:** `SPRINT-002`
- **Domínio:** `PLT`
- **Bounded Context:** `BC-002 — Identidade e Controle de Acesso`
- **Owner executor:** `DevOps`
- **TaskEnvelope:** `.codex/tasks/TASK-0772.json`
- **Downstream:** `STORY-0762 / ISSUE-0873 / TASK-0769`, Security/ROLE-010

## Resultado e limites

Provisionar e evidenciar target Linux nativo ou virtualizado e gerador em separate execution domain conforme BP-003-throttling-hardware-reference v2.1.0 e BP-003-throttling-threat-workload v2.0.1, com runtime PostgreSQL/backend reproduzível, manifest e handoff de readiness para TASK-0769, sem executar benchmark.

A próxima qualificação consome o par abaixo após revisão independente e integração. O [PR #1065](https://github.com/raphaelperrut/DSGeorref/pull/1065) registra a baseline histórica 2.0.0.

- [BP-003-throttling-hardware-reference v2.1.0](../../04-quality/benchmark-profiles/BP-003-throttling-hardware-reference.yaml), definition SHA-256 `c3600f36866839bf7b1117c32ac1630a17d32e84095c7e88fb8c49a1bb5593a5`.
- [BP-003-throttling-threat-workload v2.0.1](../../04-quality/benchmark-profiles/BP-003-throttling-threat-workload.yaml), definition SHA-256 `20f8075330b539fe63b8de7365d792daddb0e6dc9d3cdbabc5d2677eace94aa3`.

Manifest e comprovantes devem abranger todos os campos dos perfis, inclusive os não resumidos aqui. Candidatos e evidências vinculados ao hardware v2.0.0 permanecem históricos. A qualificação do hardware v2.1.0 exige novo fingerprint.

- **CPU:** x86_64 Intel ou AMD; >=4 execution CPUs disponíveis (logical CPUs/vCPUs permitidas), com reserva de referência de 4 CPUs, API budget 2 e PostgreSQL budget 2. Usar affinity/cpusets disjuntos quando disponíveis; caso contrário, justificar a indisponibilidade e comprovar fallback de reserva/isolamento reproduzível com os mesmos budgets 2+2. Quota isolada não comprova isolamento. Registrar modelo, stepping/microcode, topologia/SMT, clocks/governor quando expostos e estado de boost, mantendo a configuração entre repetições; telemetria indisponível deve ser explícita. Aplicar/fixar binding NUMA útil quando exposto; caso contrário registrar not_applicable e motivo. Nenhuma equivalência de CPU ou SKU é inferida.
- **RAM:** >=8 GiB disponíveis/reserváveis; reserved target de 8 GiB, API <=2 GiB, PostgreSQL <=4 GiB e reserva de 2 GiB para OS/measurement. Registrar limites/reservas efetivos cgroup v2 e backing, sem overcommit que prejudique a reserva. Swap configurado é permitido; qualquer swap-in/out atribuível ao target ou crescimento de memory.swap.current nas janelas invalida a execução. Registrar uso inicial, deltas por janela, memory.current, memory.events e paging counters. Sem atribuição, exigir zero swap-in/out e zero crescimento de swap no ambiente; observabilidade ausente é inconclusiva/fail. OOM/falha de alocação rejeita o candidato.
- **Storage:** SSD ou NVMe local, >=100 GiB livres antes de cada repetição no filesystem Linux de WAL/data e no backing físico local comprovado. Filesystem Linux durável; ext4 aceitável. Windows 11 + WSL2 + VHDX/ext4 em SSD/NVMe local permitido; capacidade virtual esparsa isolada não comprova espaço no backing. Registrar camadas, mapping VHDX/dispositivo, identidade/settings/I/O e mounts; fsync e durable commits obrigatórios. Network filesystem, RAM disk e WAL somente volátil proibidos. Contenção material de I/O invalida a repetição; ausência de evidência para excluir interferência é inconclusiva/fail.
- **Runtime:** target Linux nativo ou virtualizado, incluindo Windows 11 + WSL2; cgroup v2, Python 3.12.13, PostgreSQL 18.x, OCI assinado/Compose e um processo API. Registrar OS/build do host, kernel guest, hypervisor/WSL, limites VM/vCPU/RAM, engine/Compose, fingerprints, digests e locks conforme TECHNOLOGY_BASELINE.yaml. Preservar TLS/provenance e os perfis Argon2id/session aprovados; não selecionar novos parâmetros. Configuração/fingerprint fixos nas três repetições futuras, com clocks/deltas/interferência observados separadamente; drift exige novo conjunto completo.
- **Load generator:** separate execution domain, sem exigir segundo host físico; host/VM separado ou cgroup/cpuset/reserva demonstravelmente isolado fora das 4 CPUs/8 GiB do target. No venue atual, o limite operacional do gerador é 512 MiB (536870912 bytes). Uso no mesmo host exige recursos adicionais suficientes. Registrar CPU/RAM/I/O, placement, ambiente, versão/clock e transport fingerprint. Não consumir a reserva do target; interferência material invalida a execução e isolamento/atribuição sem evidência é inconclusivo/fail.
- **Claims:** nenhum minimum-supported claim, throughput/capacity claim, equivalência/comparação entre CPUs ou production SLO. GPU não requerida e sem uso neste experimento. Notebook v2 elegível em princípio; qualificação depende das evidências reais, sem PASS presumido.

Usar artifacts existentes e aprovados para PostgreSQL/backend e registrar seus digests, locks, config, contrato, perfis de segurança já existentes e startup/readiness reais. Não inventar backend/imagem/runtime aprovado. A lane pode iniciar alocação e attestation do host independentemente da validação do lock. Se faltar artifact de runtime necessário ao handoff completo, registrar o blocker operacional e não concluir esta tarefa com evidência somente de host.

uv.lock foi materializado e integrado na main. Sua presença por si só não comprova readiness. UV_LOCK_STATUS = INTEGRATED, UV_LOCK_PR = #1070, UV_LOCK_MERGE_COMMIT = 81f96b592cdac592285f4f8b736ab8be0391777c, UV_LOCK_SHA256 = bd70e02748e7f09b5ca7fd544862f3b7d1deec30365a65c66552795839ce5cf2.

Required roles: DevOps executor; Arquiteto valida aderência técnica ao profile; QA verifica evidência objetiva/reprodução/readiness; Reviewer faz final review no mesmo candidate SHA, independente do executor. Uso/contratação de host exige autorização operacional concreta existente, sem presumir orçamento, credenciais ou fornecedor. Identificar target e autorização antes de ações externas; não há nova decisão arquitetural por cumprir o profile. Não reabrir STORY-0239 nem TASK-0763, que permanecem referências com escopos próprios.

## Allow paths exclusivos de execução

- `infra/benchmarks/bp003-throttling-venue/**`
- `evidence/operations/bp003-throttling-venue/**`

## Deny paths

- `src/**`
- `pyproject.toml`
- `uv.lock`
- `requirements-validation.txt`
- `infra/images/**`
- `.github/**`
- `contracts/**`
- `tests/**`
- `tools/**`
- `**/migrations/**`
- `docs/04-quality/benchmark-profiles/**`
- `docs/03-engineering/application-profiles/AP-003-web-security-runtime-profile.md`
- `.codex/tasks/TASK-0769.json`
- `.codex/tasks/TASK-0712.json`
- `.codex/tasks/TASK-0040.json`
- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/**`
- `evidence/architecture/python-workspace-dependency-graph/**`

A criação administrativa de histórias/envelopes/índices foi autorizada separadamente pelo pedido de decomposição de ISSUE-0873. O escopo acima não autoriza sua alteração durante a execução destas prerequisites. Cada execução usa uma issue e TaskEnvelope por branch/worktree; nenhuma execução ocorreu nesta materialização. Não implementar produto, alterar profile, gerar lock ou provisionar host neste passe.

## Emenda documental de autoridade

Emenda documental explícita do Owner restrita à Story STORY-0769 e ao próprio .codex/tasks/TASK-0772.json para vincular hardware BP-003 v2.1.0 e workload v2.0.1 após revisão independente e integração; não amplia allow_paths operacionais nem remove deny_paths. Não autoriza produto, AP-003, profiles, benchmark, configuração WSL/Docker ou criação de uv.lock. A autorização de escrita no próprio envelope vale exclusivamente para esta emenda; os allow/deny paths operacionais acima permanecem intactos. O estado administrativo histórico e os gates operacionais não recebem PASS por esta correção.

## Dependências e isolamento

Predecessores: `STORY-0036`, `STORY-0767`.

STORY-0768 / ISSUE-0875 / TASK-0771 e STORY-0769 / ISSUE-0876 / TASK-0772 são paralelas: nenhuma depende da outra e seus write scopes são disjuntos. Ambas bloqueiam STORY-0762 / ISSUE-0873 / TASK-0769, que bloqueia STORY-0712 / ISSUE-0822 e depois STORY-0040 / ISSUE-0150. STORY-0239 não vira predecessor; seu caminho já é downstream e produziria ciclo. STORY-0767 aprovada permanece satisfeita; não se altera a semântica ou o conteúdo do benchmark.

## Requisitos e ADRs

REQ-AUTH-IMPL-007; downstream REQ-AUTH-IMPL-007.
ADRs: ADR-006, ADR-007, ADR-008, ADR-009, ADR-028, ADR-031, ADR-033, ADR-034. Sem nova ADR nesta decomposição.

## Critérios de aceitação

- [ ] AC-ISSUE-0876-01: Venue real identificado, acesso operacional e autorização de uso registrados sem secrets, target Linux nativo ou virtualizado, incluindo Windows 11 + WSL2, conforme BP-003-throttling-hardware-reference v2.1.0 e BP-003-throttling-threat-workload v2.0.1 após revisão independente e integração; nenhum minimum-supported claim, throughput/capacity claim, equivalência/comparação entre CPUs ou production SLO.
- [ ] AC-ISSUE-0876-02: Evidências objetivas completas do hardware profile v2.1.0: x86_64 Intel/AMD, >=4 execution CPUs disponíveis, reserva de 4 CPUs (API 2/PostgreSQL 2), affinity/cpusets disjuntos quando disponíveis ou fallback de isolamento reproduzível comprovado; modelo/topologia/SMT/clocks/boost registrados, NUMA útil quando exposto ou not_applicable justificado; >=8 GiB disponíveis/reserváveis e reserved target 8 GiB (API <=2 GiB, PostgreSQL <=4 GiB, OS/measurement 2 GiB), limites/reservas cgroup v2 sem overcommit que os prejudique. Swap configurado permitido; qualquer swap-in/out do target ou crescimento de target swap nas janelas invalida execução; uso inicial/deltas, memory.current, memory.events e paging observáveis obrigatórios; sem atribuição, zero swap-in/out e crescimento no ambiente; telemetria ausente é inconclusiva/fail. Configuração observada sem valores presumidos.
- [ ] AC-ISSUE-0876-03: SSD ou NVMe local, >=100 GiB livres antes de cada repetição no filesystem Linux durável WAL/data e backing físico local comprovado; ext4 aceitável, Windows 11 + WSL2 + VHDX/ext4 permitido, capacidade virtual isolada insuficiente; fsync/commits duráveis obrigatórios, network filesystem/RAM disk proibidos, sem contenção material ou quota que prejudique a reserva; manifest registra identidade/settings/I/O, mounts/camadas/mapping e comprovantes atribuíveis ao venue.
- [ ] AC-ISSUE-0876-04: PostgreSQL 18.x/backend executáveis por artifacts imutáveis existentes e bindings aprovados, Python 3.12.13, OCI assinado/Compose/cgroup v2, processo/CPU/RAM/isolamento e TLS/provenance conforme os profiles BP-003 vinculados e a baseline; fingerprints/digests/locks registrados. Gerador em separate execution domain fora da reserva de 4 CPUs/8 GiB do target (512 MiB (536870912 bytes) de limite operacional no venue atual), sem exigir segundo host físico, isolamento/atribuição comprovados e interferência material invalida execução; condições reproduzíveis para três repetições futuras com mesmo fingerprint/candidato, sem executar a carga BP-003.
- [ ] AC-ISSUE-0876-05: Provisioning/reproduction instructions, hardware/runtime manifest e checks de startup/readiness sem benchmark possuem comandos, resultados reais, versões/digests e candidate SHA; revisão técnica Arquiteto, QA e Reviewer independentes no mesmo candidato validam correspondência integral e handoff exato para Security/TASK-0769. Evidência parcial não conclui a prerequisite.

## Validações e evidência

- Conferir venue manifest campo a campo contra BP-003-throttling-hardware-reference v2.1.0 e BP-003-throttling-threat-workload v2.0.1, vinculando versões e definition digests: hardware c3600f36866839bf7b1117c32ac1630a17d32e84095c7e88fb8c49a1bb5593a5; workload 20f8075330b539fe63b8de7365d792daddb0e6dc9d3cdbabc5d2677eace94aa3. Comprovar CPU/SMT/boost/NUMA aplicável ou justificado/cgroups/RAM/swap observável/SSD-ou-NVMe/filesystem Linux durável/backing local e isolamento do gerador; observações não substituem requisitos.
- Reproduzir provisionamento/readiness com target autorizado, registrar comandos/saídas reais e digests, isolamento e rollback; nenhum traffic loop, fase ou medição de BP-003.
- Validar startup/conectividade/durabilidade do PostgreSQL/backend e gerador em separate execution domain usando bindings aprovados. Validar o lock aplicável, seu SHA-256 e sua compatibilidade com o runtime e os artifacts aprovados. A qualificação de hardware/venue pode ser demonstrada separadamente. O handoff completo e a execução downstream ficam bloqueados, sem defaults, se o lock aplicável estiver ausente, inválido, divergente ou não validado, ou se runtime, perfil, assinatura, provenance ou artifacts exigidos faltarem ou divergirem. A TASK-0772 deve manter uv.lock em deny_paths e não pode alterá-lo nem regenerá-lo.
- Arquiteto/QA/Reviewer independentes validam o mesmo candidate SHA e handoff; conferir diff sem código de produto, alteração de profiles ou políticas runtime; make verify antes do handoff.

Evidência: `evidence/operations/bp003-throttling-venue/`. Required roles: DevOps, Arquiteto, QA, Reviewer. Aprovações independentes no mesmo candidate SHA, com identidade/role/evidência atribuíveis; não basta autoemitir PASS ou reutilizar review de outro candidato. Perfis existentes são lidos por digest; evidências revisadas são append-only.

## Handoff, rollback e parada

Handoff identifica outputs exatos, versões/SHA-256/candidate SHA, limites e comandos de reprodução; o consumidor mantém BLOCKED se o lock aplicável estiver ausente, inválido, divergente ou não validado, ou se faltar venue ou runtime/observáveis exigidos. Sem migration ou mudança de contrato de produto. Rejeição invalida o handoff e preserva o blocker, sem defaults silenciosos. Parar por autoridade contraditória, necessidade de ampliar escopo, entrada operacional ausente ou aprovação independente faltante.

## Planejamento e prompt

Leia AGENTS.md, papel, esta história, TaskEnvelope e referências aplicáveis. Execute somente o recorte autorizado após liberação do Tech Lead. Campos PASS constantes exigidos pelo schema descrevem a baseline estrutural; não comprovam execução ou aprovação. Estado Planned e review BLOCKED até evidência independente. A criação destes documentos não libera TASK-0769 nem conclui ISSUE-0873/0822/0150.

## Disposição administrativa vigente — 2026-10-07

CLOSED_AS_DEFERRED / DEFERRED_TO_SPRINT_012, por decisão explícita do usuário.
[Obrigação canônica que absorve o trabalho pendente](../../07-assurance/PHASE-G-CTO-REVIEW-REPORT.md#epic-008-req-auth-impl-007-production-readiness):
EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS. Este item deixa de bloquear o
 desenvolvimento corrente; suas instruções de execução anteriores descrevem o
escopo técnico futuro e não autorizam retomar infraestrutura nesta fase.
Não há PASS de execução/produção. Evidências anteriores permanecem imutáveis.
Retomada na fase de readiness exige autoridade operacional e gates existentes.

## Revisão SAR

Reconciliação estrutural de 2026-10-07, conforme os charters das Fases B e F. Aprovação humana explícita de 2026-10-08: os campos PASS de B/F neste recorte significam PASS_STRUCTURAL_ONLY; não certificam execução.
B revisa definição, conflitos, critérios/ADRs, requisitos e dependências.
F revisa planejamento por dimensão e não concede autorização de implementação.
Neste passe: IDs, JSON Schema, owner Story/Issue, paths, referências, DAG e
predecessores declarados conferidos; PASS estrutural não é execução técnica.

- **Definição/requisitos:** PASS estrutural; critérios e requisito preservados.
- **Dependências:** PASS estrutural do DAG e da ordem declarada, sem quitação operacional.
- **Review:** PASS estrutural dos papéis requeridos e obrigação de mesmo candidato, sem presumir review de execução.
- **Estado real:** Execução DEFERRED_TO_SPRINT_012; venue NÃO PROVISIONADO. PASS B/F = definição e cadeia de revisão declarada; não atesta hardware, startup, benchmark ou readiness.
- **DEFERRED_ID preservado:** EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS.
- **Gate:** EPIC-108 / GitHub #816 / SPRINT-012 permanece fail-closed.
- **Ownership:** Backend / identity_access funcional; benchmark Security; BC-015 consome/enforce release gate.

## Domain-Driven Design — Fase C

- **Contexto owner:** BC-002, conforme TaskEnvelope e STORY_INDEX existentes.
- **Impacto no modelo:** NONE; nenhum modelo/código de produto alterado.
- **Regra:** boundaries e contratos publicados preservados; sem transferir ownership funcional.
- **Resultado:** PASS estrutural de definição/ownership; não atesta execução ou produção.
