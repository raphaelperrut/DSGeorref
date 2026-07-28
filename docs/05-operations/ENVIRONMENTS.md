# Ambientes

- **development:** dados sintéticos, execução local e sem exposição externa;
- **integration:** dependências reais efêmeras e fixtures controladas;
- **staging:** instalação equivalente ao alvo, com dados não sensíveis;
- **validation:** corpus representativo, benchmarks, segurança e restore;
- **production:** somente após G7 e decisão explícita do operador da instância.

A incubação privada do repositório é independente dos ambientes de runtime. Configuração deve ser validada no startup; secrets nunca ficam versionados.
