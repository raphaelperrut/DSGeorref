# STORY-0767 / ISSUE-0874 — Definir e aprovar o baseline de execução do BP-003 para throttling

- **Tipo:** `História implementável — prerequisite de decisão`
- **Estado:** `Done` — prerequisite satisfeita no baseline aprovado `4b634381328bd969679abe48ee6936aaf8fe4319`
- **Épico pai:** `EPIC-008`
- **Sprint:** `SPRINT-002`
- **Domínio:** `PLT`
- **Bounded Context:** `BC-002 — Identidade e Controle de Acesso`
- **Papel responsável:** `Arquiteto` — `ROLE-002`
- **TaskEnvelope:** `.codex/tasks/TASK-0770.json`
- **Downstream direto:** `STORY-0762 / ISSUE-0873 / TASK-0769`, executor `Security / ROLE-010`

## Resultado verificável

Definir e aprovar o baseline de execução do BP-003 para throttling: classe de
hardware de referência + workload/threat envelope quantitativo. Uma única decisão
coesa entrega dois perfis compatíveis e sua evidência de aprovação/reprodução.
A decisão foi concluída e aprovada no SHA `4b634381328bd969679abe48ee6936aaf8fe4319`.
Os dois perfis 1.0.0 e o vínculo BP-003 estão integrados; architecture/QA/final
re-review independentes PASS foram confirmados explicitamente pelo usuário.
A reconciliação administrativa está em
`evidence/security/throttling-calibration/readiness-reconciliation-v1.json`.
Hardware é reference_benchmark sem claim minimum_supported; o workload define
somente o experimento. Nenhum benchmark ou política runtime foi promovido.

## Contexto e rastreabilidade

Na baseline `aba94afbadc0a73af09fae5f950192b09bae793e`, TASK-0769 está
estruturalmente correta, mas ambos os insumos são `MISSING_MATERIAL_DECISION`.
TECHNOLOGY_BASELINE.yaml deixa quotas por hardware e throttling evidence-bound;
CAPACITY_AND_SCALING.md exige CPU-only, permite GPU opcional e classifica classes
sem benchmark como UNSUPPORTED. Nenhum deles aprova CPU/RAM/I/O mínimos concretos.
BP-003/AP-003 exigem calibração e resistência a brute force sem DoS operacional,
mas não fornecem workload quantitativo. THREAT_MODEL.md contém ameaças qualitativas.

STORY-0748 / TASK-0748 / EPIC-041 rastreiam REQ-AUTH-IMPL-007, porém os paths de
contratos, design reviews e evidência do slice não existem no checkout reconciliado.
Sua inclusão do requisito não produz um perfil consumível. Permanecem somente
referências; esta prerequisite não os reabre nem modifica.

ISSUE-0874 é registrada localmente por esta história e ISSUE_INDEX; não se presume
número de issue remota. STORY-0763 a STORY-0766 estão reservadas em envelopes
operacionais; STORY-0767 e TASK-0770 evitam colisão com essas identidades.

## Ownership e aprovação mínima

ROLE_AUTHORITY_MATRIX.md atribui arquitetura e escolhas técnicas materiais ao
Arquiteto. ROLE-002 responde por decisões técnicas materiais; ADR-028/ADR-031
mantêm parâmetros quantitativos em profiles/benchmarks. O Arquiteto define o
envelope técnico e threat, e uma autoridade arquitetural independente da autoria
aprova ambos os perfis no mesmo candidato. Ninguém aprova o próprio trabalho.
Security continua executor exclusivo do benchmark TASK-0769. QA verifica
completude/reprodutibilidade documental; Reviewer verifica escopo e rastreabilidade.
Tech Lead libera o consumidor após integração e verificação da prontidão.

OWNER_DECISION_GATE.md exclui sizing e detalhes reversíveis de escalonamento
automático. Project Owner é necessário somente se alternativas materialmente
diferentes criarem ou alterarem uma promessa pública duradoura de hardware mínimo
suportado/compatibilidade, escopo ou semântica de aceitação e satisfizerem todas as
condições desse gate. Nesse caso, registrar dentro desta mesma prerequisite a
decisão específica, alternativas, recomendação, consequências e aprovação explícita.
Não criar outra prerequisite nem um gate adicional de CTO: este recorte não
autoriza investimento ou claim de capacidade/produção. Os gates existentes seguem
vigentes para qualquer claim posterior.

## Outputs exclusivos e allow paths

