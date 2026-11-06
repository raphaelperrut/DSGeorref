# Proposta de reconstrução AC-04 v1

AC04_ORIGINAL_PACKAGE=MISSING · aprovação específica pendente

A busca cobriu a árvore pós-#1040, refs e histórico Git locais, árvores dos commits locais não alcançáveis por refs, worktrees acessíveis e registros da reconstrução #1026. Os três arquivos fixados na decisão de identidade não foram localizados. Seus SHA-256 históricos permanecem vinculados aos originais. Esta proposta tem identidade própria e cobertura limitada.

| Obrigação recuperável | Fonte | Destino ou evidência |
| --- | --- | --- |
| Política versionada, papéis, permissões, transições, exceções e erros | Decisão da #117 e AC-ISSUE-0151-01/03/04 | STORY-0041, contrato e teste de conformidade |
| Estado e evidência observável de throttling | AC-ISSUE-0151-02, REQ-AUTH-IMPL-007, freeze BC-002 | STORY-0041 referencia o contrato. STORY-0712 preserva o núcleo persistente. STORY-0714 consome o controle derivado |
| Identidade administrativa | REQ-ID-002 e decisão da #117 | STORY-0715 |
| Consolidação e integração | Decisão da #117 | STORY-0042 |
| Superfície administrativa | Decisão da #117 | STORY-0043 |
| Duas suítes de segurança | Decisão da #117 | STORY-0044 |
| Verificação final | Decisão da #117 | STORY-0045 |
| 20 vínculos G2 Access e dois vínculos ao gate Identity | Contagens aprovadas na #117 | Gates distintos. Ligações individuais pendentes de comprovação |
| Oito testes então não localizados | Registro da #117 | Pendências históricas. Nomes e ligações individuais não reconstruídos |

A lista acima identifica grupos verificáveis nas fontes canônicas e nos comentários da [Issue #117](https://github.com/raphaelperrut/DSGeorref/issues/117). A matriz integral das 36 obrigações continua sem validação. O [change control da #1026](../../../00-governance/CHANGE_CONTROL.md) registra a exclusão dos artefatos da reconstrução integrada.
