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

A story is Ready only when its TaskEnvelope 1.6.0 partitions all CTO controls, identifies required evidence and contains no unbudgeted production claim.
