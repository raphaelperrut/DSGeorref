# Fundação executável do catálogo de capacidades

Esta fundação materializa o catálogo técnico versionado previsto por
`REQ-AI-007` sem implementar o runtime das capabilities. As três entradas são
projeções dos owners e boundaries já publicados em `MOD-005`, `MOD-006` e
`MOD-007`; todas permanecem em `DOWNSTREAM_STORIES_ONLY`.

O manifesto de corpus contém somente sentinelas sintéticas para exercitar
origem, licença, SHA-256, segregação de splits e classes de acesso exigidas por
`REQ-TST-001`. Ele não é corpus científico, não contém benchmark promovido e
não sustenta claim de qualidade, custo ou escala.

O mesmo comando offline é o entry point local e de CI:

```text
python tools/governance/catalogo-de-conhecimento-tecnico-e-decomposicao-das-ca/validate_catalog.py
```

O comando emite um relatório JSON determinístico. Descriptor desconhecido,
drift do contrato congelado, source ausente ou executável, owner duplicado,
hash inválido, sobreposição de split ou checkpoint com fallback silencioso
produz finding estável e exit code `2`.

## Limites e rollback

- O `GET /capabilities` continua sendo apenas a projeção pública congelada; a
  fundação não cria endpoint, persistência, broker, ModelPack ou backend.
- Os sentinelas provam o control path, não proteção operacional de um corpus
  real; promoção e acesso a corpora reais pertencem às histórias downstream.
- Migration e rollback operacional não se aplicam. Rollback é a reversão do
  commit candidato antes de qualquer consumo downstream.
- QA e Reviewer independentes ainda devem validar o mesmo SHA candidato.
