# Governança

**Issue → Código → Testes → PR → CI/Revisão → Merge**

- Use GitHub Issues para resultado, escopo, critérios testáveis, responsável e dependências. Use sub-issues para entregas próprias, milestones para os incrementos e Project como visualização.
- Registre pré-requisitos técnicos em **Blocked by** e indique na issue qual contrato ou resultado é consumido. Antes de alterar a relação, percorra o subgrafo de predecessores com paginação e verifique ciclos sob demanda, por exemplo com a ordenação topológica de `graphlib.TopologicalSorter`. Inclua autoarestas e trate leituras incompletas ou referências inacessíveis como pendências. Confirme no código integrado o resultado esperado. Encerramento por deferral não satisfaz uma dependência.
- Use o [catálogo de módulos](docs/02-architecture/MODULE_CATALOG.md) e o [mapa de contextos](docs/02-architecture/ddd/CONTEXT_MAP.csv) para responsabilidade técnica e [CODEOWNERS](.github/CODEOWNERS) para encaminhar a revisão. Coordene mudanças em paths compartilhados na issue e no PR. Integre interfaces versionadas antes dos consumidores paralelos. Registre decisões arquiteturais materiais em ADR.
- Vincule a issue no PR e registre testes, riscos e compatibilidade aplicáveis. A revisão técnica é proporcional ao risco e considera o SHA candidato. A autoridade humana integra o candidato revisado com os checks obrigatórios verdes e as conversas resolvidas. Preserve revisão especializada e independência pessoal quando exigidas. Sessões de agentes não constituem pessoas independentes.

Consulte [Ready](docs/00-governance/DEFINITION_OF_READY.md), [Done](docs/00-governance/DEFINITION_OF_DONE.md) e o [roadmap](docs/06-delivery/ROADMAP.md).

## Vigência e histórico

A [decisão da #1047](https://github.com/raphaelperrut/DSGeorref/issues/1047#issuecomment-6730087033) substitui, a partir da integração deste corte, as disposições operacionais incompatíveis das ADR-006, ADR-007, ADR-059 e ADR-060 e das normas BC-001 correlatas. A supersessão abrange TaskEnvelopes obrigatórios, checkpoints de autoridade, atribuição por commit e composição B/K/I/C, DAA V1/V2 e trust por tarefa, Delivery Gates administrativos, registros duplicados de READY, sincronização de backlog e aprovações formais duplicadas. Para uma entrega parcial, use o resultado integrado e seu teste de contrato como referência na issue consumidora.

O [baseline anterior ao corte](https://github.com/raphaelperrut/DSGeorref/tree/559e1368efe9fdf31a74f8406f28adb9b2f0d10c) preserva as normas, ferramentas e testes históricos. Consulte-o para reproduzir um veredito com seus bytes, versão, trust e instante originais. Registros sob `.codex/tasks/`, `.codex/roles/`, `.codex/policies/`, evidências, catálogos de estado CSV/JSON, DAGs e backlogs versionados de entrega são snapshots. Os validadores administrativos, ferramentas de materialização e sync em `tools/` e testes correspondentes servem à consulta e reprodução histórica. O [mapa de materialização](.github/dsgeorref-materialization-map.json) permite localizar os IDs existentes no GitHub.

Requisitos de produto, contratos, ADRs técnicos, licenciamento, assinaturas de publicação e Prompt Bundles, controles científicos, [gates de produção](docs/05-operations/PRODUCTION_READINESS_GATES.md) e obrigações externas aplicáveis continuam vigentes em seus respectivos escopos.

## Reversão do corte

Pause integrações e recupere os produtores legados com um PR de revert sob os checks técnicos vigentes. Se um produtor obrigatório impedir a recuperação, valide um produtor técnico substituto antes de uma troca administrativa registrada. Restaure contextos anteriores somente após confirmar que seus produtores voltaram a emitir resultados para PRs. Preserve PR obrigatório, checks estritos, resolução de conversas, bloqueios de exclusão e force-push e ausência de bypass. Registre o SHA restaurado e a configuração efetiva. Reavalie cada trabalho iniciado após o corte com suas evidências originais.
