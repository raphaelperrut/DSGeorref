# ISSUE-0115 — evidência executável de aceite

Este diretório é o locator canônico da evidência versionada da `STORY-0005`.
Ele normaliza o locator legado `evidence/reviews/epic-001/story-0005/` para o
subtree autorizado da capacidade, sem alterar contratos, testes, ferramentas ou
o TaskEnvelope.

## Evidência por critério

| Critério | Evidência executável reutilizada |
|---|---|
| `AC-ISSUE-0115-01` | contrato congelado, validator e integração do `EPIC-001` |
| `AC-ISSUE-0115-02` | manifest de contrato, TaskEnvelope e grafo verificados pelas suites existentes |
| `AC-ISSUE-0115-03` | casos negativos determinísticos de contrato, automação, integração e DAA |
| `AC-ISSUE-0115-04` | DAA verifica TaskEnvelope, candidate SHA, completude e independência entre Executor, QA e Reviewer |

Os entrypoints públicos são:

- `test_epic_001_aceite_happy_path`;
- `test_epic_001_aceite_negative_paths`.

Eles carregam e executam as suites canônicas por referência. Nenhuma regra de
contrato, integração ou aprovação é copiada para este bundle.

## Candidate SHA e independência

O bundle não contém SHA tracked. A Delivery Approval Authority existente recebe
o candidate SHA esperado do gate chamador e compara esse valor com as
attestations assinadas. Seus probes negativos rejeitam TaskEnvelope divergente,
replay ou digest inválido, candidate SHA divergente ou replayado, identidade ou
role divergente, aprovação ausente/rejeitada e sobreposição de accountable
subjects.

Esta evidência não declara aprovação. Attestations reais de Executor, QA e
Reviewer devem ser emitidas posteriormente por sujeitos independentes para o
mesmo TaskEnvelope e candidate SHA.
