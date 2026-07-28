# AP-009 — First functional georeferencing slice

- **Status:** `Accepted`
- **Owner ADRs:** ADR-002, ADR-018, ADR-046, ADR-044 e ADR-041

## Aplicação

A primeira fatia processa uma imagem contra uma referência local autorizada, preserva snapshot imutável dos inputs e executa `ProcessingPlan` mínimo. Usa baseline clássica, homografia/USAC_MAGSAC, SGV obrigatório, COG/ArtifactSet e relatório por imagem. REST, CLI e runners direto/assíncrono chamam o mesmo application service.

O gate de promoção é estratificado, multidimensional e inclui equivalência entre runners. Falhas elegíveis podem acionar o AP-010; IA não é requisito para concluir a baseline clássica.
