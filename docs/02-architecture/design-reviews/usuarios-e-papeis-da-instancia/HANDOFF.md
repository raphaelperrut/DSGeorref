# Entrega contratual da STORY-0041

BC-002 · TASK-0041 · PR #1041 · política 1.1.0

O [ato Owner 6709165678](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6709165678) aprova o conteúdo contratual, a matriz concreta e o aceite parcial AC-04. A materialização parte de 0c325f1453be003ab3f6d39e9abe3cbcaa00a617, na branch codex/issue-117-contract. O SHA final, os resultados agregados e os pareceres sobre esse SHA são registrados no próprio PR.

## Conteúdo e rastreabilidade

policy.json publica as três concessões de autosserviço da própria conta ativa e o mapa de projeto. Owner lista e adiciona membros existentes com papéis registrados. Editor, reviewer e viewer somente listam. Administrador segue o vínculo e o papel efetivos do projeto. Autenticação mantém as capacidades, credenciais e transações do freeze. Os demais contratos são referenciados por suas oito operações existentes.

| Critério | Evidência |
| --- | --- |
| AC-ISSUE-0151-01 | policy.json versionado e CONTRACT.md com oito operações HTTP referenciadas |
| AC-ISSUE-0151-02 | test_req_auth_impl_007 e referência à máquina e ao schema de evidência de throttling do freeze |
| AC-ISSUE-0151-03 | Cenários negativos de alvo, projeto, estado, concessão, PAT, autoridade, proveniência e demais guardas, exigindo negação sem efeitos de sucesso |
| AC-ISSUE-0151-04 | Matriz concreta aprovada e test_epic_009_politica, com positivos por papel e negações de inclusão pelos demais papéis |

O avaliador em test_instance_policy.py interpreta somente a tabela de concessões e snapshots sintéticos server-side. Delega decisões de transporte, guardas e efeitos ao avaliador de conformidade já congelado. Ele permite verificar a política contratual. A demonstração de enforcement, I/O, durabilidade e produção pertence às histórias executáveis.

## AC-04

AC04_PARTIAL_REFERENCE=APPROVED, conforme o ato Owner acima. AC04_ORIGINAL_PACKAGE=MISSING. O arquivo AC04-RECONSTRUCTION-v1.md continua com os bytes aprovados no SHA de referência, hash SHA-256 do blob Git 935b2dcbfb73eaca6443f5c1620f0eaaa2bea97347c0e49b644e1364e3d35d95.

O aceite contratual exige os quatro critérios, a matriz concreta e seus testes. A reconciliação individual das 36 obrigações, 20 vínculos G2 Access, dois vínculos Identity e oito testes históricos permanece com as histórias responsáveis e a consolidação STORY-0045. Qualquer lacuna contratual necessária ao consumidor deve ser resolvida antes do consumo. Equivalência histórica e reprodução dos três digests originais permanecem sem comprovação.

## Validação e limites

A seleção com os testes desta entrega, os 170 testes do freeze e o teste existente de idempotência de membros passou com 321 testes em CPython 3.12.13. Ruff e git diff --check são verificações direcionadas adicionais. A seleção usa pytest explícito nos paths de contrato, pois a descoberta padrão começa em tests/.

O make verify utiliza Python 3.12.13, Node 24.20.0 e pnpm 10.26.1. A execução aplica core.longpaths=true somente ao ambiente dos subprocessos Git. O diagnóstico anterior demonstrou sete falhas idênticas na baseline e no candidato por Filename too long e sete passes em ambos com esse ajuste. O drift OpenAPI anterior foi resolvido por alinhamento de node_modules ao lockfile. Artefatos gerados permanecem os da baseline.

A validação isolada de specifications captura somente a escrita do relatório global em memória. Essa captura preserva os arquivos fora de scope e mantém os resultados e a lógica do verificador. A execução integral de make verify pode regenerar relatórios de verificação, cujos deltas devem ser conferidos e restaurados fora deste escopo.

A extensão exata de ownership foi concedida pelo [ato 6708825127](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6708825127) e registrada no checkpoint documental 802d1003f7f457734097d726c1645bffd07071fd. Os dois registros BC-002 permanecem no catálogo. O verificador ordinário continua lendo somente o envelope original e conserva PATH_OUTSIDE_EFFECTIVE_SCOPE para esse catálogo. A conferência da extensão permanece vinculada ao ato e ao diff exato.

O READY ordinário retornou FAIL para STORY-0040 e STORY-0025 no candidato anterior. O verifier DAA vigente retornou FAIL/GOVERNANCE_MODE_UNAUTHORIZED para TASK-0041, ausente das políticas solo assinadas. Esses veredictos devem ser repetidos no SHA final e registrados no PR. O ato de conteúdo mantém a integração condicionada aos gates aplicáveis.

## Revisões e integração

QA, Reviewer e Security avaliam o novo SHA em sessões funcionalmente separadas. Os pareceres e o resultado da CI vinculam o SHA final no PR, com limitações reais. Independência pessoal é ausente no modelo solo. Passes Codex e decisão de conteúdo não conferem aprovação DAA ou autoridade de merge.

Migration não se aplica à entrega contratual. Rollback por reversão dos commits da entrega. O PR permanece draft para a decisão final de integração.
