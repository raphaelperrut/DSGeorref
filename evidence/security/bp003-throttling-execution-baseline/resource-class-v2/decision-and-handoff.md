# BP-003 v2.0.0 — decisão de classe de recursos e handoff

Data: 2026-11-14, America/Sao_Paulo. Autor: ROLE-002 Arquiteto.
STORY-0767 / ISSUE-0874 / TASK-0770.
DEFERRED_ID: EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS.
BASELINE_SHA: 5d465868b23e283f3baed530c98931322cc839ed.
Branch: codex/issue-0874-bp003-v2. Estado: PENDING_INDEPENDENT_REVIEW.

## Autoridade, decisão e alternativas

O Owner autorizou explicitamente nesta execução a mudança material do hardware
profile para 2.0.0: classe x86_64 Intel/AMD reproduzível, virtualização/WSL2
permitidos, recursos reservados e gerador em domínio separado, mantendo controles
de segurança. Isso autoriza a revisão, não constitui aprovação independente dos
bytes produzidos. Não há nova ADR estrutural: PostgreSQL, trust boundaries,
contrato de autenticação, OCI/Compose e owners permanecem os existentes.

Alternativa v1: SKU e cores físicos fixos, NVMe/ext4 e gerador em segundo host.
Foi uma decisão aprovada e válida para aquele experimento, preservada no Git.
Alternativa escolhida pelo Owner para a próxima calibração: classe de recursos
com manifestação concreta e reservas reproduzíveis; reduz dependência de venue,
sem comparar CPUs ou atribuir suporte/capacidade a uma classe sem medição.
Trade-off: maior variabilidade ambiental exige evidência de isolamento, camadas
de virtualização e interferência. Um perfil elegível pode reprovar o benchmark;
a revisão não garante desempenho nem operacionaliza o notebook.

O workload também passa a 2.0.0 porque referencia a versão do hardware dentro de
spec, além do companion. Nenhuma intensidade, janela, duração, fixture, concorrência,
critério de segurança/serviço/recursos, probe ou protocolo de três repetições muda.
Os novos digests não representam nova política de throttling.

## Decisões concretas de reprodução

| Dimensão | Regra v2 e fundamento |
|---|---|
| CPU | >= 4 CPUs lógicas/vCPUs disponíveis; reserva de referência 4, API 2 + PostgreSQL 2. Preserva o denominador e o limite de CPU do workload v1. Sem SKU ou clock nominal; clocks reais observados, boost configurado constante, topologia registrada. |
| Afinidade/NUMA | Afinidade reproduzível quando disponível; fallback deve comprovar reserva/isolation equivalente em orçamento, sem equivalência entre CPUs. NUMA aplicado somente com controle útil exposto; registrar motivo de não aplicabilidade. Não declarar isolamento com quota isoladamente. |
| RAM | >= 16 GiB disponíveis/reserváveis; orçamento de referência 16 GiB: API <= 4, PostgreSQL <= 8, SO/medição 4. Tetos medidos de aceite API 3/DB 7/soma 10 GiB permanecem os da v1, distintos dos limites cgroup. Sem OOM/overcommit que inviabilize a reserva. |
| Swap | Permite swap configurado. Regra conservadora de materialidade: qualquer swap-in/out atribuível ao target ou crescimento de memory.swap.current durante a janela é material. Sem atribuição, exigir zero swap-in/out e zero crescimento no ambiente. Registrar uso inicial, deltas, memory.current, memory.events e paging; ausência de telemetria não passa. |
| Storage | SSD/NVMe local, >=100 GiB livres antes de cada repetição, WAL/data duráveis, fsync/commits preservados. ext4 em VHDX sobre SSD/NVMe local é elegível; tipo do filesystem Windows não determina sozinho a elegibilidade. Evidenciar backing/mounts/durabilidade; rede/RAM disk proibidos. |
| Interferência | Nenhuma disputa intencional. Contenção CPU/RAM/I/O material invalida a repetição. I/O concorrente que atrasa trabalho ou impede critérios é material; ausência de evidência para excluir interferência é inconclusive/fail. Manter observação host/guest/target/generator, sem inventar novo limiar quantitativo de segurança. |
| Gerador | Domínio separado: outro host/VM ou cgroup/cpuset/reservas comprovadamente isolados, fora dos 4 CPUs/16 GiB reservados ao target. Mesmo host precisa de recursos adicionais e evidência CPU/RAM/I/O; nome de container distinto não prova isolamento. |
| Fingerprint | Fixar configuração concreta de CPU/reservas/boost/afinidade ou fallback/NUMA, RAM/cgroups, storage e camadas host/guest/WSL, runtime/locks/digests/configuração, contrato/policy/fixtures e gerador. Dados dinâmicos como clocks e deltas são observações de cada repetição, não configuração a exigir igualdade byte a byte. |

Não existe claim de minimum supported, throughput/capacidade gerais, equivalência
ou comparação de CPUs ou SLO de produção. O limite de 80%/janela continua sendo
rejeição experimental, e não promessa de produto.

## Segurança e limites de escopo

O validador compara integralmente o spec do workload com a baseline e permite
somente hardware_profile_version=2.0.0. Isso preserva exatamente:

- unauthorized_successes=0, invalid credential mutations=0 e denied guard bypasses=0;
- PostgreSQL atômico como autoridade, transição persistida open -> limited/locked
  correlacionada e supressão mensurável do password verifier;
- critérios de enumeração, pisos Argon2id/session e redaction sem secrets/PII;
- persistence/restart probes e PostgreSQL indisponível => internal_error/fail-closed;
- serviço legítimo durante abuso, CPU/memória, OOM/crash/storage/commit failures;
- três repetições individualmente aprovadas, sem médias escondendo falhas;
- missing evidence => inconclusive/fail.

