# Definition of Ready

Uma issue só está Ready quando possui:

- um épico pai e uma sprint atribuída;
- resultado de produto e critérios de aceitação;
- ADRs, profiles, contratos e riscos aplicáveis;
- dependências explícitas e sem ciclo;
- decomposição do Tech Lead e file scope limitado;
- plano de testes e evidência;
- implementador, QA e Reviewer definidos;
- tratamento de migration, compatibilidade, segurança e rollback quando aplicável;
- nenhuma decisão material pendente.


## Gates incorporados pela Fase A

- máximo de 10 requisitos por história implementável;
- write scope derivado de capability estável;
- contrato `FROZEN` antes de abrir consumidores paralelos;
- ausência de decisão normativa é condição de parada;
- task que exige stack Python referencia o lock 3.12.13 e o gate ABI.
## CTO readiness

A story is Ready only when its TaskEnvelope partitions all CTO controls, identifies required evidence and contains no unbudgeted production claim. Version 1.7.0 preserves 1.6.0 envelopes and adds optional delivery gates.

## Delivery gates — ADR-006

`dependencies` continua igual aos predecessores Story→Story. Gate parcial é uma
primitive distinta: não conclui a Story owner e ausência de gates permanece válida.
Planejamento com gate pendente é válido; consumer não está READY enquanto todos seus
`delivery_gate_dependencies` não estiverem SATISFIED no consumer base.
O Tech Lead deve executar `python tools/validate_repository.py --ready-task <TASK-ID>
--consumer-base <SHA>` antes de liberar execução. Scope parcial do owner verifica
somente `stage_story_dependencies`; fora dele aplicam-se predecessores integrais.
Definição vigente, evidências independentes DAA e integração humana na baseline
canônica são obrigatórias; alteração de definição invalida satisfação anterior.
