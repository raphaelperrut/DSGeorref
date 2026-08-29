# ISSUE-0125 — evidência executável de aceite

Este diretório é o locator canônico da evidência versionada da `STORY-0015`.
Ele normaliza o locator legado `evidence/reviews/epic-003/story-0015/` para o
subtree autorizado da capacidade, sem alterar contratos, testes, ferramentas,
workflow ou TaskEnvelope.

## Evidência por critério

| Critério | Evidência executável reutilizada |
|---|---|
| `AC-ISSUE-0125-01` | contrato, fundação, automação e integração read-only do `EPIC-003` |
| `AC-ISSUE-0125-02` | evidência de `REQ-DEL-001`, `REQ-DEV-001` e `REQ-TOP-001` nas suites owner |
| `AC-ISSUE-0125-03` | casos negativos determinísticos de contrato, fundação, automação, integração e DAA |
| `AC-ISSUE-0125-04` | DAA verifica TaskEnvelope, candidate SHA e independência entre Executor, QA e Reviewer |

Os entrypoints públicos exigidos são:

- `test_epic_003_aceite_happy_path`;
- `test_epic_003_aceite_negative_paths`.

Eles carregam e executam as suites canônicas por referência. Nenhuma regra de
contrato, fundação, integração, rastreabilidade ou aprovação é copiada para
este bundle. O caminho nominal cobre contrato congelado, fundação executável,
automação, integração e Delivery Approval Authority. O caminho negativo cobre
drift de contrato, fallback silencioso, falhas determinísticas dos controles e
as rejeições fail-closed da autoridade de aprovação.

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
