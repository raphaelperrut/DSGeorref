# Padrões de integração entre contexts

- **Open Host Service + Published Language:** APIs e schemas públicos estáveis.
- **Customer/Supplier:** downstream participa da evolução do contrato, sem importar o modelo upstream.
- **Anti-Corruption Layer:** obrigatório para providers, OIDC, modelos de IA e qualquer semântica externa.
- **Process Manager:** `BC-010` coordena execução técnica; `BC-004` coordena workflow de produto.
- **Domain Events:** propagam fatos após commit; consumidores são idempotentes.
- **Separate Ways:** preferido quando compartilhar modelo reduzir autonomia ou criar ciclo.

## Shared kernel

Não existe shared kernel de domínio na baseline. O compartilhamento permitido limita-se a primitivas técnicas sem semântica de negócio: IDs tipados, clock, envelope de erro, paginação e tracing. Qualquer novo conceito compartilhado exige ADR.
