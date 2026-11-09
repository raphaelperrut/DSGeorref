# Composição de scope com autoridade B/K e integração I

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
   com sua própria base, checkpoint e envelope, ou pela composição completa
   descrita abaixo quando declarar uma integração própria.
3. Além do diff agregado, cada revisão não merge é verificada contra allow/deny
   congelados no respectivo checkpoint. Deny prevalece sobre allow e sobre a
   exceção de controle do envelope. Alterações intermediárias proibidas são
   rejeitadas mesmo quando revertidas antes do candidato. Renames são examinados
   como remoção e adição, com paths delimitados por NUL.
4. Uma alteração atribuída ao envelope da tarefa só pode ocorrer no próprio K.
   O envelope mantém os mesmos bytes em todas as revisões posteriores,
   inclusive revisões intermediárias. A política que autoriza o controle do
   envelope é a do checkpoint da tarefa.
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

## Composições herdadas

Extensão compatível autorizada pela
[decisão 6726868018 na Issue #157](https://github.com/raphaelperrut/DSGeorref/issues/157#issuecomment-6726868018).
Os seis campos originais de `IntegrationProof` e os resultados da API legada
permanecem. Dois campos opcionais descrevem uma tarefa já composta:

- `composition_revision`: I próprio do candidato herdado; default `None`;
- `composition_proofs`: tupla ordenada das provas entre o B original dessa
  tarefa e seu I próprio; default `()`.

Nessa prova, `base_revision` continua sendo o B original, ancestral do K original.
O primeiro pai do merge canônico herdado deve ser exatamente `composition_revision`
e a integração anterior da cadeia externa. O segundo pai deve ser o candidato
exato autenticado no GitHub. Sem composição, o primeiro pai continua sendo B.
Não se troca B pelo primeiro pai para acomodar o checkpoint.

Cada dependência é validada pelo mesmo algoritmo de composição e pela mesma
autoridade GitHub fixada pela invocação confiável. As provas não escolhem outro
Owner, repositório ou branch e não transferem aprovações. Como o merge autenticado
identifica C e a integração, a invocação confiável também fornece
`GitHubIntegrationAuthority.task_authorities`, um mapa de número de PR para
`FrozenTaskAuthority(B, K, task_envelope_path)`. Os valores devem vir dos
registros originais de atribuição e checkpoint, independentemente das provas.
Quando houver composição herdada, todas as provas da cadeia devem corresponder
a esse mapa. A invocação fornece o mapa sempre que receber uma cadeia de fonte
não confiável, mesmo que as provas omitam I próprio. Chamadas legadas e
composições simples podem dispensar o mapa quando seus valores de B, K e
envelope já vêm da invocação confiável. Em cada nível são
verificados ancestralidade, schema e identidade do envelope, bytes congelados,
política original, todas as revisões atribuídas, denies, colisões e árvores
completas dos merges. O `allow_paths` do envelope não concede autoridade de
papel para alterar o próprio envelope. O conjunto de paths herdados inclui
todas as dependências,
inclusive alterações intermediárias revertidas; nenhuma herança é descartada
para calcular colisões externas. Provas repetidas em ramos distintos são
verificadas novamente, sem cache de autorização por SHA.

Uma integração repetida no caminho de dependências ativo é ciclo e falha.
`MAX_COMPOSITION_DEPTH = 16` limita os níveis de provas herdadas; o nível 17
falha antes de autenticar ou percorrer suas dependências. São limites locais
conservadores do algoritmo, sem alterar políticas ou trust. Provas sem I próprio,
com dependências ausentes, incompletas, fora de ordem ou de tipo inválido retornam
finding. Erros de autenticação e evidência falham fechados em qualquer nível.

O caso #1042 mantém B/K `f33429b91194177aad3cbd75c3966b1a8c58ea09`, envelope
TASK-0714, I `890b3dab56e0bd07571832bae686f9af809f5a9f` e candidato local
`7a35a92709f80263645bc3c000e6b14d61d3360f`. Sua cadeia inclui os PRs #1044,
#1045 e #1043. A prova do #1043 mantém B
`f33429b91194177aad3cbd75c3966b1a8c58ea09`, K
`b9c05b619cdfedd2ad1f63898bbd80194cdfb91e`, candidato aprovado
`335f312b0b360e110c6062a8fa4203d22eea42c6` e I próprio
`7310cdf6c64e34158631f5239aa1f677d0039e9c`, com as provas #1044/#1045.
A reprodução consulta GitHub e objetos originais, sem alterar ou publicar o
candidato bloqueado, reexecutar READY/DAA ou emitir attestations.
Com a prova plana, a validação rejeita o checkpoint do #1043 porque exige
que ele descenda da base de integração. Com a prova herdada, a cadeia passa sem
findings. A validação integral de C ainda rejeita `federation.py`, `sessions.py`
e `tokens.py` no commit `b012f34090cb65f0318e37978247836c4354c6ae` por estarem
fora do escopo congelado da TASK-0714.

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
