# Regras de dependência e modularidade

## Direção permitida

```text
HTTP / CLI / Worker / UI
          ↓
      Application
          ↓
        Domain

Adapters concretos ──implementam──> Ports definidos para fora
Bootstrap ──compõe──> Application + Adapters
```

O pipeline geoespacial e a IA são capabilities com ports tipados. Não importam API, frontend, worker, ORM ou filesystem concreto. PostgreSQL e filesystem são implementações de ports; RabbitMQ é transporte e nunca autoridade de estado.

## Proibições

- import circular entre packages ou módulos;
- regra de negócio em rota, command handler CLI, task Celery, componente React ou migration;
- acesso direto de um módulo à tabela, path ou secret de outro boundary;
- módulo `common`, `utils`, `helpers` ou `shared` sem responsabilidade e owner explícitos;
- duplicação de caso de uso para cada interface;
- código organizado por `epic-*`, `issue-*`, sprint ou agente;
- dependência de Python 3.13/3.14 na baseline 3.12.

## Integração entre contexts

Cross-context ocorre por port, DTO/schema versionado, evento ou artifact manifest. Toda exceção exige ADR, justificativa, teste de arquitetura e plano de remoção.

## Fitness functions

`tools/check_python_architecture.py` verifica limites de arquivo/função, importações proibidas, ciclos e duplicação exata de implementações não triviais. `tools/validate_repository.py` verifica rastreabilidade, contratos, DAG e prontidão dos TaskEnvelopes.
