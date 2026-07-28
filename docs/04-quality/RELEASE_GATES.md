# Release gates

| Gate | Evidência mínima | Estado |
|---|---|---|
| G0 Governance | decisões estruturais, portfólio canônico e políticas aprovados; materialização do GitHub e autorização registradas; licença/citação obrigatórias antes de G6 | `BLOCKED_EXTERNAL` |
| G1 Foundation | SprintEvidenceSet aprovado, Project/forms/ruleset ativos, monorepo greenfield, CLI/API/Web mínimos, CI, migrations, contratos, fluxo diagnóstico e bootstrap reproduzível | `BLOCKED` |
| G2 Access | autenticação quando exposta, autorização, administração, audit trail append-only e proteção de diretórios | `BLOCKED` |
| G3 Data | workspace, banco, COG/ArtifactSet imutáveis, lineage, manifests, BackupSet coordenado, retenção e GC reference-aware | `BLOCKED` |
| G4 Geo/AI | corpus multiépoca e estratificado, splits separados, portfólio neural por estágios, Promotion Gate de ModelPacks, máscara analítica sem recorte, preservação de resolução, ProcessingPlan, Strong Geometric Verifier fail-closed, QualityProfiles, relatórios por imagem e revisão | `BLOCKED` |
| G5 Security | threat model, redaction testada, audit trail protegido, scanners, SBOM, providers sem compra e testes ofensivos | `BLOCKED` |
| G6 Publication | licença, citação, sanitização, documentação, riscos e status honesto | `BLOCKED` |
| G7 Stable Release | SLO, OpenTelemetry e dashboards validados, budgets de cardinalidade, benchmarks de lotes 40/100/300 e catálogo em escala, restore drill aprovado com RPO/RTO, painel de triagem, exports streaming, UX guiada, tutorial visual, runbooks, rollback e suporte | `BLOCKED` |

`PASS` exige evidência versionada. Documento ou intenção isolada não constitui evidência.


Para G4/G7, runners e pipelines heterogêneos exigem `DeterminismProfile`, nível de equivalência comprovado, `ScientificReproducibilityRecord`, baselines estratificados, seleção por impacto e `ScientificPipelineBundle` conforme ADR-053. Compatibilidade de schemas, migrations, artifacts históricos e downgrade seguro seguem ADR-026. Rollout, controle exclusivo, cutover e recuperação seguem ADR-026. Instalação, bootstrap, readiness e suporte seguem ADR-034 e ADR-054. Licença, contribuição, rights manifests e citação seguem ADR-034, ADR-047 e a política de citação e alimentam G0/G5/G6. As regras da governança e de AP-008 fecham a fase fundacional, autorizam somente a SPRINT-001 e mantêm o programa de decisões do portfólio. As regras do modelo operacional do GitHub definem o inventário e a previsão de issues; as regras do modelo operacional do GitHub definem sua governança operacional. Isso não altera os estados `NO_GO` de funcionalidade, publicação ou produção.

## Gate pré-implementação

Antes de qualquer commit funcional, o `ImplementationAuthorizationRecord` deve provar baseline, Project, ruleset, owner, WIP e blockers. Este gate não cria ADR e não substitui G1; apenas autoriza o início da SPRINT-001.

## Gate de integridade do planejamento do portfólio

Antes de uma onda entrar em `Ready`, validar regras do modelo operacional do GitHub: horizonte e milestone coerentes, dependências/gates satisfeitos, WIP e capacidade admissíveis, owner/reviewers definidos, contratos cross-domain exercitáveis e snapshot de forecast preservada.

## Cutover Foundation → primeira fatia funcional — AP-008

A aprovação documental de AP-008 não altera G1 para `PASS`. G1 somente muda após execução real e aprovação do `SprintEvidenceSet`. AP-009 define o conteúdo da primeira fatia autorizável depois desse evento; não autoriza alpha, beta, publicação ou produção.

## Gate da primeira fatia — AP-009

A aprovação documental de AP-009 não executa o gate. Após Foundation Gate real, a fatia deverá provar corpus positivo/negativo/adversarial, equivalência de runners, SGV, COG, provenance, segurança e budget. A IA do AP-009 só poderá afetar resultados oficiais depois dos gates específicos definidos por AP-010.

## Gate da escada neural

ModelPacks e políticas de escalonamento somente podem ser promovidos após benchmark, shadow/dual-run, canary, gate multidimensional e capacidade de rollback, conforme regras consolidadas em AP-010.

## Gate de execução em lote

A promoção de lote segue AP-011: 1, 10, 40 e até 300 imagens com fault injection, retomada, cancelamento, fairness, pressão de recursos e sucesso parcial explícito.


## Gate ClassicalMatchingProfile

A promoção exige corpus estratificado, recall FLANN versus BF, repetibilidade, coverage, condicionamento, resíduos, recursos, shadow/dual-run, canary e rollback comprovado. O gate funcional depende do `SGVProfile` calibrado e promovido por BP-002.
