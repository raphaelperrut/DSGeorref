# Design review — SGVCAL declarative conformance

- **Candidate:** `ISSUE-0817` / `STORY-0707` / `TASK-0707`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; QA e revisão independente pendentes
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela a menor representação versionada das invariantes `REQ-SGVCAL-001..010`,
com `REQ-SGVCAL-007` como requisito e teste mandatórios da STORY-0707. A cobertura da família
é declarativa: não implementa Strong Geometric Verifier, pipeline, migrations, CI, scanners,
telemetria runtime, thresholds nem promoção operacional. Esses itens permanecem nas histórias
executáveis futuras.

O contrato referencia `sgv-verdict.schema.json` e `BP-002` sem alterá-los. Nenhum endpoint,
tabela, estado, evento, algoritmo, corpus ou parâmetro quantitativo novo é definido.

## Contrato publicado

`sgvcal-conformance.schema.json` fecha dez controles:

1. hard invariants, `SGVProfile` e evidence são imutáveis e versionados por estrato;
2. toda métrica declara espaço, unidade, direção e normalização;
3. erro de transferência é simétrico e sua distribuição é robusta;
4. coverage exige leverage e suporte espacial;
5. conditioning, degeneracy e estabilidade leave-one-out são obrigatórios;
6. deformação local usa Jacobiano adaptativo;
7. footprint, topologia, CRS e plausibilidade contextual são todos obrigatórios;
8. calibração é estratificada, usa holdout cego e budget bloqueante de falso aceite;
9. zona cinzenta produz `reviewable` e não contorna hard gate;
10. promoção exige shadow, canary, evidence imutável e rollback.

O schema rejeita campos ausentes ou desconhecidos, valores permissivos, controles parciais e
fallback contextual silencioso. O manifest liga cada requisito ao teste canônico e enumera os
failure modes.

## Compatibilidade, autoridade e determinismo

O contrato segue SemVer, tem owner `BC-001`, status `FROZEN` e rejeita propriedades
desconhecidas. Remoção, renomeação, relaxamento de invariante ou mudança de authority exige
nova major e revisão do Arquiteto. Parâmetros quantitativos continuam pertencendo ao `BP-002`;
o contrato não cria uma segunda autoridade. Ordem e conteúdo das listas normativas são
constantes, tornando a validação determinística.

## Impacto, riscos e rollback

- **Contrato:** novo contrato público de conformidade; nenhum contrato congelado foi alterado.
- **Banco/migration:** N/A; o slice não cria persistência, tabela ou migration executável.
- **Runtime/CI/scanners/telemetria:** N/A; nenhuma capacidade operacional foi criada.
- **Risco residual:** a suíte prova forma contratual e rejeição fail-closed, não eficácia
  científica, execução do SGV, calibração empírica, promoção ou rollback operacional.
- **Rollback contratual:** antes de consumo, reverter o candidato; após consumo pinado,
  preservar `1.0.0` e publicar versão sucessora compatível.
- **Review:** QA sentinela e Reviewer independentes permanecem pendentes no mesmo commit.

## TaskEnvelope

O TaskEnvelope foi corrigido somente para incluir seu próprio arquivo, o registry de ownership,
o teste focado e a evidence já exigida. Os deny paths foram preservados, sem glob amplo e sem
alteração de política global.
