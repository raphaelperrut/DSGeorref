# Extensão pontual de ownership

O [ato Owner 6708825127](https://github.com/raphaelperrut/DSGeorref/issues/117#issuecomment-6708825127), consultado pelo conector autenticado, autoriza duas linhas no catálogo de ownership para corrigir o P1 do PR #1041. Autor do ato no GitHub é `raphaelperrut`, user ID `110496238`. A execução parte do candidato `e3fcdff99a9a9a46598b4c76b93b1418d1b5a939`, na branch `codex/issue-117-contract`.

O path adicional autorizado é `contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv`. As inclusões permitidas são exatamente as seguintes, mantendo cabeçalho, entradas existentes e ordenação canônica.

```csv
contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia/policy.json,BC-002,contexts,VERSIONED,NO
contracts/contexts/identity_access/plt/usuarios-e-papeis-da-instancia/test_instance_policy.py,BC-002,contexts,VERSIONED,NO
```

Este registro precede a edição do catálogo. O commit que o materializa é o checkpoint documental desta extensão, a ser identificado pelo Git no relatório da execução. O envelope TASK-0041 continua com os dois scopes originais. Seu blob Git no candidato de partida tem SHA-256 `11d7e118ecb3e34e05d6bd75e6d546d4a12b3c2260f7a79e1c57c1ff7d2178ee`.

O verificador ordinário de escopo lê os allow paths do envelope no checkpoint e não recebe atos externos como argumento. Portanto, a autorização do catálogo deve ser conferida diretamente contra o ato e o diff de duas linhas. O resultado ordinário será registrado com seu eventual finding de path fora do envelope. Este documento conserva a distinção entre a extensão específica concedida pelo Owner e o resultado do verificador.

A conferência exige ancestralidade do checkpoint ao novo candidato, integridade do TASK-0041 e adição exclusiva das duas linhas. A política do papel Arquiteto já permite `contracts/**`. Os scopes de conteúdo contratual e design review permanecem os declarados no TASK-0041. READY, matriz parametrizada, reconstrução AC04, QA, Reviewer e gates de integração mantêm seus resultados próprios.
