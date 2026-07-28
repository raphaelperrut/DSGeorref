# Capacidade e escala — baseline 3.0

## Decisão executiva

O produto inicial é uma instalação única, modular e orientada a escala vertical. Ele não possui claim de alta disponibilidade, banco distribuído ou scale-out multi-host. Workers podem operar em múltiplos processos na mesma instalação, mas PostgreSQL/PostGIS e filesystem gerenciado permanecem authorities únicas.

## Envelope suportado

- lotes usuais de 40, 100 e 300 imagens são classes obrigatórias de benchmark;
- catálogo de centenas de milhares de registros deve usar paginação e filtros server-side;
- raster, matching, mosaico e relatórios operam out-of-core;
- fan-out depende de budget de CPU, RAM, I/O, disco e GPU;
- throughput e concorrência somente são publicados após BP-001, BP-002 e BP-004.

## Classes de teste, não promessas de capacidade

A SPRINT-001 cria classes de deployment por CPU, RAM, NVMe e GPU opcional. Cada classe recebe digest de ambiente, corpus, limites e resultado. Uma classe sem benchmark é `UNSUPPORTED`, mesmo que a aplicação inicie.

## Gargalos esperados

1. IOPS e espaço temporário do filesystem;
2. PostgreSQL em consultas espaciais, outbox, audit e scheduler;
3. CPU/RAM na pirâmide raster e matching;
4. fila e admission control sob fan-out;
5. VRAM e residência de modelos quando IA for habilitada.

## Decisão sobre GPU

CPU-only é obrigatório em toda release. GPU não é adquirida nem exigida pela arquitetura. A ativação requer equivalência científica, ganho medido e custo unitário aceito pelo Owner. Falha ou ausência de GPU retorna ao caminho CPU/classic sem alterar autoridade do SGV.

## Limite estratégico

Requisito de HA, active-active, object storage obrigatório, banco distribuído ou workers multi-host fora de uma única trust zone exige nova ADR e novo investment review.
