# ComposiÃ§Ã£o de scope com autoridade B/K e integraÃ§Ã£o I

ExtensÃ£o compatÃ­vel sob ADR-007, autorizada pelo Owner na
[Issue #157, decisÃ£o 6724496132](https://github.com/raphaelperrut/DSGeorref/issues/157#issuecomment-6724496132).
NÃ£o substitui ADR, TaskEnvelope, DAA, QA, Reviewer ou decisÃ£o humana de merge.

## API e autoridade

`validate_effective_task_scope(root, base_revision=B, authority_checkpoint=K,
candidate_revision=C, task_envelope_path=path)` mantÃ©m a semÃ¢ntica legada.
Sua implementaÃ§Ã£o anterior foi movida para `scope_authority.validate_legacy_scope`;
as chamadas existentes nÃ£o precisam mudar.

A composiÃ§Ã£o acrescenta parÃ¢metros opcionais:

- `integration_revision=I`: identidade Git completa e imutÃ¡vel da integraÃ§Ã£o;
- `integration_proofs`: tupla ordenada de `IntegrationProof`, uma por integraÃ§Ã£o
  herdada entre B e I, sem lacunas;
- `integration_authority=GitHubIntegrationAuthority(repository, owner_id)`: identidade
  do repositÃ³rio e ID numÃ©rico do Owner, fixados pela invocaÃ§Ã£o confiÃ¡vel.

Assim como B/K, repositÃ³rio e Owner nÃ£o podem ser escolhidos pelo candidato ou por
um arquivo de evidÃªncia que ele altere. O adapter consulta a API GitHub com `gh api`
autenticado e fixado em `--hostname github.com`, sem ler ou registrar tokens. NÃ£o aceita um recibo JSON local como
autoridade. Sem Git, gh, autenticaÃ§Ã£o, rede ou evidÃªncia completa, retorna finding.

Cada prova contÃ©m `base_revision`, `authority_checkpoint`, `candidate_revision`,
`integration_revision`, `task_envelope_path` e o nÃºmero `pull_request` da tarefa
herdada. SÃ£o referÃªncias a evidÃªncias verificÃ¡veis, nÃ£o declaraÃ§Ãµes de permissÃ£o.
O adapter confirma repositÃ³rio, Owner, branch canÃ´nica main, PR efetivamente
integrado pelo Owner, SHA exato do head e SHA exato do merge. Confirma ainda que
esse merge Ã© ancestral do tip atual da main obtido do GitHub. O tip precisa estar
disponÃ­vel localmente; nÃ£o hÃ¡ fallback para uma ref local nÃ£o autenticada.

## VerificaÃ§Ã£o de conteÃºdo e proveniÃªncia

1. B deve ser ancestral do K original; K e I devem ser ancestrais de C.
   Todas as revisÃµes da composiÃ§Ã£o exigem SHAs completos de commits existentes.
2. A cadeia herdada comeÃ§a em B. Cada merge de integraÃ§Ã£o tem exatamente dois
   pais: a integraÃ§Ã£o anterior e o candidato autenticado do PR herdado. A Ãºltima
   prova termina exatamente em I. Cada tarefa herdada passa pelo scope legado
   com sua prÃ³pria base, checkpoint e envelope.
3. AlÃ©m do diff agregado, cada revisÃ£o nÃ£o merge Ã© verificada contra allow/deny
   congelados no respectivo checkpoint. Deny prevalece sobre allow e sobre a
   exceÃ§Ã£o de controle do envelope. AlteraÃ§Ãµes intermediÃ¡rias proibidas sÃ£o
   rejeitadas mesmo quando revertidas antes do candidato. Renames sÃ£o examinados
   como remoÃ§Ã£o e adiÃ§Ã£o, com paths delimitados por NUL.
4. O envelope de cada tarefa deve manter os mesmos bytes do checkpoint em todas
   as revisÃµes posteriores, inclusive revisÃµes intermediÃ¡rias. A polÃ­tica usada
   para autorizar o controle do envelope Ã© sempre a do checkpoint dessa tarefa.
5. Todo merge, herdado ou da tarefa, Ã© reconstruÃ­do com `git merge-tree
   --write-tree`. Sua Ã¡rvore completa deve ser idÃªntica Ã  Ã¡rvore real, incluindo
   blobs, remoÃ§Ãµes e modos. Conflito, mÃºltiplas merge bases, octopus ou resoluÃ§Ã£o
   manual que modifique a Ã¡rvore automÃ¡tica sÃ£o rejeitados.
6. As revisÃµes atribuÃ­veis Ã  tarefa sÃ£o as de C que nÃ£o pertencem Ã  histÃ³ria jÃ¡
   provada de I ou B. Cada uma Ã© verificada com o envelope/polÃ­tica originais de K.
   InterseÃ§Ã£o entre os paths tocados por essas revisÃµes e os da histÃ³ria herdada
   Ã© rejeitada por ambiguidade, mesmo se os bytes finais coincidirem. NÃ£o se usa
   apenas `git diff I..C` nem subtraÃ§Ã£o de listas de arquivos para autorizar C.

O suporte inicial Ã© conservador: integraÃ§Ãµes canÃ´nicas por merge commit do Owner,
duas ancestralidades sem conflito e sem colisÃ£o de paths entre tarefa e heranÃ§a.
Squash, rebase, permissÃµes delegadas de merge e resoluÃ§Ã£o manual exigem evidÃªncia
adicional que esta extensÃ£o nÃ£o presume. Retornar zero findings certifica somente
este controle de composiÃ§Ã£o; nÃ£o transfere aprovaÃ§Ãµes antigas para outro SHA.

## RegressÃ£o, caso real e rollback

`test_scope_composition.py` cobre compatibilidade B/K/C, main avanÃ§ada, preservaÃ§Ã£o
de K, identidade/autoridade externas, conteÃºdo de merge, envelope apÃ³s K,
cancelamento entre revisÃµes, colisÃµes e deny-overrides-allow. Os testes legados
`test_materialization.py -k recovery_scope` continuam aplicÃ¡veis.

O caso local #1043 usa B `f33429b91194177aad3cbd75c3966b1a8c58ea09`,
K `b9c05b619cdfedd2ad1f63898bbd80194cdfb91e`,
I `8cbd6092f1c887654a34f899d3428d76e8683724` e
C `1636cf221b81252e01a63f09d477233f735ee465`.
A prova herdada do PR #1044 usa checkpoint
`749278d2eddae46854ec9b500155394ee30edec1`, candidato
`42e3db8a3523662d4d698c6d5bf98a5a8b8e2ffc` e envelope TASK-0785.
SÃ£o entradas para verificaÃ§Ã£o, sem exceÃ§Ã£o para seus paths. A reproduÃ§Ã£o local
deve registrar o resultado real com autoridade GitHub disponÃ­vel; C nÃ£o Ã©
publicado pela correÃ§Ã£o. TASK-0784, seu checkpoint e o trust nÃ£o sÃ£o modificados.

Rollback: reverter somente o PR desta extensÃ£o mediante decisÃ£o humana, preservando
envelopes e registros histÃ³ricos. A API legada continua disponÃ­vel durante a
adoÃ§Ã£o; nenhuma proteÃ§Ã£o da main Ã© alterada.
