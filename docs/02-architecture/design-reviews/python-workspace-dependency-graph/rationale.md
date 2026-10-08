# TASK-0771 — Rationale v1.0.0

Decisão técnica do autor ROLE-002 para STORY-0768 / ISSUE-0875, baseada exclusivamente no workspace do commit `926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6` e em metadados oficiais PyPI capturados como inputs. Estado: candidato para aprovação arquitetural independente; o autor não aprova o próprio trabalho. Não há decisão de produto/owner pendente para escolher versões deste grafo.

## Isolamento e fontes

Worktree criado do BASE, branch `codex/issue-0875-task-0771-python-graph-isolated`, sem transportar commits, arquivos não versionados ou evidência da ISSUE-0876. A checkout compartilhada permaneceu intacta. Apenas os quatro outputs e a árvore de evidência autorizada são alterados. O inventário registra digests de blobs Git no BASE e dos bytes locais; a diferença de EOL entre checkout e Git não muda a autoridade do blob.

`pyproject.toml` contém `dependencies=[]`; isso é uma lacuna do manifest, não evidência de que o backend não possui dependências. Os dois requirements e os imports integram seis dependências runtime: cryptography, psycopg[binary], PyJWT, Alembic, SQLAlchemy e Celery. Alembic/SQLAlchemy aplicam-se ao controlador de migrations; Celery aplica-se ao executável foundation já integrado em tools, não implica novo worker de produto. PyYAML/jsonschema/Ruff/mypy são dev; pytest é test. O comando de testes requer runtime + dev + test, pois os validadores exercitados pelos testes usam PyYAML/jsonschema.

O inventário DIRECT_DECLARED_DEPENDENCIES e THIRD_PARTY_NOTICES classificam pacotes Python como validação e não incluem o requirements posterior do adapter. Seu escopo e sua data não os tornam autoridade de fechamento runtime/transitivo. Não se remove pacote apenas por faltar no inventário de licenças anterior.

## Psycopg: duas autoridades e nenhuma igualdade artificial

Os dois manifests integrados do workspace fixam `psycopg[binary]==3.3.6`. O adapter importa psycopg; a evidência integrada de ensaio registra 3.3.6. Essa é a autoridade para o workspace. A distribuição irmã `psycopg-binary==3.3.6` é exigida exatamente pelo extra binary publicado; essa igualdade interna é obrigatória e não precisa de constraint duplicada.

`infra/images/native-stack.conda-lock.txt` fixa psycopg e psycopg-c 3.2.9 com URLs/hashes Conda. `native-stack.lock.yaml` identifica 3.2.9 como driver do ABI smoke da imagem. Essa autoridade é preservada para o ambiente Conda, fora do fechamento PyPI aprovado. Não se instala o workspace dentro do prefixo Conda, não se reutilizam seus site-packages e não se adiciona esse ambiente ao PYTHONPATH. Um virtualenv derivado do próprio intérprete Conda também não é o runtime autorizado neste handoff.

Não foi encontrado contrato de extensão compartilhada, objeto C cruzando processos ou linkagem in-process entre esses dois drivers. A ligação existente é pelo protocolo PostgreSQL e não exige igualdade de versões dos clientes. O wheel binary do workspace pode trazer sua própria libpq; ele não substitui as bibliotecas da imagem Conda. Isso fundamenta a separação de autoridade, sem declarar ABI smoke, interop em execução ou equivalência de comportamentos que não foram testados neste passe.

## SQLAlchemy: pin integrado, baseline histórica e limite da evidência

A baseline normativa foi importada no commit `c3ab776bca77d968ee97099b7cae464d452a46f5` (2026-07-27) e referencia família 2.0.x. O commit integrado `a61be06e765f6af360487d36f122b462aa8eef2e` (2026-10-02) introduziu `SQLAlchemy==2.1.2` no requirements do adapter. O código de migration usa create_engine/text e o fixture integrado usa sqlalchemy.engine.make_url. Não há import de APIs asyncio nem extra SQLAlchemy ativado.

`evidence/implementation/contas-locais-bootstrap-unico-sessoes-tokens-e-ada/id-parte-2/VALIDATION-REPORT.json` registra explicitamente SQLAlchemy 2.1.2, Alembic 1.18.4, psycopg 3.3.6 e 22 testes aprovados, incluindo migrations/rollback e regressões. A evidência anterior do adapter também registra ensaios de migration. Alembic 1.18.4 exige SQLAlchemy>=1.4.23 nos metadados oficiais; 2.1.2 satisfaz esse contrato. O pin não é deduzido da máquina atual.

Decisão ROLE-002: preservar `SQLAlchemy==2.1.2` como versão única deste workspace. A referência 2.0.x é histórica desatualizada para o adapter integrado, reconciliada localmente por esta decisão técnica sob revisão independente. Não se promove uma nova tecnologia, contrato ou versão ainda não integrada; tampouco se escolhe um downgrade 2.0 arbitrário. A documentação geral não foi alterada fora do allow scope. A aprovação independente desta reconciliação é necessária; não se atribui aprovação prévia de arquitetura ao relatório do Backend.

