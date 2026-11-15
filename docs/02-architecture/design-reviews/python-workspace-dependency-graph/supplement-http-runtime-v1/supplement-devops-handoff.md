# Handoff DevOps suplementar — http-runtime-v1.0.0

Este documento não autoriza TASK-0773, instalação de Python, escrita de lock ou criação de API/TLS. Executar os blocos somente em passe futuro explicitamente autorizado, após aprovação independente do mesmo candidato por Arquitetura, DevOps, QA e Reviewer. Autoridade composta: graph em `cb198c9e8340e0675c36679de426abf922e1c569` + commit aprovado deste suplemento. Baseline corrente capturada: `051ed667565bdce1eb22745aee35861a6d4be119`.

## Entradas fixas

O manifest suplementar está em `docs/02-architecture/design-reviews/python-workspace-dependency-graph/supplement-http-runtime-v1/supplement.json`. A evidência está em `evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1/`. Verificar digests.json deste diretório e os 55 hashes do histórico, inclusive o manifest histórico por seu próprio digest. Não rodar capture-delta.py, capture-resolution-inputs.py nem assemble-author-artifacts.py operacionalmente. PyPI vivo não é fallback.

Permanecem uv **0.12.19**, tarball Linux amd64 SHA-256 `23bf5552d220e0842b65c862097b2ebaeba0064b74eda5e565e77fd25969d8c8`, URL `https://github.com/astral-sh/uv/releases/download/0.12.19/uv-x86_64-unknown-linux-gnu.tar.gz`, attestation do repositório astral-sh/uv e registry único `file:///opt/dsgeorref-python-inputs/simple`. O bootstrap já aprovado é consumido por referência; não é recapturado ou substituído. No futuro, verificar checksum e attestation antes de extrair uv, conforme o handoff histórico. Nenhum build, outro índice, extra adicional ou download automático de Python é permitido.

O proposed pyproject suplementar é completo, tem 14 roots nos grupos runtime/dev/test e 39 constraints. Ele preserva as demais configurações do manifest histórico. A raiz corrente da main permanece com dependencies=[]; o checker de autoria deve confirmar que não foi alterada. O futuro passe verifica o SHA-256 do pyproject raiz contra source-inputs.json antes da cópia. Qualquer drift novo requer nova análise, não merge textual automático. Não executar pip install dos dois requirements antigos: seus pins divergentes foram reconciliados semanticamente neste suplemento para o futuro manifest único.

## Pré-requisito externo: CPython standalone

Provisionamento por operador/passe autorizado para `/usr/local` é um pré-requisito; não amplia os allow_paths de TASK-0773. Não executar aqui. Target Linux x86_64, glibc>=2.28, prefixo fora de Conda. Arquivo fixo:

- Publisher: Astral / astral-sh/python-build-standalone.
- Release imutável: 20260602; IDs de release/asset no registro cpython-artifact.json.
- URL: https://github.com/astral-sh/python-build-standalone/releases/download/20260602/cpython-3.12.13%2B20260602-x86_64-unknown-linux-gnu-install_only.tar.gz
- Formato: tar.gz com prefixo python/.
- SHA-256: `9be5c21b78dbc371e739bc7faf3b007b8e607335f780bdd2e0dd44a6e3580d76`.
- Provenance: bundles Sigstore/SLSA e resultado `gh attestation verify --repo astral-sh/python-build-standalone` exit 0 estão versionados no suplemento. Verificar novamente os bytes do archive contra esse digest e a attestation antes do provisionamento; não aceitar outra build/tag/digest.

Procedimento exato para o operador futuro:

1. Reservar exclusivamente `/usr/local` para a janela de provisionamento. Salvar inventário de todos os paths existentes, permissões/ownership e backup restaurável de `/usr/local` em storage operacional autorizado. Registrar checksum do backup. Se não for possível impedir escrita concorrente ou fazer backup/restauração, parar.
2. Baixar somente a URL fixa para `/opt/dsgeorref-python-inputs/cpython-3.12.13+20260602-x86_64-unknown-linux-gnu-install_only.tar.gz`; verificar sha256sum e `gh attestation verify ARQUIVO --repo astral-sh/python-build-standalone`. Não usar instalador remoto, uv python install, Conda ou link para outro prefixo.
3. Inspecionar o tar: todos os membros devem estar sob python/, sem travessia; links devem resolver dentro do prefixo. Registrar lista completa de membros, tipos e hashes dos arquivos e dos destinos textuais de symlinks. Rejeitar colisão de qualquer arquivo/symlink existente em `/usr/local`; diretórios existentes podem ser compartilhados sem mudar permissões. Não substituir instalação preexistente nem selecionar outro destino.
4. Extrair com `tar --keep-old-files --no-overwrite-dir --strip-components=1 -xzf ARQUIVO -C /usr/local`. O operador deve ter autorizado os paths do inventário; em erro parcial, fazer rollback antes de tentar qualquer outra ação. Não alterar PATH global nem registrar Python em Conda.
5. Verificar os hashes instalados contra o inventário e executar os gates abaixo com ambiente limpo. Registrar versão, executable, prefixos, platform/libc, digest do archive e do binário. Não ajustar versão ou prefixo se falhar.

```bash
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 /usr/local/bin/python3.12 -I -B - <<'PY'
import platform, sys
assert sys.implementation.name == 'cpython'
assert sys.version_info[:3] == (3, 12, 13)
assert sys.executable == '/usr/local/bin/python3.12'
assert sys.prefix == sys.base_prefix == '/usr/local'
assert platform.system() == 'Linux' and platform.machine() == 'x86_64'
libc, version = platform.libc_ver()
assert libc == 'glibc' and tuple(map(int, version.split('.')[:2])) >= (2, 28)
print(sys.version, sys.executable, sys.base_prefix, libc, version)
PY
```

