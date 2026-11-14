# Adendo de handoff — avaliação do achado MEDIUM de QA

Candidato avaliado e preservado: `16a8c928244a3deb72dcedcbac196090e3b47cf5`.
Entrada fornecida pelo Owner nesta continuação: `QA_RESULT=PASS_WITH_FINDINGS`.
Este documento registra a avaliação do executor; não constitui nova aprovação de QA.
As evidências do candidato revisado permanecem intactas. Este adendo e os relatórios
associados são arquivos suplementares locais, sem novo commit ou PR, para preservar
o SHA conforme a alternativa 5 da instrução do Owner.

## Conclusão

`MEDIUM_FINDING_STATUS=RESIDUAL`; `SAFE_REUSE_AVAILABLE=NO` sob todas as restrições
da tarefa. Nenhuma remediação de produção foi aplicada. A correção adequada exige
modificar o produtor para publicar uma composição seletiva/hook com os dados de
erro e invalidação necessários. Isso está fora do write scope e foi expressamente
proibido nesta continuação. Não se propõe framework, package ou shared layer.

Há repetição efetiva de orquestração de sessão, quatro chamadas ao SDK, expiração,
serialização de requests, correlação de memberships, chaves e ciclo de pedidos.
Os dois hooks atendem a responsabilidades sobrepostas de BC-002; a distinção de
apresentação da nova tela não elimina nem reclassifica toda essa repetição como
semelhança superficial. Não há duas políticas de autorização: ambos delegam ao
servidor, usam o mesmo SDK e reutilizam os mesmos guards/redaction existentes.

## Alternativas verificadas no código do candidato

Paths nesta tabela são relativos a
`src/frontend/src/contexts/identity_access/features/`.

| Alternativa | Constatação objetiva | Decisão |
|---|---|---|
| Reutilizar `contas-locais-bootstrap-unico-sessoes-tokens-e-adapter/index.tsx` | Linhas 4–7 exportam somente `IdentitySurface` e `mountIdentitySurface`. O README confirma esses dois exports como superfície publicada. | API pública disponível, mas não é uma composição seletiva das quatro operações necessárias. |
| Montar `IdentitySurface` diretamente | `identity-surface.tsx:9` não recebe props; instancia seu próprio hook e renderiza oito operações, incluindo bootstrap, OIDC, token e logout. | Substituir a tela por ela amplia os fluxos exibidos. Ocultar painéis por DOM/CSS dependeria de detalhes internos; não fornece os comportamentos adicionais de erro/invalidação. |
| Importar `useIdentityAccess` diretamente | O símbolo é exportado pelo módulo interno `use-identity-access.ts:23`, mas não pelo entrypoint público. O retorno não publica `invalidate`, reset/setter dos resultados ou transporte configurável por instância. | Criaria nova dependência em detalhe interno sem cumprir a restrição de API publicada estável. Export TypeScript por arquivo não equivale ao boundary publicado no README/index. |
| Adaptar os resultados do hook existente | `Outcome` em `use-identity-access.ts:18` não carrega status HTTP bruto. Em `run`, o caminho de erro só expõe o status se houver Problem válido; `catch` perde a Response. `options()` não seleciona `parseAs: "text"`. | Um wrapper local não recupera informação já descartada. A nova tela preserva HTTP 200/403/500 mesmo com JSON malformado (`use-project-access.ts:50`, `:56`, `:76`, `:87`), comportamento explicitamente testado. |
| Adaptar edição e reenvio | O hook existente não publica invalidação de decisão; conserva resultados por operação. Seu `catch` chama `clearIdentity()`, inclusive em falha de rede. A nova tela invalida resultado na edição e mantém a sessão em falha de comunicação do vínculo para reenvio sem edição/chave nova. | A troca direta altera o fluxo testado de resposta perdida → reenvio com mesma chave. Isso não acusa falha de autorização no hook existente; são comportamentos distintos que precisam ser preservados nesta tarefa. |
| Reutilizar `OperationPanel` interno | O ciclo de chaves fica nos formulários, não só nos hooks. O painel existente reseta o formulário inteiro após sucesso, não oferece callback público de invalidação e sua apresentação não exibe `Problem.code` como campo. A nova tela mantém parâmetros, limpa senha e apresenta todos os campos aplicáveis. | Também não é substituição pública compatível. Um wrapper que refaça esses comportamentos mantém a duplicação e não resolve a perda de status no hook. |
| Extrair/manter dois hooks com novo framework ou interceptar globalmente o cliente | Exigiria novo boundary ou efeitos compartilhados para observar Response/dados descartados. | Rejeitado por escopo, risco de acoplamento e instrução explícita; nenhuma dessas alternativas foi implementada. |

Sessão, check, listagem e vínculo estão presentes em ambos os hooks. Portanto, a
ausência de alguma das quatro operações não é a razão da recusa: os bloqueios são
o boundary publicado e a preservação objetiva dos comportamentos de AC_03/AC_04.
O import de guards/redaction já existente no candidato não foi alterado nem
estendido para consumir outros módulos internos. Nenhuma aresta de dependência
nova foi introduzida; não há novo risco de ciclo nesta avaliação.

## Verificação focada e integridade

Executado somente o arquivo frontend co-localizado `surface.test.tsx` da nova
feature: **28 PASS, zero falhas/skips**, incluindo `test_epic_010_superficie`.
Relatórios novos: `focused-tests.log` e `focused-tests.xml`.
São testes da implementação preservada, não um ensaio de substituição pelo hook
antigo. As incompatibilidades acima foram avaliadas por inspeção estática.

Os testes verificam negativa, Problem Details, status com JSON malformado,
expiração/resposta tardia, invalidação ao editar, chave mantida após falha de rede,
CSRF e correlação dos membros. Nenhum teste backend, banco, browser adicional ou
`make verify` foi repetido: não houve mudança de código e o Owner restringiu esta
etapa à avaliação mínima/testes frontend afetados. O resultado global anterior de
make verify e sua classificação preexistente continuam registrados no handoff
original; este adendo não o transforma em PASS.

`assessment.json` registra SHA, digests dos arquivos inspecionados, verificação de
que todos os arquivos rastreados continuam iguais ao candidato e integridade das
evidências originais. Não foram alterados TaskEnvelope, allow_paths, contratos,
feature preexistente, código da nova feature ou testes.

## Risco residual e encaminhamento

Mudanças futuras em sessão, HTTP, expiração ou reenvio poderão exigir atualização
coordenada em duas orquestrações; há risco de divergência e custo de manutenção.
O achado MEDIUM continua aberto para decisão de Reviewer/Owner. Uma eventual
correção precisa de escopo próprio no produtor, publicação de boundary apropriado
e verificação dos dois consumidores; não é requisito que se crie uma camada genérica.
Não se declara o achado resolvido, a correção autorizada ou nova aprovação de QA.

Fail-closed, Problem Details, idempotência e os quatro contratos são preservados
porque a implementação do candidato não mudou, e os testes focados passaram.
`READY_FOR_QA=YES` para reavaliação/disposição do achado no mesmo candidato, com o
risco residual e a limitação preexistente do gate global explicitados. Nenhum PR
foi aberto. `src/frontend/debug.log` continua preexistente e fora da entrega.
