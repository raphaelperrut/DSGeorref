# Composição de scope com autoridade B/K e integração I

> Registro histórico. A [governança vigente](../../GOVERNANCE.md) define o fluxo a partir da integração da #1047.

Extensão compatível sob ADR-007, autorizada pelo Owner na
[Issue #157, decisão 6724496132](https://github.com/raphaelperrut/DSGeorref/issues/157#issuecomment-6724496132).
Não substitui ADR, TaskEnvelope, DAA, QA, Reviewer ou decisão humana de merge.

## API e autoridade

`validate_effective_task_scope(root, base_revision=B, authority_checkpoint=K,
candidate_revision=C, task_envelope_path=path)` mantém a semântica legada.
Sua implementação anterior foi movida para `scope_authority.validate_legacy_scope`;
as chamadas existentes não precisam mudar.

A composição acrescenta parâmetros opcionais:

- `integration_revision=I`: identidade Git completa e imutável da integração;
- `integration_proofs`: tupla ordenada de `IntegrationProof`, uma por integração
  herdada entre B e I, sem lacunas;
- `integration_authority=GitHubIntegrationAuthority(repository, owner_id)`: identidade
  do repositório e ID numérico do Owner, fixados pela invocação confiável.

Assim como B/K, repositório e Owner não podem ser escolhidos pelo candidato ou por
um arquivo de evidência que ele altere. O adapter consulta a API GitHub com `gh api`
autenticado e fixado em `--hostname github.com`, sem ler ou registrar tokens. Não aceita um recibo JSON local como
autoridade. Sem Git, gh, autenticação, rede ou evidência completa, retorna finding.

Cada prova contém `base_revision`, `authority_checkpoint`, `candidate_revision`,
`integration_revision`, `task_envelope_path` e o número `pull_request` da tarefa
herdada. São referências a evidências verificáveis, não declarações de permissão.
O adapter confirma repositório, Owner, branch canônica main, PR efetivamente
integrado pelo Owner, SHA exato do head e SHA exato do merge. Confirma ainda que
esse merge é ancestral do tip atual da main obtido do GitHub. O tip precisa estar
disponível localmente; não há fallback para uma ref local não autenticada.

## Verificação de conteúdo e proveniência

1. B deve ser ancestral do K original; K e I devem ser ancestrais de C.
   Todas as revisões da composição exigem SHAs completos de commits existentes.
   Replacement refs (inclusive namespace efetivo customizado) e graft overlays
   são rejeitados antes da leitura da história, preservando a identidade dos objetos.
2. A cadeia herdada começa em B. Cada merge de integração tem exatamente dois
   pais: a integração anterior e o candidato autenticado do PR herdado. A última
   prova termina exatamente em I. Cada tarefa herdada passa pelo scope legado
   com sua própria base, checkpoint e envelope.
3. Além do diff agregado, cada revisão não merge é verificada contra allow/deny
   congelados no respectivo checkpoint. Deny prevalece sobre allow e sobre a
   exceção de controle do envelope. Alterações intermediárias proibidas são
   rejeitadas mesmo quando revertidas antes do candidato. Renames são examinados
   como remoção e adição, com paths delimitados por NUL.
4. O envelope de cada tarefa deve manter os mesmos bytes do checkpoint em todas
   as revisões posteriores, inclusive revisões intermediárias. A política usada
   para autorizar o controle do envelope é sempre a do checkpoint dessa tarefa.
5. Todo merge, herdado ou da tarefa, é reconstruído com `git merge-tree
   --write-tree`. Sua árvore completa deve ser idêntica à árvore real, incluindo
   blobs, remoções e modos. Conflito, múltiplas merge bases, octopus ou resolução
   manual que modifique a árvore automática são rejeitados.
6. As revisões atribuíveis à tarefa são as de C que não pertencem à história já
   provada de I ou B. Cada uma é verificada com o envelope/política originais de K.
   Interseção entre os paths tocados por essas revisões e os da história herdada
   é rejeitada por ambiguidade, mesmo se os bytes finais coincidirem. Não se usa
   apenas `git diff I..C` nem subtração de listas de arquivos para autorizar C.

O suporte inicial é conservador: integrações canônicas por merge commit do Owner,
duas ancestralidades sem conflito e sem colisão de paths entre tarefa e herança.
Squash, rebase, permissões delegadas de merge e resolução manual exigem evidência
adicional que esta extensão não presume. Retornar zero findings certifica somente
este controle de composição; não transfere aprovações antigas para outro SHA.

## Regressão, caso real e rollback

`test_scope_composition.py` cobre compatibilidade B/K/C, main avançada, preservação
de K, identidade/autoridade externas, conteúdo de merge, envelope após K,
cancelamento entre revisões, colisões e deny-overrides-allow. Os testes legados
`test_materialization.py -k recovery_scope` continuam aplicáveis.

O caso local #1043 usa B `f33429b91194177aad3cbd75c3966b1a8c58ea09`,
K `b9c05b619cdfedd2ad1f63898bbd80194cdfb91e`,
I `8cbd6092f1c887654a34f899d3428d76e8683724` e
C `1636cf221b81252e01a63f09d477233f735ee465`.
A prova herdada do PR #1044 usa checkpoint
`749278d2eddae46854ec9b500155394ee30edec1`, candidato
`42e3db8a3523662d4d698c6d5bf98a5a8b8e2ffc` e envelope TASK-0785.
São entradas para verificação, sem exceção para seus paths. A reprodução local
deve registrar o resultado real com autoridade GitHub disponível; C não é
publicado pela correção. TASK-0784, seu checkpoint e o trust não são modificados.

Rollback: reverter somente o PR desta extensão mediante decisão humana, preservando
envelopes e registros históricos. A API legada continua disponível durante a
adoção; nenhuma proteção da main é alterada.
