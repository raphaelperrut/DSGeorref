# ISSUE #124 / PR #1062 — representação de evidência e histórico limpo

Candidato anterior: `452bb204612e460bba4f698ceaefb47d98838c9e`.
BASELINE_SHA corresponde ao baseline da issue:
`061e83daf5f22cd39f2338f83c204a29428c2cc0`.
O novo candidato é o commit que contém este handoff e o `validation.json` adjacente;
seu único pai é BASELINE_SHA. Os dois commits anteriores não são ancestrais dele.
O PR #1062 é preservado e a atualização remota usa lease explícito do HEAD anterior.

## Correção restrita às evidências

Classificação: FALSE_POSITIVE_DIGEST_REPRESENTATION. O run foundation-security
#265 (43639568266), job 132583905372, apontou seis `generic-api-key` em evidências.
O Gitleaks 8.24.3 local reproduziu os mesmos seis achados nos dois commits anteriores.
`secret-pattern-review` passou no run. Os valores foram conferidos como digests de
arquivos ou identificador público do commit baseline; nenhum segredo real encontrado.

| Arquivo sob story-0048 | Linha histórica | Valor documental |
|---|---:|---|
| qa-medium-finding/assessment.json | 43 | SHA-256 do hook de identidade preexistente |
| qa-medium-finding/assessment.json | 45 | SHA-256 do hook da nova superfície |
| HANDOFF.md | 73 | Identificador do baseline no parâmetro OpenAPI |
| validation.json | 49 | SHA-256 do hook da nova superfície |
| validation.json | 59 | SHA-256 do OpenAPI |
| qa-medium-finding/validation.json | 67 | SHA-256 do hook da nova superfície |

Digests SHA-256 em JSON usam agora `sha256:` seguido de oito grupos de oito
hexadecimais minúsculos separados por `:`. Remover o prefixo e os separadores
reconstrói os 64 caracteres originais, sem perda de bits. Não há truncamento,
mascaramento, exceção de scanner ou valor fictício. A mesma representação é usada
nos novos digests para evitar reincidência na documentação dos mesmos arquivos.

O comando documentado no handoff original usa `OPENAPI_BASE_SHA=$BASELINE_SHA`.
O baseline está identificado separadamente acima e no handoff original.
Logs originais e os dados dos testes/decisões permanecem preservados.
Mapas ativos de digests de evidência foram recalculados; os valores anteriores
estão preservados em mapas `historical_*`. Afirmações históricas de parentagem,
SHA e estado local nos snapshots anteriores descrevem os candidatos indicados,
não a nova parentagem consolidada. O `validation.json` adjacente é o vínculo atual.
`rewrite_evidence.py` reproduz a transformação a partir do candidato anterior e
confere a reversibilidade antes de atualizar os mapas dependentes.

Código de produção e de testes permanece byte-identical ao candidato anterior,
incluindo a feature preexistente. TaskEnvelope corrigido, ACs, contratos e
arquitetura não mudam. `.github/gitleaks.toml`, `.gitleaksignore`, workflows e
regras de detecção também não mudam. Somente o path de evidência autorizado recebe
alterações. O arquivo preexistente `src/frontend/debug.log` permanece excluído.

## Verificação e limites

Os relatórios locais de Gitleaks e dos testes focados desta continuação, os digests
atuais e a comparação de integridade estão no `validation.json` e arquivos adjacentes.
Usa-se o Gitleaks 8.24.3 oficial, checksum da distribuição conferido, a configuração
original do repositório e o intervalo do PR com `--no-merges --first-parent`.
Somente o arquivo frontend `surface.test.tsx` da feature é reexecutado, incluindo
`test_epic_010_superficie`. Não são repetidas regressões amplas ou make verify.
A falha local preexistente CRLF/hash da stack nativa continua classificada como
não causada pelo candidato; não se declara gate global verde nem novo QA aprovado.

MEDIUM_FINDING_STATUS=RESIDUAL: duplicação efetiva de orchestration, sem reutilização
segura pela API pública vigente (SAFE_REUSE_AVAILABLE=NO). A correção adequada exige
alterar produtor fora de TASK-0048; não foi aplicada remediação funcional.
Risco residual: divergência futura e manutenção coordenada das duas orquestrações.
Fail-closed, Problem Details e idempotência são preservados. Nenhum novo PR,
migration, alteração de banco ou mudança em main é parte desta remediação.
CI hospedada e revisão vinculada ao novo SHA continuam necessárias.