Rollback: suspender consumidores que usarem este interpreter; validar que cada arquivo criado ainda corresponde ao inventário instalado. Remover somente arquivos/symlinks criados por esta extração e diretórios novos que estiverem vazios, em ordem inversa. Preservar diretórios anteriores e dados alheios. Se houver alteração concorrente, parar e restaurar o backup integral sob controle exclusivo, sem sobrescrever silenciosamente trabalho novo. Conferir o inventário anterior e restaurar seus ownership/permissões. O candidato/lock permanece bloqueado após rollback. O procedimento não exige decidir outra versão em tempo de execução.

## Compor os inputs sem duplicar metadados históricos

Usar checkout limpa do candidato aprovado e histórico Git disponível. O script é stdlib-only, não instala/resolver pacotes nem altera produto. O comando --compose somente cria um diretório que ainda não existe, por isso nunca sobrescreve evidência. Preparar externamente `/opt/dsgeorref-python-inputs` e montar/copiar `composed/simple` no path canônico após verificar todos os hashes, sem mudar o conteúdo ou adicionar packages. A tabela de URLs dos wheels no índice contém somente artifacts já fixados.

```bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
S=evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1
RUN=evidence/operations/python-workspace-lock
PY=/usr/local/bin/python3.12
"$PY" -I -B "$S/check-supplement.py"
"$PY" -I -B - <<'PY'
import hashlib, json, pathlib, subprocess
sources=json.loads(pathlib.Path('evidence/architecture/python-workspace-dependency-graph/supplement-http-runtime-v1/source-inputs.json').read_text())
expected=next(x['sha256'] for x in sources if x['path']=='pyproject.toml')
assert hashlib.sha256(pathlib.Path('pyproject.toml').read_bytes()).hexdigest()==expected
assert not subprocess.check_output(['git','status','--porcelain']), 'checkout must be clean before execution evidence'
PY
"$PY" -I -B "$S/check-supplement.py" --compose "$RUN/composed"
"$PY" -I -B - <<'PY'
import hashlib, pathlib
origin=pathlib.Path('evidence/operations/python-workspace-lock/composed/simple')
target=pathlib.Path('/opt/dsgeorref-python-inputs/simple')
assert not target.exists(), 'canonical registry path already exists; stop'
target.parent.mkdir(parents=True,exist_ok=True)
import shutil
shutil.copytree(origin,target)
def hashes(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
assert hashes(origin)==hashes(target)
PY
```

O composer reutiliza literalmente os arquivos simple e blocos de metadata históricos de nome/versão inalterados. Substitui por nome os registros de resolution-delta.json, retira tzdata e cria índice raiz com 54 nomes. Config final desativa Python download/build/fallback e mantém o resolver exato. No passe autorizado, guardar SHA-256 do config/índice composto em RUN antes de executar uv. Não alterar historical resolver-config.toml; o checker histórico não é adequado à closure nova e não deve ser alterado ou usado para atribuir PASS ao conjunto novo.

## Futura materialização de TASK-0773

Somente depois da emenda administrativa e autorização de execução futura, com bootstrap uv verificado e CPython externo provisionado. Estes comandos NÃO foram executados neste passe:

```bash
UV=/opt/dsgeorref-python-inputs/uv-x86_64-unknown-linux-gnu/uv
CONFIG="$RUN/composed/resolver-config.toml"
CACHE=/opt/dsgeorref-python-inputs/cache
cp "$S/supplement-pyproject-proposed.toml" pyproject.toml
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV" --config-file "$CONFIG" --cache-dir "$CACHE" lock --python "$PY" --no-python-downloads --no-build
"$PY" -I -B "$S/check-supplement.py" --check-lock uv.lock
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV" --config-file "$CONFIG" --cache-dir "$CACHE" lock --check --python "$PY" --no-python-downloads --no-build
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV" --config-file "$CONFIG" --cache-dir "$CACHE" sync --frozen --no-default-groups --python "$PY" --no-python-downloads --no-build
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 "$UV" --config-file "$CONFIG" --cache-dir "$CACHE" sync --frozen --no-default-groups --group dev --group test --python "$PY" --no-python-downloads --no-build
```

Repetir geração sem lock de preferência em outra checkout limpa do mesmo candidato com os mesmos inputs e registry canônico; exigir SHA-256 idêntico de uv.lock. Repetir sync com cache completo e --offline. Testar o conjunto reconciliado (incluindo runtime de credenciais/psycopg e groups dev/test) e registrar falhas reais, sem atribuir os ensaios antigos a novas versões. URLs indisponíveis, falha de checksum/metadata/marker, dependência adicional, erro de runtime/provenance ou conflito novo interrompem a operação. Não resolver com upgrade, mudança de pin, extras ou builds. Nenhum comando escolhe versão em tempo de execução.

O validador antigo de topologia do uv que exige manifests filhos continua com a limitação histórica registrada; não criar members/packages para satisfazê-lo. O checker suplementar verifica o root virtual existente e a closure exata. Qualquer mudança futura de ferramenta fora dos allow_paths exige seu próprio escopo.

Rollback do futuro workspace: reverter apenas pyproject.toml e uv.lock do candidato operacional, preservar sua evidência append-only e remover somente seu ambiente virtual dedicado após registro de integridade. Não tocar no graph histórico, suplemento revisado, Conda ou produto. Falha não libera benchmark, AP-003, imagem API ou TLS.
