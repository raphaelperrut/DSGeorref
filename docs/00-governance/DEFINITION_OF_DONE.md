# Definition of Done

Uma mudança só está Done quando:

- implementação e testes obrigatórios foram concluídos dentro do escopo aprovado;
- artifacts gerados e contratos estão sincronizados;
- migrations e rollback foram validados quando aplicável;
- invariantes de segurança, privacidade, geoprocessamento e ciência passaram;
- critérios de aceitação foram demonstrados por evidência no pull request;
- QA registrou aprovação independente;
- Reviewer registrou aprovação final;
- documentação e rastreabilidade foram atualizadas;
- a autoridade humana realizou o merge do commit aprovado.
## CTO completion

Done requires evidence for applicable CTO controls on the same candidate commit. Production claims additionally require the relevant G-CTO gate.

## Segregação funcional no regime solo — ADR-060

QA e final review continuam obrigatórios em passes e contextos distintos do
Executor, sobre o mesmo candidato. Ausência de independência pessoal é declarada;
requisitos estritos e DAA/trust mantêm-se. A exceção da #1026 não conclui Done
nem dispensa merge humano.
