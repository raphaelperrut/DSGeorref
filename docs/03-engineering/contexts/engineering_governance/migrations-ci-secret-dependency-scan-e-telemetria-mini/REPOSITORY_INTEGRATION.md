# Integração da capacidade no repositório

`repository_integration.py` é o gate executável da `ISSUE-0134`. Ele compõe os
contratos e controles já publicados pelas histórias predecessoras sem
reimplementar suas regras: o validator de quality é executado em subprocesso
read-only e precisa retornar relatório `DRY_RUN`, sem findings nem ações
destrutivas.

O gate confirma:

- identidade, dependências, ownership, escopo, migration/rollback e os quatro
  testes obrigatórios do `TASK-0024`;
- a hierarquia explícita entre batch/job, imagem, tentativa e work unit por meio
  dos contratos versionados de Job, Attempt e TaskEnvelope e do relatório por
  imagem;
- checkpoints canônicos sob autoridade PostgreSQL, migrations versionadas no
  fluxo expand–migrate–contract e rollback fail-closed;
- homografia projetiva e `USAC_MAGSAC` como combinação canônica, encapsulada e
  sem fallback silencioso;
- o resultado da automação de CI, secret/dependency scan e telemetria publicada
  pela `STORY-0023`.

Execução focada:

```text
py -3.12 -X utf8 tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/repository_integration.py --repository-root .
py -3.12 -m pytest -q -p no:cacheprovider tools/governance/migrations-ci-secret-dependency-scan-e-telemetria-mini/test_repository_integration.py
```

O gate falha com códigos estáveis quando um documento está ausente ou inválido,
o TaskEnvelope sofre drift, a hierarquia perde lineage, checkpoints deixam de
ser canônicos, a política de migration/rollback se torna permissiva, o baseline
científico admite outro estimador ou fallback, ou o control plane retorna saída
malformada ou falha.

Esta integração não altera schema, estado persistido, contrato compartilhado ou
deployment. A obrigação de migration/rollback do envelope é atendida pela
validação executável da política existente; não há migration de dados a aplicar
neste diff. O rollback operacional do candidato é sua reversão antes do consumo.
Depois da fase contract, vale o forward fix ou restore coordenado já congelado na
matriz de versões.

QA sentinela e Reviewer ainda devem avaliar o mesmo commit candidato. Este
handoff não declara aprovação independente.
