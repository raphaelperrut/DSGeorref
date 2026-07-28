# Protocolo de integração

1. Congelar e integrar a revisão contratual.
2. Regenerar clientes e bindings de schema.
3. Executar lanes sobre o mesmo digest de contrato.
4. Integrar domínio e migrations antes dos adapters.
5. Executar suites de integração e E2E em ambiente limpo.
6. Produzir evidência imutável de QA.
7. Executar final review no commit candidato exato.
8. Autoridade humana integra somente o commit revisado.

Rebase ou mudança de código após QA invalida evidências de QA e final review.
