# Requisitos não funcionais

Atributos de qualidade, segurança, desempenho, operabilidade, compatibilidade, reprodutibilidade e integridade.

**Total:** 93 requisitos.

| ID | Tipo | Prioridade | Requisito | Owner | ADRs governantes |
|---|---|---:|---|---|---|
| `REQ-AIE-005` | NAO_FUNCIONAL | P1 | reutilizar somente checkpoints e artifacts canônicos com compatibilidade comprovada | `AP-010` | ADR-051, ADR-002, ADR-018, ADR-028, ADR-036, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-048, ADR-054, ADR-041, ADR-049, ADR-050, ADR-053, ADR-026 |
| `REQ-AIE-006` | NAO_FUNCIONAL | P1 | manter IA opcional, CPU classic baseline funcional e indisponibilidade explícita de capability | `AP-010` | ADR-051, ADR-002, ADR-018, ADR-028, ADR-036, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-048, ADR-054, ADR-041, ADR-049, ADR-050, ADR-053, ADR-026 |
| `REQ-ART-001` | NAO_FUNCIONAL | P0 | Artefatos possuem hash, origem, projeto, retenção e lineage | `ADR-018;ADR-027` | ADR-051, ADR-002, ADR-018, ADR-039, ADR-044, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-ARTLAYOUT-001` | NAO_FUNCIONAL | P1 | roots internos são separados por função e durabilidade | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-036, ADR-044, ADR-027, ADR-054, ADR-041 |
| `REQ-ARTLAYOUT-002` | NAO_FUNCIONAL | P1 | objetos internos são content-addressed e vinculados a IDs lógicos | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-039, ADR-044, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-ARTLAYOUT-003` | NAO_FUNCIONAL | P0 | `ArtifactSet` é bundle diretório imutável | `ADR-018` | ADR-051, ADR-018, ADR-044, ADR-027, ADR-041 |
| `REQ-ARTLAYOUT-004` | NAO_FUNCIONAL | P1 | publicação usa staging, fsync, validação e rename atômico | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-036, ADR-044, ADR-027, ADR-054, ADR-041 |
| `REQ-ARTLAYOUT-005` | NAO_FUNCIONAL | P1 | Todo ArtifactSet e todo objeto persistido sujeito a verificação de integridade devem registrar SHA-256 como checksum canônico; hashes auxiliares podem acelerar verificações locais, mas não podem substituir o valor normativo. | `ADR-018` | ADR-051, ADR-018, ADR-034, ADR-044, ADR-027, ADR-041 |
| `REQ-ARTLAYOUT-006` | NAO_FUNCIONAL | P1 | nomes e metadata internos são sanitizados | `ADR-018` | ADR-051, ADR-018, ADR-034, ADR-044, ADR-027, ADR-041 |
| `REQ-ARTLAYOUT-007` | NAO_FUNCIONAL | P1 | execução usa identidade dedicada e impede escape do root | `ADR-018` | ADR-051, ADR-018, ADR-034, ADR-044, ADR-027, ADR-041 |
| `REQ-ARTLAYOUT-008` | NAO_FUNCIONAL | P1 | capability probe valida semântica do filesystem | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-036, ADR-044, ADR-027, ADR-054, ADR-041 |
| `REQ-ARTLAYOUT-009` | NAO_FUNCIONAL | P1 | scrubbing e reconciliação detectam corrupção e órfãos | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-036, ADR-044, ADR-027, ADR-054, ADR-041 |
| `REQ-ARTLAYOUT-010` | NAO_FUNCIONAL | P0 | serving ocorre somente após autorização e resolução segura | `ADR-018` | ADR-051, ADR-002, ADR-018, ADR-028, ADR-034, ADR-044, ADR-047, ADR-027, ADR-041, ADR-026 |
| `REQ-AUD-001` | NAO_FUNCIONAL | P0 | Operações privilegiadas e decisões humanas geram eventos append-only, sem sampling, com schema, retenção, digest e acesso próprios | `ADR-054` | ADR-002, ADR-028, ADR-039, ADR-054, ADR-050, ADR-026 |
| `REQ-BKP-001` | NAO_FUNCIONAL | P0 | BackupSets coordenam PostgreSQL, artefatos gerenciados, manifests, checksums, versões e ponto de consistência sem copiar implicitamente acervos externos | `ADR-027` | ADR-051, ADR-018, ADR-036, ADR-047, ADR-048, ADR-027, ADR-050, ADR-053, ADR-026 |
| `REQ-BKP-002` | NAO_FUNCIONAL | P0 | Restore drills automatizados e isolados validam integridade, lineage, formatos geoespaciais, reconstrução de jobs, RPO e RTO | `ADR-027` | ADR-027, ADR-026 |
| `REQ-CLASSICPROFILE-001` | NAO_FUNCIONAL | P1 | preparação fotométrica é governada por profile | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-002` | NAO_FUNCIONAL | P1 | pirâmide coarse-to-fine e tiles preservam lineage de coordenadas | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-003` | NAO_FUNCIONAL | P1 | quotas espaciais são adaptativas e redistribuíveis | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-004` | NAO_FUNCIONAL | P1 | RootSIFT float32 é canônico e versionado | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-005` | NAO_FUNCIONAL | P1 | FLANN possui piso de recall contra BF | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-006` | NAO_FUNCIONAL | P1 | ratio, reverse matching, mutual consistency e unicidade são explícitos | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-007` | NAO_FUNCIONAL | P1 | analysis mask é obrigatória e priors são suaves | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-008` | NAO_FUNCIONAL | P1 | poda pré-homografia é determinística e preserva coverage | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-009` | NAO_FUNCIONAL | P1 | calibração usa gate multidimensional | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-CLASSICPROFILE-010` | NAO_FUNCIONAL | P0 | `ClassicalMatchingProfile` é imutável, promovido por shadow/canary e reversível | `BP-001` | ADR-051, ADR-002, ADR-046, ADR-044, ADR-047, ADR-041, ADR-053 |
| `REQ-DBSCHEMA-010` | NAO_FUNCIONAL | P1 | migrations e compatibilidade seguem ADR-026 | `ADR-026` | ADR-018, ADR-027, ADR-026 |
| `REQ-EPIC-001` | NAO_FUNCIONAL | P0 | Georreferenciamento funcional somente começa após fluxo diagnóstico ponta a ponta, migrations, contratos, CI, segurança mínima e clean-room bootstrap comprovados | `AP-008` | ADR-002, ADR-018, ADR-036, ADR-034, ADR-054, ADR-053 |
| `REQ-EPIC-031` | NAO_FUNCIONAL | P0 | O cliente TypeScript é gerado do OpenAPI e fluxos críticos possuem testes de componente, acessibilidade e E2E | `ADR-002` | ADR-051, ADR-002, ADR-018, ADR-034, ADR-044, ADR-041, ADR-026 |
| `REQ-EPIC-039` | NAO_FUNCIONAL | P0 | Backup e restore são demonstrados antes de uso com dados reais | `PRODUCT_BASELINE` | ADR-018, ADR-027, ADR-026 |
| `REQ-GC-001` | NAO_FUNCIONAL | P0 | Garbage collection é reference-aware, idempotente e auditável, com dry-run, tombstone, quarentena, período de graça e revalidação | `ADR-027` | ADR-039, ADR-027 |
| `REQ-HW-001` | NAO_FUNCIONAL | P0 | Toda release funciona em CPU; GPU é aceleração opcional, declarada e governada sem alterar silenciosamente qualidade ou algoritmo | `ADR-051` | ADR-051, ADR-028, ADR-039, ADR-053 |
| `REQ-MET-001` | NAO_FUNCIONAL | P1 | Métricas possuem budget de cardinalidade; resultados científicos permanecem no banco/exports e alertas são orientados a sintomas/SLOs | `ADR-054` | ADR-002, ADR-018, ADR-036, ADR-054 |
| `REQ-NFR-001` | NAO_FUNCIONAL | P1 | Metas de capacidade e latência são medidas com corpus representativo | `PRODUCT_BASELINE` | ADR-039, ADR-041, ADR-050 |
| `REQ-OBS-001` | NAO_FUNCIONAL | P1 | Logs estruturados, métricas, traces e correlation IDs por request/job | `ADR-054` | ADR-002, ADR-018, ADR-036, ADR-054 |
| `REQ-OBS-002` | NAO_FUNCIONAL | P1 | Telemetria usa contratos OpenTelemetry/backends substituíveis e correlation IDs de request até ArtifactSet, sem se tornar fonte autoritativa | `ADR-054` | ADR-002, ADR-018, ADR-036, ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-OFF-001` | NAO_FUNCIONAL | P0 | O core executa offline e toda conexão de saída é explícita, governada e auditável | `ADR-051` | ADR-051, ADR-047, ADR-041, ADR-049 |
| `REQ-PLN-005` | NAO_FUNCIONAL | P0 | impor WIP por classe e teto global com reservas para P0, segurança e manutenção | `DELIVERY_PLAN` | ADR-002, ADR-044, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-PLN-006` | NAO_FUNCIONAL | P1 | registrar capacidade por faixas, categoria e confiança, sem conversão automática em prazo | `DELIVERY_PLAN` | ADR-002, ADR-044, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-PRV-001` | NAO_FUNCIONAL | P0 | Retenção, exclusão e exportação são configuráveis e auditadas por instância/projeto | `ADR-027` | ADR-002, ADR-018, ADR-039, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-RET-001` | NAO_FUNCIONAL | P0 | RetentionPolicies versionadas consideram classe, estado, dependência, hold e reprodução antes de tornar um objeto elegível à remoção | `ADR-027` | ADR-051, ADR-018, ADR-036, ADR-039, ADR-047, ADR-048, ADR-027, ADR-050, ADR-053 |
| `REQ-RMQ-002` | NAO_FUNCIONAL | P0 | Intermediários devem possuir classe de persistência, recomputabilidade, dependências, retenção e custo estimado | `ADR-050` | ADR-051, ADR-018, ADR-036, ADR-047, ADR-048, ADR-027, ADR-050, ADR-053 |
| `REQ-RUNTIME-009` | NAO_FUNCIONAL | P1 | Sinais operacionais aplicam cardinalidade limitada, redaction e correlação consistente. | `ADR-054` | ADR-002, ADR-018, ADR-036, ADR-034, ADR-039, ADR-054 |
| `REQ-SCM-004` | NAO_FUNCIONAL | P0 | Upgrade, rollback e downgrade devem avaliar compatibilidade e bloquear operações irreversíveis sem restore seguro | `ADR-026` | ADR-027, ADR-026 |
| `REQ-SDR-003` | NAO_FUNCIONAL | P1 | Operações não determinísticas devem declarar capacidade, executar probes e usar consenso orçado quando aplicável | `ADR-053` | ADR-051, ADR-046, ADR-039, ADR-044, ADR-047, ADR-053 |
| `REQ-SDR-004` | NAO_FUNCIONAL | P1 | Replay científico e promoção devem preservar hashes do ambiente e classificar divergências sem retenção ilimitada | `ADR-053` | ADR-051, ADR-018, ADR-036, ADR-046, ADR-039, ADR-047, ADR-048, ADR-027, ADR-041, ADR-050, ADR-053, ADR-026 |
| `REQ-SGVCAL-001` | NAO_FUNCIONAL | P1 | invariantes duras e `SGVProfile` são imutáveis por estrato | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-002` | NAO_FUNCIONAL | P1 | toda métrica declara espaço, unidade, direção e normalização | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-003` | NAO_FUNCIONAL | P1 | erros usam distribuições robustas de transferência simétrica | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-004` | NAO_FUNCIONAL | P1 | coverage é multidimensional e inclui leverage e suporte espacial | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-005` | NAO_FUNCIONAL | P0 | condicionamento, degenerescência e estabilidade leave-one-out são obrigatórios | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-006` | NAO_FUNCIONAL | P1 | deformação local é medida por Jacobiano adaptativo | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-007` | NAO_FUNCIONAL | P1 | footprint, topologia, CRS e plausibilidade contextual são validados | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-008` | NAO_FUNCIONAL | P1 | calibração é estratificada, com holdout cego e budget de falso aceite | `BP-002` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-009` | NAO_FUNCIONAL | P1 | zona cinzenta é governada sem override de hard gate | `ADR-046` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SGVCAL-010` | NAO_FUNCIONAL | P1 | profile e evidence são promovidos por shadow/canary e possuem rollback | `BP-002` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-044, ADR-047, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SMO-001` | NAO_FUNCIONAL | P0 | Scheduler deve emitir métricas agregadas e eventos correlacionados sem labels de alta cardinalidade | `ADR-039` | ADR-039, ADR-041, ADR-050 |
| `REQ-SMO-004` | NAO_FUNCIONAL | P1 | Dashboard role-based deve explicar bloqueios, prioridade efetiva e ações seguras com auditoria | `ADR-039` | ADR-046, ADR-039, ADR-048, ADR-054, ADR-050, ADR-026 |
| `REQ-SPRINT-001-007` | NAO_FUNCIONAL | P1 | aplicar gate progressivo de CI proporcional às capacidades presentes | `AP-008` | ADR-002, ADR-018, ADR-036, ADR-034, ADR-044, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-SRC-003` | NAO_FUNCIONAL | P0 | Fontes externas são integradas por gateway de capacidades com adapters allowlisted, testes de contrato e estados explícitos de suporte | `ADR-047` | ADR-051, ADR-002, ADR-018, ADR-028, ADR-034, ADR-047, ADR-041, ADR-049 |
| `REQ-SRG-001` | NAO_FUNCIONAL | P1 | Baselines científicos devem ser versionados, estratificados e separados entre desenvolvimento, sentinelas e promoção cega | `ADR-053` | ADR-046, ADR-047, ADR-053 |
| `REQ-SRG-002` | NAO_FUNCIONAL | P1 | Seleção de testes deve usar grafo de impacto com tiers obrigatórios e matriz completa em promotion candidates | `ADR-053` | ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-SRG-003` | NAO_FUNCIONAL | P0 | Promoção deve aplicar gate multidimensional sem compensação de hard gates por médias globais | `ADR-053` | ADR-046, ADR-047, ADR-053 |
| `REQ-SRG-004` | NAO_FUNCIONAL | P1 | Bundles científicos devem coexistir, permitir canary/dual-run, pinning e rollback sem alterar artifacts históricos | `ADR-053` | ADR-051, ADR-018, ADR-036, ADR-046, ADR-047, ADR-048, ADR-027, ADR-050, ADR-053 |
| `REQ-SRP-001` | NAO_FUNCIONAL | P1 | Cada attempt deve preservar snapshot seletivo e imutável de policy, plano, capacidade, prioridade e runners sem secrets | `ADR-039` | ADR-039, ADR-041, ADR-050 |
| `REQ-SRP-004` | NAO_FUNCIONAL | P1 | Bundles de reprodução devem ser assinados, redigidos, sujeitos a retenção e livres de payloads raster e credenciais | `ADR-039` | ADR-034, ADR-039, ADR-027, ADR-054 |
| `REQ-SUP-001` | NAO_FUNCIONAL | P0 | Releases possuem lockfiles, SBOM, scanning, checksums, assinatura OCI e provenance verificável | `ADR-034` | ADR-051, ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-TOOL-001` | NAO_FUNCIONAL | P1 | O backend e os serviços Python devem usar **CPython 3.12.13 como runtime primário inicial, dentro da linha 3.12**. O código deve permanecer compatível com a linguagem 3.12 e não pode depender de sintaxe, biblioteca padrão ou comportamento exclusivo de Python 3.13 ou 3.14. | `AP-001` | ADR-002, ADR-044, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-TOOL-002` | NAO_FUNCIONAL | P1 | dependências Python usam `uv`, workspace e lock frozen | `AP-001` | ADR-002, ADR-044, ADR-054, ADR-041, ADR-053, ADR-026 |
| `REQ-TOOL-003` | NAO_FUNCIONAL | P1 | FastAPI/Pydantic permanecem no adapter HTTP | `ADR-002` | ADR-051, ADR-002, ADR-018, ADR-034, ADR-044, ADR-041, ADR-026 |
| `REQ-TOOL-004` | NAO_FUNCIONAL | P1 | persistência usa SQLAlchemy 2/Alembic e permite SQL/PostGIS explícito | `ADR-018` | ADR-002, ADR-018, ADR-039, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-TOOL-005` | NAO_FUNCIONAL | P1 | domínio, transporte e persistência possuem modelos separados | `ADR-002` | ADR-051, ADR-002, ADR-018, ADR-034, ADR-039, ADR-044, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-TOOL-006` | NAO_FUNCIONAL | P1 | Os gates locais e de integração contínua devem executar Ruff e mypy com as configurações versionadas do repositório; qualquer violação não dispensada por exceção aprovada deve bloquear o commit candidato. | `AP-001` | ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-TOOL-007` | NAO_FUNCIONAL | P1 | integrações aplicáveis usam PostGIS e RabbitMQ reais | `AP-001` | ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-TOOL-008` | NAO_FUNCIONAL | P1 | frontend usa Node 24 LTS e pnpm frozen | `AP-001` | ADR-002, ADR-053 |
| `REQ-TOOL-009` | NAO_FUNCIONAL | P1 | frontend opera em TypeScript strict com Vitest, Testing Library e Playwright | `AP-001` | ADR-002, ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-053, ADR-026 |
| `REQ-TOOL-010` | NAO_FUNCIONAL | P1 | Make oferece entrypoints equivalentes em local e CI | `AP-001` | ADR-002, ADR-054, ADR-053, ADR-026 |
| `REQ-UPG-001` | NAO_FUNCIONAL | P0 | Upgrades usam fases explícitas e matriz de compatibilidade, são precedidos de preflight/BackupSet, executam migrations controladas, smoke tests e rollback/restore documentado | `ADR-026` | ADR-034, ADR-027, ADR-026 |
| `REQ-UPG-002` | NAO_FUNCIONAL | P0 | Migrations devem ser executadas por controlador exclusivo com lease, preflight, plano e checkpoints persistidos | `ADR-026` | ADR-002, ADR-018, ADR-039, ADR-048, ADR-027, ADR-041, ADR-026 |
| `REQ-UPG-003` | NAO_FUNCIONAL | P0 | Cutover deve depender de evidence gate multidimensional incluindo invariantes, readers históricos, health e canary | `ADR-026` | ADR-034, ADR-046, ADR-039, ADR-047, ADR-054, ADR-050, ADR-053, ADR-026 |
| `REQ-UPG-004` | NAO_FUNCIONAL | P0 | Falhas devem seguir recuperação por fase, bloqueando writers em estado incerto e usando forward-fix ou restore após irreversibilidade | `ADR-026` | ADR-027, ADR-026 |
| `REQ-UPG-005` | NAO_FUNCIONAL | P1 | Rollout faseado limita versões mistas, drena writers e fixa jobs longos à versão compatível até a conclusão. | `ADR-026` | ADR-051, ADR-002, ADR-018, ADR-034, ADR-044, ADR-041, ADR-026 |
| `REQ-UX-002` | NAO_FUNCIONAL | P0 | Capacidades como bootstrap, busca espacial e IA compõem planos versionados e não aparecem como modos duplicados sem justificativa | `ADR-044;ADR-051` | ADR-051, ADR-002, ADR-018, ADR-034, ADR-044, ADR-047, ADR-041, ADR-026 |
| `REQ-WORKER-001` | NAO_FUNCIONAL | P1 | `TaskEnvelope` é mínimo, versionado e contém somente IDs, versão e contexto técnico indispensável | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-002` | NAO_FUNCIONAL | P1 | existem poucas filas duráveis por classe de workload, sem fila dinâmica por job | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-003` | NAO_FUNCIONAL | P1 | ack ocorre somente após commit autoritativo e prefetch é calibrado por workload | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-004` | NAO_FUNCIONAL | P1 | workers usam prefork reciclável e isolamento explícito de processos/subprocessos | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-005` | NAO_FUNCIONAL | P1 | leases persistem em PostgreSQL com fencing token e expiração verificável | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-006` | NAO_FUNCIONAL | P1 | retry segue taxonomia de domínio; poison messages entram em quarantine auditável | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-007` | NAO_FUNCIONAL | P1 | scheduler e outbox são autoritativos para DAG, despacho e redelivery | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-008` | NAO_FUNCIONAL | P1 | progresso é persistente, monotônico e reconciliável entre SSE e polling | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-009` | NAO_FUNCIONAL | P1 | cancelamento atua somente em safe points e preserva consistência/publicação atômica | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
| `REQ-WORKER-010` | NAO_FUNCIONAL | P1 | readiness, drain, shutdown e retomada são governados e testados por fault injection | `AP-007` | ADR-002, ADR-018, ADR-036, ADR-044, ADR-054, ADR-041 |
