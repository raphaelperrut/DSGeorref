# BP-003 — Security runtime calibration

- **Status:** `Required before production-like readiness`
- **Owner ADR:** ADR-028

Calibrar Argon2id, limites de concorrência, atraso progressivo, janelas, cooldowns, session idle/absolute timeout e thresholds de lockout sob hardware mínimo suportado e threat tests. A promoção deve demonstrar resistência a brute force e ausência de DoS operacional por consumo de memória/CPU.

## Baseline de execução v2 — throttling

STORY-0767 / ISSUE-0874 / TASK-0770 introduziu os dois perfis em `2.0.0`.
A decisão do Owner reduz a reserva de RAM da classe de referência no hardware
`2.1.0`. O workload `2.0.1` atualiza o vínculo com essa classe. O novo par está
`PENDING_INDEPENDENT_REVIEW` e se aplica à próxima calibração após revisão
independente e integração.

- [BP-003-throttling-hardware-reference.yaml](BP-003-throttling-hardware-reference.yaml): hardware `reference_benchmark`, não `minimum_supported`; a aprovação do experimento não declara hardware mínimo suportado ou capacidade geral do produto.
- [BP-003-throttling-threat-workload.yaml](BP-003-throttling-threat-workload.yaml): números de carga e critérios do benchmark, não thresholds, janelas, cooldowns ou lockouts runtime.

A aplicabilidade permanece restrita ao recorte `post_auth_session` e às condições dos perfis. Este vínculo não executa o benchmark nem satisfaz o gate de produção em hardware mínimo suportado. A promoção dos valores finais de throttling continua pertencendo a TASK-0769 / [AP-003](../../03-engineering/application-profiles/AP-003-web-security-runtime-profile.md), após execução e revisão do benchmark.

Versões, digests e handoff são rastreados em `evidence/security/bp003-throttling-execution-baseline/`. Rejeição, alteração ou inaplicabilidade dos perfis invalida o handoff; uma substituição exige nova versão e revisão, sem fallback para hardware local ou defaults.

### Classe reproduzível e controles preservados

CPU x86_64 Intel/AMD, sem SKU/frequência exatos; mínimo de quatro CPUs alocáveis,
com orçamento reservado de quatro (API 2 + PostgreSQL 2). CPUs adicionais não
aumentam o orçamento nem alteram o denominador de aceitação. Afinidade reproduzível
quando disponível; ausência exige mecanismo de reserva/isolamento comprovado.
Registrar clocks/topologia e boost, mantendo a configuração entre repetições;
NUMA somente quando houver controle útil. Não comparar desempenho entre modelos.

Reservar 8 GiB com API <= 2 GiB, PostgreSQL <= 4 GiB e 2 GiB para SO/medição.
Os 8 GiB definem a classe de referência do BP-003, sem requisito de produção.
Os limites efetivos dos cgroups se aplicam junto aos critérios do workload,
incluindo a reprovação por OOM ou falha de alocação.
Swap configurado é permitido, mas paginação/swap material nas janelas invalida a
execução; o profile define observação conservadora por deltas e atribuição,
memory.current e memory.events. OOM continua reprovação. SSD/NVMe local com
100 GiB livres por repetição, filesystem Linux durável e WAL/data com fsync e
commits duráveis; network filesystem e RAM disk permanecem proibidos.

Linux/cgroup v2 continua obrigatório. Windows 11 + WSL2/ext4/VHDX e outras
virtualizações são admitidos com identificação das camadas e recursos reais no
fingerprint; não exigem ext4 no host Windows. Python 3.12.13, PostgreSQL 18.x,
OCI assinado/Compose, locks, TLS/provenance e pisos de segurança são preservados.
O gerador requer domínio de execução separado, com recursos fora da reserva do
target; segundo host físico é opcional. Interferência material CPU/RAM/I/O invalida
a repetição; falta de evidência de isolamento é inconclusive/fail.

O workload 2.0.1 altera apenas a versão, o digest e os vínculos com o hardware 2.1.0.
Taxas, durações, concorrência, fixtures, probes, critérios de aceitação e as três
repetições permanecem iguais aos do workload 2.0.0.
PostgreSQL permanece autoridade; fail-closed, transições persistidas observáveis,
supressão do verifier, proteção contra enumeração e ausência de secrets/PII não são
flexibilizados. Nenhuma política AP-003 é promovida.

Resultados não autorizam claims de hardware mínimo suportado, throughput/capacidade
gerais, equivalência de CPUs ou SLO de produção. A obrigação
`EPIC-008-REQ-AUTH-IMPL-007-PRODUCTION-READINESS` permanece aberta; os registros
históricos de indisponibilidade da v1 não são defeitos nem atestação atual da v2.

### Histórico e rollback

A v1.0.0 foi aprovada no SHA `4b634381328bd969679abe48ee6936aaf8fe4319`, conforme
`evidence/security/throttling-calibration/readiness-reconciliation-v1.json`.
Seus artefatos e aprovações permanecem históricos e válidos para aquela versão.
Rollback documental recupera os três arquivos BP-003 desse SHA em uma mudança
revisada e restaura seus vínculos/digests v1 como conjunto. Isso restaura também
suas restrições de venue; não autoriza executar v1 em hardware v2 incompatível.
Os candidatos e evidências da TASK-0772 vinculados ao hardware 2.0.0 permanecem
históricos. O hardware 2.1.0 exige nova qualificação do venue e novo fingerprint.
A calibração exige três novas repetições no mesmo ambiente concreto.
