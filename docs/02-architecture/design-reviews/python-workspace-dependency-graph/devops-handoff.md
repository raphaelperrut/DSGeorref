# TASK-0771 — Handoff DevOps v1.0.0

Estado: decisão do autor fechada para revisão independente; nenhum uv.lock materializado e nenhum frozen install atestado. Base `926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6`. O candidate é o commit contendo este arquivo e digests.json, obtido por `git rev-parse HEAD`. Arquiteto independente, DevOps, QA e Reviewer devem vincular a decisão, os inputs e suas evidências a esse mesmo SHA. O autor não emite essas aprovações.

Tech Lead deve autorizar e serializar posteriormente escrita em `pyproject.toml`, `uv.lock` e a evidência DevOps. Este documento não concede essa autorização. Não transportar evidência/commits da ISSUE-0876. Nenhuma terceira Story/Issue/Task é criada. A limitação do validador que exige manifests filhos precisa de escopo de adequação separado e explicitamente autorizado; não improvisar packages para satisfazê-lo.

## Inputs e transformação exatos

Usar exatamente os blobs do candidato revisado: approved-dependency-graph.yaml, constraints.txt, rationale.md e devops-handoff.md; resolution-inputs.json, simple/**, resolver-config.toml, pyproject-additions.toml, pyproject-proposed.toml e digests.json em `evidence/architecture/python-workspace-dependency-graph/`. Conferir todos os SHA-256 do manifest antes de usar. O grafo registra também SHA-256 dos blobs das autoridades no BASE. Não executar capture-resolution-inputs.py novamente: ele é um registro do método de captura e novas respostas do PyPI constituiriam nova decisão.

A única transformação de manifest autorizável é copiar os bytes de `pyproject-proposed.toml` sobre o pyproject raiz, depois de confirmar que o manifest atual ainda é o input BASE. O proposto preserva o conteúdo existente, substitui dependencies=[] pelos seis roots runtime exatos e adiciona quatro roots dev, pytest no grupo test, 31 constraints, restrição de environment e default-groups vazio. Não cria build-system, child projects, novos extras ou mudanças de produto. Interpretar o root virtual como único projeto do workspace atual; imports existentes recebem PYTHONPATH=src/backend. O pin interno psycopg-binary é imposto pelo extra do root; Mako/MarkupSafe/typing_extensions estão apenas nas constraints.

Decisões de versão: workspace `psycopg[binary]==3.3.6`; Conda/native `psycopg==3.2.9` permanece em ambiente separado, sem compartilhamento de prefixo/ABI. Workspace `SQLAlchemy==2.1.2` preserva o adapter integrado e ensaiado; a referência histórica `2.0.x` é reconciliada localmente nesta decisão, sob aprovação técnica independente.

Python: CPython 3.12.13 exato, Linux x86_64 com glibc >=2.28. O requires-python de metadata permanece >=3.12,<3.13; este fechamento e seu sync são restritos à versão exata 3.12.13. Windows/macOS e outras versões/lanes não são certificados por este input. Fornecer previamente um intérprete aprovado fora de qualquer prefixo Conda em `/usr/local/bin/python3.12`; registrar sua identidade/digest na evidência de execução. Não usar Python/site-packages do ambiente Conda. Não baixar Python automaticamente.

Resolver: uv 0.12.19, arquivo `uv-x86_64-unknown-linux-gnu.tar.gz`, SHA-256 `23bf5552d220e0842b65c862097b2ebaeba0064b74eda5e565e77fd25969d8c8`. Origem fixa: https://github.com/astral-sh/uv/releases/download/0.12.19/uv-x86_64-unknown-linux-gnu.tar.gz . Release imutável; exigir checksum e verificar attestation GitHub do produtor astral-sh/uv. Nenhum instalador flutuante é input aprovado.

Índice único: `file:///opt/dsgeorref-python-inputs/simple`, cópia literal do snapshot revisado. O nome/caminho canônico fixa a identidade registry no lock entre execuções. Origens de wheels são URLs HTTPS de files.pythonhosted.org com SHA-256, copiadas do PyPI oficial. O config externo explícito desativa fallback do PyPI default, outros índices, builds, downloads de Python e prereleases e fixa metadados de dependências. Não habilitar `--all-extras`, overrides, upgrade, index externo, no-deps ou relaxamento de constraints.

## Comandos para o passe futuro, não executados nesta tarefa

Executar numa checkout limpa do candidate revisado e autorizado, em Linux amd64. Preparar `/opt/dsgeorref-python-inputs` vazio para estes inputs e o cache exclusivo, sem apagar dados existentes. O path canônico pode ser um mount da cópia verificada; se já existir conteúdo diferente, parar. O arquivo do resolver deve ser previamente baixado da URL fixa acima para esse diretório; a obtenção não autoriza troca de versão.

```bash
set -euo pipefail
GRAPH_EVIDENCE="$PWD/evidence/architecture/python-workspace-dependency-graph"
PYTHON_EXACT=/usr/local/bin/python3.12
"$PYTHON_EXACT" -I -B -c 'import sys; assert sys.version_info[:3] == (3,12,13); assert sys.base_prefix == "/usr/local"'
"$PYTHON_EXACT" -B "$GRAPH_EVIDENCE/check-structure.py" --verify-digests
"$PYTHON_EXACT" -B - <<'PY'
import hashlib, pathlib, subprocess
base = "926a6a8c9a69a838b165cca9df6c4ebb9c03c8d6"
current = subprocess.check_output(["git", "show", "HEAD:pyproject.toml"])
expected = subprocess.check_output(["git", "show", f"{base}:pyproject.toml"])
assert current == expected, "manifest changed since approved BASE; stop"
assert not subprocess.check_output(["git", "status", "--porcelain"]), "checkout must be clean"
PY
printf '%s  %s\n' '23bf5552d220e0842b65c862097b2ebaeba0064b74eda5e565e77fd25969d8c8' '/opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu.tar.gz' | sha256sum --check
gh attestation verify /opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu.tar.gz --repo astral-sh/uv
tar -xzf /opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu.tar.gz -C /opt/dsgeorref-python-inputs
test ! -e /opt/dsgeorref-python-inputs/simple
cp -R "$GRAPH_EVIDENCE/simple" /opt/dsgeorref-python-inputs/simple
cmp "$GRAPH_EVIDENCE/simple/index.html" /opt/dsgeorref-python-inputs/simple/index.html
"$PYTHON_EXACT" -B - <<'PY'
import pathlib, hashlib
origin = pathlib.Path('evidence/architecture/python-workspace-dependency-graph/simple')
target = pathlib.Path('/opt/dsgeorref-python-inputs/simple')
expected = {p.relative_to(origin).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in origin.rglob('*') if p.is_file()}
actual = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob('*') if p.is_file()}
assert actual == expected, 'snapshot copy mismatch; stop before uv lock/sync'
PY
"$PYTHON_EXACT" -I -B -c 'import sys; assert sys.version_info[:3] == (3,12,13); assert sys.base_prefix == "/usr/local"'
UV_EXACT=/opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu/uv
CONFIG_EXACT="$GRAPH_EVIDENCE/resolver-config.toml"
CACHE_EXACT=/opt/dsgeorref-python-inputs/cache
cp "$GRAPH_EVIDENCE/pyproject-proposed.toml" pyproject.toml
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV_EXACT" --config-file "$CONFIG_EXACT" --cache-dir "$CACHE_EXACT" lock --python "$PYTHON_EXACT" --no-python-downloads --no-build
"$PYTHON_EXACT" -B "$GRAPH_EVIDENCE/check-structure.py" --verify-digests --check-lock uv.lock
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV_EXACT" --config-file "$CONFIG_EXACT" --cache-dir "$CACHE_EXACT" lock --check --python "$PYTHON_EXACT" --no-python-downloads --no-build
```

`check-structure.py` exige o conjunto exato de 43 versões, registry canônico e URLs/hashes das wheels admitidas; sdist, package adicional ou artifact novo falham. O próprio script de integridade e o manifest devem ser os blobs do candidate aprovado. A cópia do índice completo também deve ser conferida arquivo a arquivo por hash, não apenas o index raiz (incluído no bloco acima). Nada foi instalado ou resolvido por uv no presente passe; estes comandos são o procedimento futuro e não uma alegação de execução.



Para repetição documental do lock, usar os mesmos bytes/config/intérprete/resolver em outra checkout limpa autorizada no mesmo path registry canônico e comparar SHA-256 dos dois uv.lock, sem usar o primeiro lock como preferência de resolução. Não regenerar metadados ou consultar PyPI/simple como fallback. Falha por artifact remoto ausente mantém bloqueio e requer recuperação do mesmo conteúdo com mesmo hash; não é permissão para escolher outra versão.

Depois da geração e validação do lock, instalar com frozen, sempre no mesmo runtime e usando os mesmos inputs:

```bash
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV_EXACT" --config-file "$CONFIG_EXACT" --cache-dir "$CACHE_EXACT" sync --frozen --no-default-groups --python "$PYTHON_EXACT" --no-python-downloads --no-build
# Ambiente de dev/test (runtime continua incluído):
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV_EXACT" --config-file "$CONFIG_EXACT" --cache-dir "$CACHE_EXACT" sync --frozen --no-default-groups --group dev --group test --python "$PYTHON_EXACT" --no-python-downloads --no-build
# Com cache completo verificado, repetir o sync acima acrescentando --offline.
```

Manter a verificação lock --check antes de sync --frozen: frozen sozinho não atesta que o lock corresponde ao manifest. Conferir hashes dos wheels e suas dependências ativas; nenhum build nativo é permitido. Registrar uv --version, versão/digest do Python, identidade do host/plataforma, SHA-256 dos inputs/pyproject/lock, resultados reais e diff limitado ao scope futuro. Não reutilizar esta revisão como prova de instalação ou teste de ABI. Preservar o lock Conda e sua stack inteira.

A revisão deste candidato, o scope DevOps, a materialização real, o frozen install e o gate estrutural de topologia são gates distintos. TASK-0769 continua bloqueada sem lock e sem os demais inputs operacionais reais. Rejeição independente invalida o handoff; nenhum PASS, benchmark ou promoção BP-003 é fabricado.