AP-003, src, tests, contracts, infra, migrations, locks, workflows e política
runtime permanecem intactos. Não houve workload, benchmark, autenticação de teste,
provisioning ou nova inspeção de hardware nesta tarefa.

## Notebook: elegível em princípio, venue não atestado

Entradas fornecidas pelo Owner nesta solicitação, sem nova medição:

| Entrada | Compatibilidade teórica |
|---|---|
| Intel Core i7-14650HX, 16 cores/24 logical processors | Intel x86_64 permitido, quantidade nominal suficiente para 4 CPUs target e recursos adicionais; reserva real e afinidade por verificar. |
| RAM 34081755136 bytes | Acima de 16 GiB; WSL/VM deve receber memória disponível/reservável suficiente além das necessidades do gerador e do host. |
| Dois NVMe ~512 GB, um com >200 GB livres | Meio e espaço nominais compatíveis; conferir >=107374182400 bytes no filesystem Linux efetivo e backing local do VHDX antes de cada repetição. |
| Windows 11 Pro x64 + WSL2 disponível | Classe host/guest admitida; Linux/cgroup v2, limites, versões, durabilidade e interferência ainda precisam de evidência. |

NOTEBOOK_ELIGIBLE_IN_PRINCIPLE=YES. VENUE_READY=NOT_ATTESTED.
Não se herdam resultados do hermes ou do Windows da TASK-0772 como configuração
atual do notebook. WSL instalado/disponível não prova runtime, memória alocada,
isolamento ou autorização de execução. O gerador local só é elegível se ficar
fora da reserva, incluindo recursos adicionais e ausência de interferência material.

## Artefatos, histórico e rollback

Os dois paths canônicos continuam os mesmos; versões 2.0.0 e SHA-256 canônicos
estão em validation.json, com raw file SHA-256 UTF-8/LF. artifact-manifest.json
fixa também o documento BP-003 e os inputs normativos, por bytes Git da baseline.
O candidate SHA é o commit contendo este pacote e os três arquivos BP-003.

A aprovação histórica v1.0.0 permanece no SHA
4b634381328bd969679abe48ee6936aaf8fe4319, consumida da confirmação explícita do
usuário em evidence/security/throttling-calibration/readiness-reconciliation-v1.json.
Evidências históricas architecture-decision-v1.yaml, candidate-handoff-v1.yaml,
execution-artifact-manifest-v1.json, focused-structural-checks-v1.json e
normative-link-handoff-v2.json não foram editadas. O último nome v2 refere-se ao
handoff normativo histórico, não aos novos profiles 2.0.0.

Rollback: recuperar conjuntamente os três arquivos BP-003 do SHA aprovado v1
em mudança revisada (`git restore --source=4b634381328bd969679abe48ee6936aaf8fe4319
-- <três paths BP-003>`), verificar seus dois digests canônicos e companions e
restabelecer o handoff v1. Nunca misturar workload/hardware/resultados de versões
diferentes. A reserva v2 não satisfaz automaticamente as restrições exatas v1.
Preservar este pacote de evidência no histórico; não apagar aprovações ou resultados.

## Validação e handoff

Comando documental reproduzível:
`python evidence/security/bp003-throttling-execution-baseline/resource-class-v2/validate_profiles.py`.
Python usa somente leitura de Git/documentos e escreve validation.json neste
diretório. Verifica parse sem chaves duplicadas, versões, companions, digests,
igualdade integral do workload salvo referência de hardware, pins/pisos preservados,
TaskEnvelope/schema, identidade/índice/DAG/dependências, escopo e whitespace.
Não existe schema normativo próprio para os profiles nas entradas; a validação
não inventa certificação de schema. Inspeção documental adicional cobre WSL2,
virtualização, isolamento, materialidade, claims e rollback descritos acima.

`make verify` foi tentado conforme TASK-0770: exit 2 no primeiro passo,
`No module named ruff` no Python miniforge3 do ambiente. make-verify.log preserva
o output. Nenhuma investigação de ruff/EPERM, instalação ou correção fora de escopo.
Não se declara o gate global verde ou etapas posteriores executadas.

BLOCKER_FINDINGS=0 e HIGH_FINDINGS=0 na verificação documental do autor; não são
pareceres independentes. Aprovação arquitetural independente, QA documental e
Reviewer ainda PENDING no mesmo candidate SHA. A autorização do Owner para mudar
o profile não substitui essas revisões existentes.

READY_FOR_INDEPENDENT_REVIEW=YES. READY_TO_RETRY_TASK_0772=NO até aprovação e
integração v2. Após isso, o dispatch autorizado da TASK-0772 deve vincular
explicitamente os profiles/digests 2.0.0 e substituir a aplicabilidade das cláusulas
v1 (SKU/core físico/segundo host) em seus inputs históricos, sem editar envelopes
fora desta lane. A nova inspeção real/readiness é responsabilidade da TASK-0772;
nenhum resultado operacional é antecipado aqui. Não é uma nova prerequisite.

TASK-0769 não é liberada: falta venue/runtime e permanecem os gates independentes.
O registro canônico da obrigação é preservado sem edição por estar fora do escopo;
suas referências de v1 continuam históricas e a autorização atual determina esta
revisão v2. A obrigação production-readiness e seus controles continuam abertos.
Não há aprovação de produção, promoção AP-003, calibração ou implementação de
throttling. Nenhum review de outro papel é emitido pelo autor.
