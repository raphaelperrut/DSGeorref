# Fase B — Requirements Review Charter

- **Baseline:** `2.6.0`
- **Owner:** `Product Owner`
- **Estado:** `CONCLUÍDA`
- **Objetivo:** revisar, para cada sprint, issue, critério de aceite e ADR aplicável, conflitos, redundâncias, requisitos ausentes, requisitos impossíveis e dependências circulares.

## Escopo

- 12 sprints;
- 869 issues, incluindo 110 envelopes de épico e 759 histórias implementáveis;
- todos os critérios de aceite e gates de sprint;
- 376 requisitos ativos;
- 22 ADRs;
- dependências de épicos e histórias.

## Fora de escopo

- implementação de código de produção;
- alteração de decisões arquiteturais aceitas sem novo conflito material;
- promoção de parâmetros `EVIDENCE_BOUND` sem benchmark.

## Critérios de saída

- cada critério possui identificador e ADR governante;
- cada requisito possui semântica implementável e evidência canônica;
- nenhum conflito ou requisito impossível permanece bloqueante;
- redundâncias são eliminadas ou classificadas como controles deliberados;
- DAGs de épicos e histórias permanecem acíclicos;
- relatório e matrizes passam no validador do repositório.
