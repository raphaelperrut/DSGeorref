# Política de runtime Python 3.12

## Decisão

A implementação inicial do DSGeorref usa **CPython 3.12.13** como pin reproduzível da linha 3.12. Python 3.13 e 3.14 são alvos de atualização futura, não requisitos atuais e não podem introduzir comportamento condicional no código de domínio.

## Configuração normativa

- `.python-version`: `3.12.13`;
- `pyproject.toml`: `requires-python = ">=3.12,<3.13"`;
- Ruff: `target-version = "py312"`;
- mypy: `python_version = "3.12"` e modo strict;
- CI inicial: somente 3.12 para o gate obrigatório;
- patch inicial: `3.12.13`; imagem OCI, lockfile e digest resolvido são vinculados ao mesmo commit candidato; tags `latest` são proibidas.

## Compatibilidade futura

### Python 3.13

A lane 3.13 é criada como experimento isolado e não bloqueante. Ela não altera o suporte oficial nem permite sintaxe 3.13 no código. A promoção exige o `PythonRuntimeGate` do AP-001.

### Python 3.14

A lane 3.14 somente é aberta depois de a lane 3.13 estar estável. Não é permitido saltar diretamente de 3.12 para 3.14 como runtime primário.

## Regra de código

- usar apenas recursos da linguagem e standard library disponíveis em 3.12;
- evitar branches `if sys.version_info` no domínio; compatibilidade deve ficar em adapters isolados;
- não adicionar backport ou polyfill sem issue e owner explícitos;
- qualquer dependência que abandone 3.12 exige substituição, pin compatível ou início antecipado do gate de atualização;
- o prazo operacional para concluir a migração deve preceder o fim do suporte de segurança da série 3.12.

## Evidência

- `test_python_312_primary_and_upgrade_gates`;
- teste de importação da stack completa na imagem nativa;
- teste de wheel/ABI e smoke geoespacial;
- lock diff, SBOM, benchmark e rollback para lanes futuras.


## Pin inicial da Fase A

- CPython: `3.12.13`;
- lock de fontes nativas: `infra/images/native-stack.lock.yaml`;
- digest/SBOM/provenance: produzidos e assinados pela SPRINT-001 em `native-stack.resolved.yaml`;
- a ausência do digest antes do build não autoriza tag flutuante nem escolha implícita.