- `docs/04-quality/benchmark-profiles/BP-003-throttling-hardware-reference.yaml`
- `docs/04-quality/benchmark-profiles/BP-003-throttling-threat-workload.yaml`
- `docs/04-quality/benchmark-profiles/BP-003-security-runtime-calibration.md` — somente referências e aplicabilidade dos dois insumos aprovados
- `evidence/security/bp003-throttling-execution-baseline/**`

Os dois YAML são outputs entregues e aprovados, versão 1.0.0, no SHA
`4b634381328bd969679abe48ee6936aaf8fe4319`; seus bytes permanecem preservados. BP-003 recebe somente o vínculo aos perfis e a
regra de aplicabilidade; não recebe calibração ou política final de throttling.
O escopo acima é o escopo de execução de TASK-0770. A criação desta história,
envelope e sincronização administrativa de índices/grafo e TASK-0769 foi
autorizada separadamente pelo pedido de materialização.

### A) Hardware Reference Profile

Definir arquitetura/classe de CPU e capacidade mínima/de referência necessária;
RAM mínima/de referência; armazenamento e característica de I/O quando material;
GPU explicitamente não requerida para este benchmark, salvo decisão fundamentada
compatível com a baseline CPU-only. Sistema/runtime deve ser pinado somente onde
afeta reprodução, usando a autoridade de TECHNOLOGY_BASELINE.yaml.

Identificar e versionar a classe, unidades, condições e regra de aplicabilidade
dos resultados. Distinguir minimum supported de reference benchmark hardware:
se diferentes, declarar ambos, relação entre eles e quais execuções/limitações
satisfazem BP-003 e o critério de hardware de TASK-0769. Uma classe de referência
aprovada para medir não ganha status de hardware suportado sem benchmark.
Nenhum resultado pode ser extrapolado a classe não avaliada; quotas continuam
EVIDENCE_BOUND. A máquina local ou um exemplo não vira baseline por inferência.
Ambiguidade entre o mínimo requerido por BP-003 e a referência mantém o consumidor
bloqueado até decisão explícita dentro desta prerequisite.

### B) Threat Workload Profile

Identificar operações de autenticação existentes sujeitas à medição, com origem
no contrato congelado, sem criar endpoints ou operações. Fixar padrões de
tentativas legítimas e abusivas, intensidade/rate com unidades, concorrência,
duração e janelas de observação da carga, distribuição de tentativas por
identidade/origem relevante e sequências de brute force/repeated attempts.
Definir geração determinística/replay das entradas, ordem/temporização e seeds
quando houver aleatoriedade, mantendo dados sintéticos sem secrets ou PII reais.

Estabelecer critérios objetivos e verificáveis de resistência ao abuso, ausência
de enumeração/bypass e preservação de pisos/autorização/CSRF; critérios objetivos
de CPU/memória e DoS operacional, incluindo como medi-los e avaliar carga legítima
durante abuso. Valores de planejamento e critérios pertencem a esta decisão e
precisam de fundamento e aprovação explícitos; não derivar números da prosa genérica.
Fixar versão, unidades, vínculo à versão de hardware, protocolo de reprodução,
validade e critérios que exigem nova versão/recalibração. Janelas e taxas de carga
não são windows, cooldowns ou lockouts finais de enforcement.

## Fora de escopo / deny paths

- `src/**`, `tools/**`, `tests/**`, `infra/**`, `.github/**`, `contracts/**`, `**/migrations/**`
- `docs/03-engineering/application-profiles/AP-003-web-security-runtime-profile.md`
- `.codex/tasks/TASK-0769.json`, `.codex/tasks/TASK-0712.json`, `.codex/tasks/TASK-0040.json`, `.codex/tasks/TASK-0748.json`
- `docs/06-delivery/stories/STORY-0748-ISSUE-0858-slice-2-3-definir-politicas-e-contratos-fail-closed-threat-model-validado-scanning-e-t.md`
- `evidence/security/throttling-calibration/**`

Não executar benchmark; não escolher/promover thresholds, windows, cooldowns,
lockout, atraso progressivo ou limites finais de enforcement. Não implementar
throttling, alterar contratos de produto, Argon2id, session timeout ou parâmetros
alheios a REQ-AUTH-IMPL-007. Não criar framework, infraestrutura ou outra prerequisite.

## Dependências e cadeia de desbloqueio

Predecessor: `STORY-0036` — contrato de identidade existente, preservado.

