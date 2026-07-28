# Database migrations

## Contrato normativo

A evolução segue as decisões consolidadas na ADR-026. Cada schema possui identificador, versão e matriz explícita de readers/writers. Versões major desconhecidas falham de modo fechado; dual-write somente é permitido durante migration temporária, limitada e auditada.

O padrão obrigatório é `expand–migrate–contract`:

```text
expandir schema
→ implantar readers compatíveis
→ executar backfill chunked, idempotente e retomável
→ validar contagens, checksums e invariantes
→ trocar writers
→ observar janela de segurança
→ contrair estruturas antigas
```

Cada migration declara:

- preflight de espaço, locks, duração e capacidade;
- versões adjacentes compatíveis;
- checkpoints e estado persistido;
- idempotência e estratégia de retomada;
- invariantes e critérios de conclusão;
- ponto de irreversibilidade;
- necessidade de `BackupSet` e restore drill;
- forward-fix, rollback compatível ou restore.

Artifacts históricos nunca são reescritos no lugar. Adapters podem convertê-los para o modelo canônico em memória; rematerializações físicas criam novo artifact, manifest, checksums e relações `derived_from`/`supersedes`.

A ferramenta concreta de migration será escolhida com a stack backend. As decisões consolidadas na ADR-026 determinam que o `UpgradeController` singleton executa o plano, limita versões mistas, exige evidence gate para cutover e recupera a instalação conforme a fase.
## Janela de rollback — Fase G

A matriz normativa está em `contracts/operations/version-and-rollback-matrix.yaml`. Rollback destrutivo só é garantido antes da fase contract; depois dela, aplica-se forward fix ou restore coordenado.
