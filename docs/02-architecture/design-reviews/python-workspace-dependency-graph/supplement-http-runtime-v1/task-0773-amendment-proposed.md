# Proposta de emenda mÃ­nima futura â€” TASK-0773

PROPOSTA NÃƒO APLICADA. NÃ£o altera `.codex/tasks/operations/TASK-0773.json`, seus allow_paths, a Story ou seus estados. Executabilidade atual: **NO**. Somente apÃ³s fechamento tÃ©cnico e aprovaÃ§Ã£o independente do commit candidato deste suplemento poderÃ¡ o Owner/Tech Lead autorizar a emenda administrativa e, separadamente, sua execuÃ§Ã£o.

Substituir somente as referÃªncias operacionais que presumem consumo exclusivo do graph histÃ³rico (outcome, references, acceptance_criteria, tests, evidence e stop_conditions e seus espelhos de planejamento, se ainda aplicÃ¡veis) para consumir a composiÃ§Ã£o abaixo. A aprovaÃ§Ã£o histÃ³rica permanece imutÃ¡vel e nÃ£o se estende ao novo candidato.

```text
HISTORICAL_APPROVED_GRAPH_SHA = cb198c9e8340e0675c36679de426abf922e1c569
CURRENT_BASELINE_SHA = 051ed667565bdce1eb22745aee35861a6d4be119
SUPPLEMENT_CANDIDATE_SHA = commit Git que contÃ©m estes blobs; SHA exato entregue no handoff final
APPROVED_SUPPLEMENT_SHA = preencher somente com esse candidato depois de revisÃ£o independente
FINAL_EXPECTED_DISTRIBUTION_COUNT = 54
FINAL_EXPECTED_DIRECT_ROOT_COUNT = 14
FINAL_EXPECTED_TRANSITIVE_COUNT = 40
FINAL_EXPECTED_CONSTRAINT_COUNT = 39
SUPPLEMENT_CANDIDATE_MANIFEST_SHA256 = 90060e4bb44e82bb35cf7e32a66d653a876ce365ef8bb7ea136405d5a7198ac5
PYPROJECT_PROPOSED_SHA256 = 45afa84044f47c12ab6e011e77834d48df327655d9f4d59625f63e9ecaee8a01
CHECKER_SUPPLEMENT_SHA256 = 7458d3ccc44334725f84ab92adfcfbe25f613e7fc2f025e8859eab27c8fcd65e
CPYTHON_ARTIFACT_SOURCE = astral-sh/python-build-standalone
CPYTHON_ARTIFACT_RELEASE = 20260602
CPYTHON_ARTIFACT_ID = 436827047
CPYTHON_ARTIFACT = cpython-3.12.13+20260602-x86_64-unknown-linux-gnu-install_only.tar.gz
CPYTHON_ARTIFACT_SHA256 = 9be5c21b78dbc371e739bc7faf3b007b8e607335f780bdd2e0dd44a6e3580d76
CPYTHON_RECORD_SHA256 = 939bf190e36a00246f2e6a90c16503e6acdec8033fd0499388626b356ffddb55
CPYTHON_DESTINATION = /usr/local/bin/python3.12
CPYTHON_SYS_BASE_PREFIX = /usr/local
PYTHON = CPython 3.12.13 / Linux amd64 / glibc>=2.28 / fora de Conda
UV = 0.12.19 / bootstrap e digest histÃ³ricos preservados
```

O digest do manifest acima Ã© o identificador de conteÃºdo candidato, sem referÃªncia circular ao prÃ³prio digests.json. O digest do pacote completo Ã© o SHA-256 de digests.json, entregue junto com o SHA Git no resultado final; a revisÃ£o deve vincular ambos. O manifest de digests vincula todos os artifacts novos e source-inputs.json. NÃ£o preencher APPROVED_SUPPLEMENT_SHA com o histÃ³rico nem interpretar o autor como aprovador.

Autoridades novas a adicionar por referÃªncia:

- `docs/02-architecture/design-reviews/python-workspace-dependency-graph/supplement-http-runtime-v1/supplement.json` e rationale.md;
- o handoff `supplement-devops-handoff.md` nesse mesmo diretÃ³rio, substituindo os passos que sÃ³ cobriam 43 distribuiÃ§Ãµes;
- `evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1/resolution-delta.json`, pin-reconciliation.json, constraints-delta.txt, source-inputs.json e digests.json;
- `supplement-pyproject-proposed.toml` nessa evidÃªncia como autoridade completa da cÃ³pia futura sobre o pyproject raiz;
- `check-supplement.py` nessa evidÃªncia como checker da composiÃ§Ã£o/lock e composer dos inputs; checker histÃ³rico fica imutÃ¡vel e nÃ£o valida o conjunto novo;
- `cpython-artifact.json`, cpython-attestations.json e cpython-provenance-verification.json como autoridade externa prÃ©via do interpreter. Provisionar `/usr/local` requer autorizaÃ§Ã£o operacional separada, nÃ£o se torna write scope da TASK-0773.

Preservar literalmente:

```json
"allow_paths": [
  "pyproject.toml",
  "uv.lock",
  "evidence/operations/python-workspace-lock/**"
]
```

Manter deny_paths para cÃ³digo, manifests requirements, graph/evidÃªncia arquitetural e infra. Os inputs compostos do composer serÃ£o registrados exclusivamente sob evidence/operations/python-workspace-lock/** no futuro passe. O registry canÃ´nico externo conserva o binding histÃ³rico e precisa ser preparado por operador autorizado, sem modificar artifacts arquiteturais.

A emenda exige primeiro confirmaÃ§Ã£o independente da precedÃªncia explÃ­cita dos pins runtime/validaÃ§Ã£o, da escolha Pydantic e da fonte standalone, alÃ©m de fechamento dos checks pertinentes. NÃ£o amplia a tarefa para API/TLS, imagens, release infra, benchmark, AP-003 ou throttling. Exigir reproduÃ§Ã£o independente de uv.lock e frozen sync com os mesmos inputs, checks de integridade e registro real dos testes de compatibilidade; nÃ£o atribuir os ensaios do adapter antigo Ã s versÃµes reconciliadas. Stop conditions devem falhar por qualquer diferenÃ§a de artifact/pin/metadata/runtime, sem decisÃµes ad hoc.

LimitaÃ§Ã£o presente: make verify foi tentado e nÃ£o passou por ausÃªncia de ruff no ambiente de checks. A proposta estÃ¡ escrita para revisÃ£o, mas a emenda e sua aplicaÃ§Ã£o permanecem condicionadas aos gates independentes; nÃ£o hÃ¡ autorizaÃ§Ã£o de execuÃ§Ã£o neste documento.