`STORY-0767 / ISSUE-0874 / TASK-0770` blocks
`STORY-0762 / ISSUE-0873 / TASK-0769` blocks
`STORY-0712 / ISSUE-0822 / TASK-0712` blocks
`STORY-0040 / ISSUE-0150 / TASK-0040`.

Todos os predecessores anteriores permanecem. Criar a prerequisite não conclui a
decisão. TASK-0769 permanece bloqueada até ambos os perfis aprovados, versionados
e integrados com aplicabilidade resolvida, handoff e revisões independentes.
A decisão libera somente o planejamento de execução do benchmark; não promove
throttling, não libera STORY-0712 e não conclui o aceite de ISSUE-0150.

## Critérios de aceitação

- [x] AC-ISSUE-0874-01: Hardware de referência aprovado independentemente e versionado, com CPU, RAM, armazenamento/I/O material, GPU, sistema/runtime, identificação da classe, distinção minimum supported/reference e aplicabilidade suficiente para satisfazer o recorte de BP-003/TASK-0769 sem claim de suporte não medido.
- [x] AC-ISSUE-0874-02: Workload/threat profile aprovado independentemente e versionado, com operações existentes, padrões legítimos/abusivos, rate, concorrência, duração/janelas, distribuição brute-force/repeated attempts, critérios objetivos de segurança e CPU/memória/DoS e protocolo de reprodução.
- [x] AC-ISSUE-0874-03: Ambos os perfis possuem unidades, versões e vínculo entre si e determinam todas as entradas de planejamento necessárias; TASK-0769 executa sem escolher novo hardware, carga ou critério de aceitação, preservando a seleção posterior de candidatos de throttling por calibração.
- [x] AC-ISSUE-0874-04: Nenhuma política quantitativa de throttling é promovida, nenhum benchmark é executado, e código, contratos de produto, AP-003, Argon2id, sessões e parâmetros fora de REQ-AUTH-IMPL-007 permanecem intactos.
- [x] AC-ISSUE-0874-05: Handoff identifica exatamente os dois arquivos, versões, SHA-256, candidato/base integrada, aplicabilidade e evidências de aprovação independente que TASK-0769 consumirá; BP-003 referencia os insumos aprovados e registra limitações e rollback.

## Validações e evidência

Verificar parse dos YAML, presença e coerência dos campos/unidades, cobertura dos
critérios, versões/digests e reprodução documental das sequências de carga, sem
executar tentativas de autenticação ou medir runtime. QA verifica que nenhum
parâmetro de planejamento necessário ficou para decisão do executor Security.
Reviewer verifica escopo, ausência de política promovida e aprovação atribuível
ao mesmo candidato. Executar `make verify` antes do handoff e registrar limitações
ambientais sem alterar código/validators para fabricar aprovação.

`evidence/security/bp003-throttling-execution-baseline/` contém fundamento da
decisão, validações, decisões específicas do Owner somente se aplicáveis,
aprovações independentes, limitações e handoff com paths/versões/SHA-256.
Evidência de materialização não é aprovação dos perfis nem resultado de benchmark.

## Compatibilidade e rollback

Sem migration, mudança de produto ou contrato. Perfil rejeitado/alterado invalida
seu handoff; o consumidor permanece bloqueado até uma versão aprovada aplicável.
Preservar evidência revisada e digests; não substituir versão aprovada em silêncio
nem usar a máquina local ou defaults como fallback.

## Condições de parada e prompt

Lacunas de hardware/workload são o objeto explícito desta decisão; devem ser
resolvidas com fundamento e aprovação, nunca por inferência do consumidor.
Parar por contradição de autoridade, necessidade de novo endpoint/contrato,
redução de piso, parâmetros finais de enforcement, claim de suporte sem benchmark,
Owner Decision Gate aplicável sem decisão, colisão de escopo ou falta de aprovação
independente. Não criar uma segunda prerequisite.

Leia AGENTS.md, ROLE-002, esta história, TASK-0770 e as autoridades referenciadas.
Produza somente os dois perfis de execução e sua evidência. Security executará
TASK-0769 depois da integração; não executar seu benchmark nesta tarefa.

## Gates de planejamento

Decisão satisfeita; nenhuma decisão material permanece aberta no baseline de
execução aprovado. Aprovações independentes foram consumidas da confirmação
explícita do usuário para o SHA indicado, sem self-approval ou repetição de gates.
TASK-0769 fica Ready para execução do experimento após integração administrativa.
ISSUE-0873 permanece aberta, ISSUE-0822/0150 bloqueadas e o gate de produção
em minimum_supported não foi satisfeito por hardware reference_benchmark.