Os ensaios históricos usaram Python 3.12.10 e PostgreSQL 16.1, com fixtures sintéticas. Eles fundamentam adoção e funcionamento do adapter nessa execução, mas não certificam Python 3.12.13, a imagem Conda, produção, BP-003 ou performance. Os únicos checks novos neste passe são estruturais.

## Transitivas, resolver e ausência de upgrade oportunista

Todos os pins dos manifests são preservados. Mako 1.4.3, MarkupSafe 3.0.3 e typing_extensions 4.16.0 são usados transitivamente, sem imports diretos no workspace; passam de roots para constraints sem mudança de versão. Nenhuma distribuição foi conclusivamente identificada como obsoleta. FastAPI/Pydantic/NumPy/Rasterio/Shapely aparecem apenas no ABI smoke da stack nativa atual; não são novas dependências runtime do backend. Bibliotecas planejadas sem uso atual, npm, serviços PostgreSQL/RabbitMQ e componentes Conda não viram roots PyPI.

O BASE não contém bootstrap uv exato. A escolha técnica inicial é uv 0.12.19, uma release estável imutável anterior ao BASE, com digest oficial do arquivo Linux amd64. A escolha congela um resolver capaz de consumir índice simple local e metadados estáticos. Não é atualização de dependência adotada nem regra flutuante latest.

O fechamento preserva todos os 14 pins declarados e segue as relações Requires-Dist ativas para CPython 3.12.13/Linux x86_64. Para cada transitiva sem pin adotado, seleciona a maior release estável, compatível com todas as constraints ativas e com wheel compatível, publicada até `2026-10-06T22:27:26Z`, timestamp do BASE. A recomputação de constraints/extras converge para 43 distribuições e 47 edges, sem relaxamento manual. Essa regra constitui a primeira decisão de fechamento transitivo; não substitui um lock anterior nem atualiza versões por oportunidade. Versões, URLs, hashes e metadados resultantes agora ficam fixos: DevOps não reaplica a regra ao PyPI vivo.

`constraints.txt` possui 31 pins transitivos, incluindo os três já adotados. Eles vinculam o fechamento aprovado à transformação do pyproject, sem duplicar os 11 roots diretos nem a igualdade de psycopg-binary já imposta pelo pai. O snapshot simple contém somente wheels admitidos; sem sdist/build, sem prerelease, sem fallback de índice, sem extras adicionais e sem consulta a metadados mutáveis na resolução. O config fornece os Requires-Dist oficiais capturados por versão. Qualquer pacote, versão, hash ou origem fora desse conjunto deve falhar e voltar ao Arquiteto; DevOps não corrige constraints por conta própria.

## Topologia e handoff

No BASE há apenas um pyproject, na raiz. Aprova-se um projeto raiz virtual que representa o workspace atual, com PYTHONPATH=src/backend; nenhum manifest filho ou package vazio é introduzido. O validador existente `uv_validation.py` pressupõe members filhos não vazios, incompatível com o inventário atual. Essa limitação é registrada para revisão/adequação futura em scope explicitamente autorizado. Não é falta de autoridade para selecionar versão e não justifica nova prerequisite de versão, criação silenciosa de package ou PASS fictício do gate.

O manifest proposto é um input textual de transformação, mantido em evidence, não alteração do pyproject real. O handoff fixa os comandos, índice de conteúdo congelado, Python e resolver. Aprovações independentes no mesmo candidate SHA e scope serializado do Tech Lead precedem qualquer escrita posterior em pyproject/uv.lock. TASK-0769 permanece bloqueada até os locks e os demais pré-requisitos reais estarem aprovados e materializados.

## Integridade e referências externas

Artifacts v1.0.0, schema do grafo v1.0.0. `evidence/architecture/python-workspace-dependency-graph/digests.json` registra SHA-256 dos bytes UTF-8/LF dos outputs e de todos os inputs/evidências novos, excluindo o próprio manifest por circularidade. O candidate SHA é o commit Git que contém esses blobs; nenhuma revisão anterior atesta o novo candidato.

Fontes oficiais: [uv 0.12.19](https://github.com/astral-sh/uv/releases/tag/0.12.19), [checksum oficial](https://releases.astral.sh/github/uv/releases/download/0.12.19/uv-x86_64-unknown-linux-gnu.tar.gz.sha256), [settings de uv](https://docs.astral.sh/uv/reference/settings/), [sync/frozen](https://docs.astral.sh/uv/concepts/projects/sync/). Os URLs de metadados PyPI de cada distribuição estão no snapshot; eles são proveniência, não comandos para renovar inputs.
