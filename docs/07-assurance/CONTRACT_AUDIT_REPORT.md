# Auditoria dos contratos arquiteturais

- **Baseline:** `2.6.0`
- **Resultado:** `PASS`
- **OpenAPI:** `3.1.0`
- **Operações HTTP:** `56`
- **Operações congeladas:** `56`
- **Contratos por operação:** `56`
- **Schemas OpenAPI:** `125`
- **JSON Schemas independentes:** `19`

## Verificações

- catálogo e OpenAPI possuem o mesmo conjunto de operações;
- cada operação declara permissão, idempotência, respostas e códigos de erro;
- requests e responses usam schemas específicos;
- todas as referências locais do OpenAPI resolvem;
- JSON Schemas seguem Draft 2020-12;
- cada operação possui contrato Markdown com request, response, erros e regras;
- nenhum envelope genérico `CommandRequest` ou `ResourceEnvelope` permanece.

## Divergências

Nenhuma.
