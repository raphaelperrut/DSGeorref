# Handoff — consolidação dos cinco slices de governança

## Baseline candidato

Os cinco predecessores estão integrados no mesmo histórico que antecede este
candidato:

| Slice | PR | Merge commit | Output local |
|---|---:|---|---|
| `STORY-0754` | #991 | `af6fb2091a446cca6ec781003cc40a3528b881ca` | `ism-iss-parte-1` |
| `STORY-0755` | #992 | `0686b168be5f1996972d60261a5da4afe110f0ca` | `iss-pln-parte-2` |
| `STORY-0756` | #993 | `0415c9a880ebad159fdbb0b5aad5066c04052ab6` | `prj-prm-parte-3` |
| `STORY-0757` | #994 | `97d6668c72b18cce5feca50ac3b0855afb47a357` | `prm-sprint-001-parte-4` |
| `STORY-0758` | #995 | `b40f0e9a94000eb0f5beb18a0813fcf11f6ba116` | `sprint-001-parte-5` |

O teste obrigatório exige que cada merge continue ancestral do `HEAD`, que todos
os outputs produzidos existam no checkout e que as cinco dependências da
`TASK-0684` permaneçam exatas.

## Rastreabilidade e integração

O contrato congelado da `STORY-0683` mantém cinco requisitos. As policies dos
cinco slices acrescentam 48 requisitos, totalizando os 53 requisitos listados no
`EPIC-110`. O teste deriva a cobertura das autoridades versionadas e rejeita
requisito, teste, control key, policy ID ou output reclamado por mais de um owner.
Assim, a consolidação não replica regras normativas em um novo manifest.

Os write scopes dos cinco TaskEnvelopes são verificados por contenção de path e
permanecem disjuntos. Os cinco packages pertencem a `BC-001`, usam schema `1.0.0`
e possuem IDs de policy exclusivos. A binding explícita do primeiro slice deve
continuar idêntica ao owner, status, versão e path do contrato congelado; os demais
slices apenas materializam seus controles locais. Nenhum contrato ou output é
reescrito por esta consolidação.

## Acceptance criteria

- `AC-ISSUE-0794-01`: coberto por ancestry dos cinco merge commits, presença dos
  outputs e dependências exatas no teste obrigatório.
- `AC-ISSUE-0794-02`: coberto pela igualdade entre os 53 requisitos do épico e a
  união disjunta contrato + policies, com teste único por requisito.
- `AC-ISSUE-0794-03`: coberto por scopes, outputs, policy IDs, controls e testes
  sem colisão, mais compatibilidade explícita com o contrato congelado.
- `AC-ISSUE-0794-04`: reservado a Reviewer independente sobre o SHA candidato.

## Escopo, contratos e rollback

A `TASK-0684` foi ajustada somente para autorizar o próprio arquivo e o diretório
de evidence que ela já exigia; o espelho Phase F recebeu os mesmos dois paths.
Não houve alteração de outcome, dependência, requisito, AC, deny path ou regra de
produto.

Impacto contratual: `NONE`; o contrato público existente é apenas consumido e
verificado, sem mudança de ADR, schema, API, evento ou semântica. Migration e
rollback operacional: `NOT_APPLICABLE`, pois o diff adiciona somente teste,
handoff e evidence versionados no control plane, sem estado/schema persistido,
artifact implantável ou deployment. Uma retirada antes de consumo é feita por
revert normal do commit, sem ação de dados.

## Limitações e riscos residuais

- A aprovação de `AC-ISSUE-0794-04` permanece externa e não é declarada aqui.
- A evidência separada da `STORY-0756` não existe no path sugerido pelo envelope
  daquele slice; o `HANDOFF.md`, os testes e o merge commit #993 são as evidências
  versionadas efetivamente presentes no baseline. A consolidação não altera o
  predecessor nem inventa evidência retroativa.
- O teste prova integração do control plane versionado; não executa mutação de
  GitHub, cutover, persistência ou operação runtime.
