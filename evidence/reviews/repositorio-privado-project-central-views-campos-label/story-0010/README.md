# ISSUE-0120 — evidência executável de aceite

Este diretório é o locator canônico da evidência versionada da `STORY-0010`.
Ele normaliza o locator legado `evidence/reviews/epic-002/story-0010/` para o
subtree autorizado da capacidade, sem alterar contratos, testes, ferramentas,
workflow ou TaskEnvelope.

## Evidência por critério

| Critério | Evidência executável reutilizada |
|---|---|
| `AC-ISSUE-0120-01` | contratos congelados, consolidação, automação e integração read-only do `EPIC-002` |
| `AC-ISSUE-0120-02` | lineage dos slices, TaskEnvelopes, owners e rastreabilidade de requisitos verificados pelas suites existentes |
| `AC-ISSUE-0120-03` | casos negativos determinísticos de contrato, consolidação, automação, integração e DAA |
| `AC-ISSUE-0120-04` | DAA verifica TaskEnvelope, candidate SHA e independência entre Executor, QA e Reviewer |

Os entrypoints públicos exigidos são:

- `test_epic_002_aceite_happy_path`;
- `test_epic_002_aceite_negative_paths`.

Eles carregam e executam as suites canônicas por referência. Nenhuma regra de
contrato, integração, rastreabilidade ou aprovação é copiada para este bundle.
O caminho nominal cobre o contrato de consolidação, a consolidação executável,
a automação, a integração e a Delivery Approval Authority. O caminho negativo
repete as superfícies fail-closed e inclui todos os probes de consolidação
aplicáveis.

## Candidate SHA e independência

O bundle não contém SHA tracked. A Delivery Approval Authority existente recebe
o candidate SHA esperado do gate chamador e o compara com as attestations
assinadas. Seus probes negativos rejeitam TaskEnvelope divergente, replay ou
digest inválido, candidate SHA divergente ou replayado, identidade ou role
divergente, aprovação ausente/rejeitada e sobreposição de accountable subjects.

Esta evidência não declara aprovação. Attestations reais de Executor, QA e
Reviewer devem ser emitidas posteriormente por sujeitos independentes para o
mesmo TaskEnvelope, candidate SHA, conjunto de evidências e riscos residuais.

## Impacto e rollback

Contratos compartilhados, ADRs, produção, banco, migrations, API, frontend,
geoprocessamento, IA, broker e workflow permanecem inalterados. O rollback é a
reversão deste bundle de evidência; não existe migração ou ação destrutiva.
