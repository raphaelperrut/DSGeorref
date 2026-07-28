# Padrões de código

- linguagens, versões e ferramentas estão fixadas nas regras consolidadas em AP-001 e serão materializadas na SPRINT-001;
- tipagem estática e lint serão obrigatórios onde houver suporte maduro;
- funções preferencialmente pequenas; módulos acima de 500 linhas exigem plano de decomposição;
- erros de domínio são tipos específicos; boundaries preservam causa e contexto;
- I/O, clock, rede, filesystem e providers são injetáveis em testes;
- toda operação destrutiva exige autorização, idempotência quando aplicável e auditoria;
- caminhos são representados internamente por identificador de raiz + path relativo, não por strings absolutas oriundas do frontend;
- CLI, API e worker devem produzir comportamento semântico equivalente para o mesmo caso de uso.

## Baseline de qualidade aprovada

- Python: Ruff e mypy progressivamente estrito;
- frontend: TypeScript strict, Vitest, Testing Library e Playwright;
- integração: pytest com PostGIS/RabbitMQ reais quando a semântica depender desses serviços;
- dependências: locks frozen e atualizações somente por PR;
- entrypoints: Make como façade comum de desenvolvimento e CI.
