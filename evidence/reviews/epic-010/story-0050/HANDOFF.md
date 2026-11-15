# Handoff parcial — ISSUE #126 / TASK-0050

Baseline: `7062b1432479e256cc673b5b313932e9b41dcecf`.
Branch: `codex/issue-126-final-audit`.
O candidato documental é o commit que introduz este pacote. Resolver o SHA exato
com `git log -1 --format=%H -- evidence/reviews/epic-010/story-0050/HANDOFF.md`.
QA e Reviewer devem usar esse único SHA, os mesmos arquivos deste diretório e os
riscos R-01 a R-04 de AUDIT.md. Se o candidato mudar, não reutilizar aprovação.
Não há autorreferência de hash nem afirmação de revisão independente concluída.

## Entrega

- Envelope: somente duas allow_paths corrigidas, com exceção nominal temporária
  para a correção do próprio envelope. Demais campos semanticamente preservados.
- Dependência #125: closed/completed e integrada na baseline pelo merge #1063.
- integrated-artifacts.json: commits, merges e Git object IDs da baseline para
  os artefatos das seis histórias, incluindo rename do teste de segurança.
- TRACEABILITY.csv: matriz parcial; separa observações históricas de verificação final.
- mandatory-search.log e mandatory-selection.log/xml: testes exigidos ausentes;
  nenhum executado, exit 5, 184 desmarcados na seleção das suítes pertinentes.
- make-verify.log: FAIL ambiental por Chromium ausente na sandbox, exit 2.
- AUDIT.md: conclusão parcial, condição de parada e riscos herdados.

O arquivo preexistente e não rastreado src/frontend/debug.log foi preservado e
excluído do commit. Nenhum código, helper, teste, contrato, ADR, migration, workflow,
policy ou regra de produto foi criado/modificado. API/database/frontend/geo/AI
inalterados; migration_required=false.

## Retomada necessária

F-01 impede o fechamento solicitado: os testes nomeados obrigatórios não existem.
É necessária definição do Owner sobre mapeamento explícito para node IDs existentes
ou uma baseline que já contenha os testes. Não foram inventados substitutos nem
aberta issue de remediação. Após resolver isso, concluir a auditoria e executar a
evidência pertinente no candidato final, com QA/revisão independentes e gate global.
Não interpretar este handoff como aprovação ou liberação de downstream/release.

READY_FOR_QA_REVIEW=NO. STOP_CONDITION=MANDATORY_ACCEPTANCE_TESTS_ABSENT.
Nenhum PR aberto. Este é um commit de diagnóstico parcial, não de aceite final.
