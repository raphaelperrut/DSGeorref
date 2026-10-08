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

Provisionar e evidenciar host Linux e gerador separado que correspondam integralmente ao hardware reference profile aprovado de BP-003, com runtime PostgreSQL/backend reproduzível, manifest e handoff de readiness para TASK-0769, sem executar benchmark.

O hardware profile 1.0.0 aprovado no SHA 4b634381328bd969679abe48ee6936aaf8fe4319 é imutável nesta lane. Usar exatamente AMD EPYC 7313P, quatro cores físicos dedicados, uma thread usada por core sem siblings SMT compartilhados, boost desabilitado, 3000 MHz nominal e afinidade/NUMA do spec. API usa dois cores e PostgreSQL outros dois. Alocar 16 GiB com limites/reservas, cgroup v2, swap e I/O como definidos no profile; GPU não requerida.

Provisionar NVMe local dedicado/ext4, pelo menos 100 GiB livres por repetição e durabilidade WAL/data/commits sem redução, isolando outros workloads. Gerador separado não pode consumir os quatro cores/16 GiB do venue. Manifest e comprovantes devem abranger todos os campos do spec, incluindo os que não foram resumidos aqui. Nenhuma proposta substitui o hardware exato por equivalência informal.

Usar artifacts existentes e aprovados para PostgreSQL/backend e registrar seus digests, locks, config, contrato, perfis de segurança já existentes e startup/readiness reais. Não inventar backend/imagem/runtime aprovado. A lane pode iniciar alocação e attestation do host independentemente da decisão de grafo; não consome outputs da outra prerequisite nem gera o lock Python. Se faltar artifact de runtime necessário ao handoff completo, registrar o blocker operacional e não concluir esta tarefa com evidência somente de host. O preflight consolidado de TASK-0769 exige o uv.lock efetivamente materializado por DevOps com scope autorizado; aprovação do grafo e attestation de host não o substituem.

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

## Dependências e isolamento

Predecessores: `STORY-0036`, `STORY-0767`.

STORY-0768 / ISSUE-0875 / TASK-0771 e STORY-0769 / ISSUE-0876 / TASK-0772 são paralelas: nenhuma depende da outra e seus write scopes são disjuntos. Ambas bloqueiam STORY-0762 / ISSUE-0873 / TASK-0769, que bloqueia STORY-0712 / ISSUE-0822 e depois STORY-0040 / ISSUE-0150. STORY-0239 não vira predecessor; seu caminho já é downstream e produziria ciclo. STORY-0767 aprovada permanece satisfeita; não se altera a semântica ou o conteúdo do benchmark.

## Requisitos e ADRs

REQ-AUTH-IMPL-007; downstream REQ-AUTH-IMPL-007.
ADRs: ADR-006, ADR-007, ADR-008, ADR-009, ADR-028, ADR-031, ADR-033, ADR-034. Sem nova ADR nesta decomposição.

## Critérios de aceitação

- [ ] AC-ISSUE-0876-01: Venue real identificado, acesso operacional e autorização de uso registrados sem secrets, host Linux conforme o profile 1.0.0 aprovado no SHA 4b634381328bd969679abe48ee6936aaf8fe4319; nenhum hardware equivalente ou claim minimum_supported.
- [ ] AC-ISSUE-0876-02: Evidências objetivas completas do profile: AMD EPYC 7313P x86_64, quatro cores físicos dedicados, threads/SMT/boost/clocks/afinidade/NUMA conforme spec, 16 GiB e limites/reservas cgroup, sem swap/overcommit; configuração observada corresponde aos requisitos, sem valores presumidos.
- [ ] AC-ISSUE-0876-03: NVMe local dedicado, ext4, espaço livre, WAL/data, fsync/commits duráveis e ausência de contenção/quota conforme profile; manifest registra identidade/settings/I/O e comprovantes atribuíveis ao venue.
- [ ] AC-ISSUE-0876-04: PostgreSQL/backend executáveis por artifacts imutáveis existentes e bindings aprovados, Python 3.12.13, OCI assinado/Compose/cgroup v2, processo/CPU/RAM/isolamento e TLS/provenance conforme profile; gerador em host separado e condições reproduzíveis para três repetições, sem executar a carga BP-003.
- [ ] AC-ISSUE-0876-05: Provisioning/reproduction instructions, hardware/runtime manifest e checks de startup/readiness sem benchmark possuem comandos, resultados reais, versões/digests e candidate SHA; revisão técnica Arquiteto, QA e Reviewer independentes no mesmo candidato validam correspondência integral e handoff exato para Security/TASK-0769. Evidência parcial não conclui a prerequisite.

## Validações e evidência

- Conferir venue manifest campo a campo contra o hardware profile aprovado, distinguindo requisitos de observações e comprovando CPU/SMT/boost/NUMA/cgroups/RAM/NVMe/ext4/durabilidade.
- Reproduzir provisionamento/readiness com target autorizado, registrar comandos/saídas reais e digests, isolamento e rollback; nenhum traffic loop, fase ou medição de BP-003.
- Validar startup/conectividade/durabilidade do PostgreSQL/backend e gerador separado usando bindings aprovados; falta de runtime/lock/perfil/assinatura é BLOCKED, sem fallback.
- Arquiteto/QA/Reviewer independentes validam o mesmo candidate SHA e handoff; conferir diff sem código de produto, alteração de profiles ou políticas runtime; make verify antes do handoff.

Evidência: `evidence/operations/bp003-throttling-venue/`. Required roles: DevOps, Arquiteto, QA, Reviewer. Aprovações independentes no mesmo candidate SHA, com identidade/role/evidência atribuíveis; não basta autoemitir PASS ou reutilizar review de outro candidato. Perfis existentes são lidos por digest; evidências revisadas são append-only.

## Handoff, rollback e parada

Handoff identifica outputs exatos, versões/SHA-256/candidate SHA, limites e comandos de reprodução; o consumidor mantém BLOCKED se faltar lock, venue ou runtime/observáveis exigidos. Sem migration ou mudança de contrato de produto. Rejeição invalida o handoff e preserva o blocker, sem defaults silenciosos. Parar por autoridade contraditória, necessidade de ampliar escopo, entrada operacional ausente ou aprovação independente faltante.

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
