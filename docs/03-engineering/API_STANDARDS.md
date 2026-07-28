# Padrões de API

Rotas sob `/api/v1`; IDs opacos; paginação consistente; idempotency key para criação; erros no formato Problem Details; correlation ID; OpenAPI versionado; autorização por papel, projeto, operação e recurso.

Downloads usam streaming autorizado ou URLs temporárias quando o backend de storage suportar. Endpoints administrativos não compartilham o mesmo privilégio de operadores. Caminhos absolutos do servidor não devem ser retornados ao frontend salvo em interfaces administrativas explicitamente protegidas.

## Contratos de lote aceitos — AP-011

Os contratos de API deverão representar `BatchRun`, `ImageRun`, tentativa, work unit, estado agregado, progresso com confiança, cancelamento escopado e paginação server-side de resultados. A composição é governada pela AP-011 e pelas ADRs canônicas de scheduler, retries, checkpoints e cancelamento.

## Adapter concreto aprovado — ADR-002

FastAPI será o adapter HTTP; Pydantic representa somente fronteiras de transporte. OpenAPI é artifact versionado e gera o cliente TypeScript. Domain models, schemas de transporte e modelos SQLAlchemy permanecem separados conforme ADR-002. UoW, idempotência persistente e geração do cliente seguem AP-002.
