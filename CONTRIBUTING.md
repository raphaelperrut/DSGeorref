# Contribuição

## Durante a incubação privada

O desenvolvimento é conduzido pelo mantenedor único. O fluxo de trabalho permanece rastreável mesmo sem equipe:

1. selecionar uma issue ou épico;
2. criar branch curta vinculada ao identificador;
3. registrar plano, riscos, testes e rollback;
4. implementar a menor mudança coerente;
5. executar checks e anexar evidências;
6. revisar o diff com Codex e, para mudanças críticas, buscar revisão humana externa quando disponível;
7. integrar somente após critérios de aceite satisfeitos.

Commits devem ser claros e vinculados à issue. Conventional Commits é recomendado, não substitui rastreabilidade.

## Após a publicação

Quando o repositório for aberto, pull requests externos exigirão `Signed-off-by` conforme DCO 1.1, `inbound=outbound`, SPDX/REUSE e provenance verificável. Durante a incubação privada, contribuições externas permanecem fechadas pelo gate de publicação.
