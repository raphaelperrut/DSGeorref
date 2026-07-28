# SPEC-001 — Prompt Bundle Contract

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-001`
- **ADRs governantes:** `ADR-006`, `ADR-007`, `ADR-008`, `ADR-057`
- **Bounded Contexts:** `BC-001`
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Propósito

O Prompt Bundle é o pacote imutável e verificável que determina como um agente recebe políticas, papel, contexto de domínio, tarefa, restrições, exemplos e contrato de saída. Ele transforma prompts permanentes de uma ideia textual em um artefato de engenharia versionado. O bundle não substitui ADR, requisito, especificação, contrato ou TaskEnvelope; ele apenas os compõe de modo determinístico e registra exatamente o material entregue ao agente.

A finalidade primária é reduzir alucinação operacional. Um agente não deve escolher livremente quais instruções ler, inferir precedência ou concatenar trechos ad hoc. O resolver recebe uma identidade e uma versão, verifica compatibilidade, resolve herança, valida fragmentos, calcula hashes, confere assinatura e produz um prompt resolvido acompanhado de lock e evidence.

## 2. Escopo

O contrato cobre JSON e YAML equivalentes, schema, versionamento semântico, assinatura Ed25519, SHA-256, canonicalização, herança, composição, templates seguros, validação, backward compatibility, redaction, limites, resolução offline e auditoria. Não cobre conteúdo de produto que pertença a requisitos, escolha de modelo, parâmetros de inferência científicos ou autorização de ferramentas fora do TaskEnvelope.

## 3. Terminologia normativa

“DEVE” indica condição obrigatória; “NÃO DEVE” indica proibição; “PODE” indica extensão compatível; “bundle fonte” é o documento versionado; “bundle resolvido” é o resultado da composição; “fragmento” é uma unidade ordenável; “lock” é a resolução fechada de versões; “payload” é a projeção canônica assinada; “engine” é o resolver e validador; “executor” é o agente que recebe o prompt resolvido.

## 4. Representações JSON e YAML

JSON é a representação canônica para hashing. YAML é uma superfície autoral e deve ser carregado em um modelo JSON sem tags customizadas, aliases recursivos, chaves não textuais ou valores implícitos dependentes do parser. Datas permanecem strings RFC 3339; inteiros e números conservam tipo; chaves duplicadas são erro. Depois do parse, ambas as representações devem produzir a mesma árvore de dados e o mesmo payload hash.

## 5. Identidade

`bundle_id` é estável e não reutilizável. `bundle_version` segue SemVer. Identidade completa é o par imutável. Alterar conteúdo sem alterar versão é corrupção. O catálogo deve rejeitar duas cargas com o mesmo par e hashes distintos. Renomear um bundle cria nova identidade; aliases só podem existir no catálogo e nunca alteram o material assinado.

## 6. Schema e extensibilidade

A major do `schema_version` determina o leitor mínimo. `additionalProperties: false` é usado nos objetos normativos para impedir campos silenciosamente ignorados. Extensões futuras devem ser promovidas por nova minor quando opcionais. Um campo experimental somente pode existir em uma namespace explícita autorizada por uma futura versão do schema; prefixos improvisados são proibidos.

## 7. Fragmentos

Cada fragmento possui identidade, espécie, formato, conteúdo, variáveis, prioridade, origem e hash do conteúdo. As espécies são políticas de sistema, papel, contexto de domínio, tarefa, restrição, contrato de saída e exemplo. Um fragmento não pode misturar espécies para burlar precedência. O conteúdo deve ser autocontido e não pode referenciar arquivo não resolvido no lock.

## 8. Precedência

A engine agrupa e ordena fragmentos pela precedência normativa: `SYSTEM_POLICY`, `ROLE`, `DOMAIN_CONTEXT`, `TASK`, `CONSTRAINT`, `OUTPUT_CONTRACT`, `EXAMPLE`. Dentro da mesma espécie, usa `composition_order`; `priority` resolve somente fragmentos declarados no mesmo nível e não pode mover uma instrução inferior acima de política ou ADR. Conflitos sem estratégia explícita são erro.

## 9. Herança

Herança é limitada a dezesseis pais e deve formar DAG. Cada referência declara constraint de versão e merge strategy. A engine resolve versões apenas a partir do catálogo pinado ou do lock; descoberta pela rede durante a execução é proibida. Herança circular, diamond com hashes divergentes ou duas versões incompatíveis da mesma identidade bloqueiam a resolução.

## 10. Estratégias de merge

`APPEND` adiciona fragmentos após os herdados; `PREPEND` antes dos herdados dentro da mesma espécie; `REPLACE_BY_FRAGMENT_ID` substitui somente identidade exata; `ERROR_ON_CONFLICT` rejeita duplicação. Merge profundo implícito de objetos é proibido. Input e output contracts só podem ser substituídos integralmente por uma versão descendente compatível e claramente declarada.

## 11. Composição

`composition_order` lista cada fragmento efetivo exatamente uma vez. Fragmento ausente, repetido ou não listado é erro. Após resolver herança, a engine materializa uma sequência final e calcula um `resolved_prompt_sha256`. Esse hash pertence à evidence de execução, não ao bundle fonte, porque incorpora valores autorizados de variáveis.

## 12. Templates

Apenas `LITERAL` e `MUSTACHE_SAFE` são permitidos. Mustache seguro admite interpolação de variável declarada, seções booleanas e iteração sobre arrays limitados pelo input schema. Não admite funções, avaliação de expressão, acesso a atributo arbitrário, include dinâmico, leitura de ambiente, relógio, aleatoriedade, rede ou filesystem. As regras completas estão em `SPEC-004`.

## 13. Variáveis

Toda variável deve ser declarada com tipo, obrigatoriedade e sensibilidade. Valores extras são rejeitados. Default somente é aceito quando serializável no tipo. Variável sensível deve ser redigida de logs e evidence; ela não pode aparecer no prompt se a política do bundle não autorizar seu uso. Comprimentos e valores enumerados são validados antes do render.

## 14. Input contract

O input contract é JSON Schema autocontido e deve aceitar exatamente o contexto que será injetado. O TaskEnvelope é passado por referência e projeção allowlisted, não como dump irrestrito. O limite de bytes é aplicado após serialização UTF-8. Falhas produzem erro estruturado e nenhum prompt parcial é entregue ao executor.

## 15. Output contract

O bundle declara TEXT, JSON ou YAML. JSON/YAML devem validar contra schema. Texto deve respeitar tamanho e formato adicional quando definido. A engine pode permitir no máximo duas tentativas de reparo, explicitamente contabilizadas, sem alterar requisitos. Reparos não podem completar campo de domínio por inferência; apenas corrigem sintaxe ou estrutura usando o mesmo contexto.

## 16. Projeção canônica do payload

O payload hash usa a árvore completa do bundle com `signatures=[]`, `integrity.payload_sha256` preenchido com 64 zeros e `integrity.lock_digest_sha256` preenchido com 64 zeros. Essa projeção quebra auto-referência e torna o hash estável. A serialização segue o profile JCS do projeto: chaves ordenadas, UTF-8, strings NFC, números JSON finitos e ausência de whitespace não semântico.

## 17. Lock

O lock registra identidade, versão, payload hash raiz, dependências resolvidas, origem e lock digest. O digest é calculado com `lock_digest_sha256` zerado. O lock não executa resolution; ele é o resultado dela. Em modo fechado, qualquer dependência ausente ou hash divergente é erro. O lock deve ser armazenado junto da evidence da execução.

## 18. Hashes

SHA-256 é normativo. Hash de fragmento cobre bytes UTF-8 NFC do conteúdo. Payload hash cobre a projeção canônica. Lock digest cobre o lock canônico. O resolved prompt hash cobre a sequência final após render e separadores canônicos. Algoritmos adicionais podem existir apenas como aceleração e nunca substituem os valores SHA-256.

## 19. Assinatura

A assinatura usa Ed25519 sobre a mensagem binária `DSGEOREF-PROMPT-BUNDLE-V1`, NUL, bundle id, NUL, versão, NUL, payload hash ASCII, NUL e lock digest ASCII. A chave é identificada por `key_id` e resolvida em trust store local. O bundle deve ter pelo menos uma assinatura válida por chave não revogada. A assinatura de exemplo usa chave exclusivamente de teste.

## 20. Trust store e rotação

O trust store é versionado, distribuído pela supply chain do produto e não pode ser modificado pelo agente. Rotação aceita janela de assinatura dupla. Revogação impede novas execuções e marca evidence anterior, sem apagar histórico. Chave desconhecida, expirada ou revogada resulta em `SIGNATURE_UNTRUSTED`.

## 21. Versionamento do bundle

Patch corrige texto sem alterar significado ou instâncias válidas. Minor adiciona fragmento opcional ou variável opcional, mantendo output compatível. Major altera precedência, contrato obrigatório, tipo, canonicalização ou remove capacidade. A versão do conteúdo e a versão do schema são independentes e ambas são verificadas.

## 22. Backward compatibility

O engine declara majors de schema suportadas e janela de leitura. Ele pode ler major anterior para replay, mas writers produzem somente a major corrente. Migração é uma função explícita, determinística e testada por fixtures. Migração nunca reescreve a evidence original; produz novo bundle com lineage para o anterior.

## 23. Forward compatibility

Leitor antigo rejeita major nova. Não é permitido ignorar campos desconhecidos em objetos normativos. Um catálogo pode armazenar bytes desconhecidos sem executá-los, desde que preserve hash e marque `UNSUPPORTED`. Isso permite transporte sem interpretação.

## 24. Catálogo

O catálogo indexa bundle id, versões, schema, status, hash, assinaturas e compatibilidade. Publicação é imutável. Uma versão pode ser deprecada, não sobrescrita. O catálogo oferece resolução local e não concede autoridade para alterar o TaskEnvelope.

## 25. Pipeline de validação

A ordem obrigatória é: parse seguro; validação de schema; normalização Unicode; validação semântica; resolução de herança; detecção de ciclos; cálculo de hashes; validação do lock; verificação de assinatura; validação de compatibilidade; render de template; validação de output contract; geração de evidence. Falha em qualquer etapa interrompe as seguintes.

## 26. Validações semânticas

Além do schema, a engine confirma unicidade de fragmentos, cobertura exata de `composition_order`, existência de variáveis, ausência de secrets em fragmentos, compatibilidade de merge, limites de token/bytes, relação entre assinatura e integrity, e precedência. O schema sozinho não é suficiente para esses invariantes.

## 27. Erros

Erros têm código, etapa, bundle id/version, path JSON, mensagem segura e detalhe redigido. Códigos mínimos: `PARSE_FAILED`, `SCHEMA_INVALID`, `DUPLICATE_KEY`, `INHERITANCE_CYCLE`, `VERSION_UNRESOLVED`, `MERGE_CONFLICT`, `HASH_MISMATCH`, `LOCK_MISMATCH`, `SIGNATURE_INVALID`, `SIGNATURE_UNTRUSTED`, `INPUT_INVALID`, `TEMPLATE_INVALID`, `OUTPUT_INVALID`, `LIMIT_EXCEEDED` e `UNSUPPORTED_VERSION`.

## 28. Segurança contra prompt injection

Dados de usuário são tratados como dados, delimitados e validados; nunca são promovidos a fragmento de política. Conteúdo externo não pode introduzir instrução executável. Fragmentos de contexto incluem rótulo de origem e trust level. O executor não pode alterar a ordem ou remover delimitadores. Tentativa de instrução em campo de dados é preservada como conteúdo e submetida ao output contract.

## 29. Ferramentas

`tool_access` é allowlist. A disponibilidade real é interseção entre bundle, TaskEnvelope, papel e runtime. O bundle não pode conceder ferramenta proibida por nível superior. Cada chamada é auditável e associada ao resolved prompt hash.

## 30. Rede e egress

`DENY` é o padrão. `ALLOWLIST` exige domínios e finalidade. Redirecionamento, DNS rebinding e downloads implícitos são bloqueados pelo runtime. O bundle não contém credenciais. Ausência de rede não pode impedir execução de tarefas cuja baseline é offline.

## 31. Privacidade e redaction

`redaction_paths` usa JSON Pointer. A engine redige antes de log, hash de evidence textual ou observabilidade. O payload hash do bundle não inclui valores de execução. Evidence pode armazenar hash de input redigido e identificadores opacos, nunca secrets ou dados pessoais desnecessários.

## 32. Observabilidade

Métricas são de baixa cardinalidade: bundle id, major, status e etapa. Não incluem prompt, variável ou conteúdo. Traces registram hashes, duração, contagens e resultado. Logs estruturados seguem política de audit e redaction da `ADR-055`.

## 33. Determinismo

A resolução e o render são determinísticos. Nondeterminismo de modelo é separado e declarado no execution record. O mesmo bundle, lock, inputs redigidos e engine version devem produzir os mesmos bytes do prompt resolvido. Fixtures verificam essa propriedade.

## 34. Limites

O schema limita fragmentos e herança; profiles podem reduzir os limites. A engine impõe bytes e tokens antes da chamada. Truncamento silencioso é proibido. Se o contexto exceder o orçamento, a execução para com diagnóstico e proposta de decomposição, sem remover requisito.

## 35. Persistência

Bundle, lock, signature record e resolved execution record são artifacts imutáveis. Paths são relativos ao root gerenciado. Publicação segue staging, validação, fsync e rename atômico. A visão corrente aponta para versões, não muta conteúdo.

## 36. Execução offline

Todos os pais, schemas, chaves públicas e templates devem estar no pacote ou cache governado. A engine nunca baixa dependência durante uma execução. Import offline verifica hash, assinatura, licença e compatibilidade antes de disponibilizar a versão.

## 37. Testes de conformidade

A suíte inclui exemplos JSON/YAML equivalentes, hash conhecido, assinatura válida, assinatura alterada, lock alterado, ciclo, conflito de merge, variável ausente, output inválido, major desconhecida, key revogada e limites excedidos. Uma implementação só pode declarar conformidade se passar todos os vetores.

## 38. Publicação

Uma versão candidata é publicada somente após schema, validação semântica, vetores, assinatura, revisão de segurança e compatibilidade. Publicação gera receipt contendo hashes, key ids, engine mínima, timestamp e status. Receipt não substitui o bundle.

## 39. Handoff para Codex

Cada TaskEnvelope lista `SPEC-001`, referências aos bundles aplicáveis e status `PASS`. O agente deve parar se o bundle não resolver, se a assinatura falhar ou se uma instrução contradizer o TaskEnvelope. O handoff final inclui versão e hashes usados.

## 40. Governança de mudanças

Alteração de canonicalização, algoritmo, precedência, trust model, merge ou contract obrigatório exige ADR substituta e major. Novo tipo de fragmento exige revisão de segurança. Ajustes de conteúdo compatíveis seguem SemVer e revisão normal. Nenhum prompt pode ser corrigido “em produção” sem nova versão.

## 41. Exemplos e schemas

Os artefatos executáveis estão em `contracts/prompts/`. O exemplo mínimo possui payload, lock e assinatura Ed25519 verificáveis. O exemplo composto demonstra herança sem transformar o bundle pai em dependência implícita de rede.

## 42. Critérios de aceite

- JSON e YAML produzem árvore equivalente;
- schema e invariantes semânticas passam;
- hash e assinatura do vetor são reproduzíveis;
- ciclo e conflito são rejeitados;
- output inválido não é publicado;
- secrets não aparecem em logs;
- bundle não assinado ou incompatível não executa;
- TaskEnvelope registra specification baseline e evidence.

## 43. Condições de parada

A implementação deve parar diante de ambiguidade de precedência, algoritmo não especificado, formato sem schema, chave sem trust, dependência não pinada, template com avaliação arbitrária, output sem contrato ou tentativa de usar o Prompt Bundle para criar requisito novo.

# Anexo A — Perfil documental equivalente a aproximadamente vinte páginas

Este anexo detalha os comportamentos que uma implementação precisa executar sem completar lacunas por conveniência. A extensão do documento é deliberada: o Prompt Bundle atravessa governança, segurança, reprodutibilidade, templates, supply chain e observabilidade. Uma descrição curta deixaria decisões relevantes para cada implementador e produziria engines incompatíveis.

## A.1 Modelo conceitual completo

O modelo contém seis objetos persistentes e dois objetos transitórios. O `PromptBundleSource` é o documento autoral validado. O `PromptBundleLock` fecha todas as versões herdadas. O `PromptBundleSignatureRecord` prova autoria e integridade. O `ResolvedPromptBundle` registra a composição ordenada antes de receber valores. O `PromptExecutionRecord` registra a projeção usada em uma execução. O `PromptPublicationReceipt` comprova a promoção para o catálogo. Os objetos transitórios são o `RenderContext`, que existe somente durante validação e render, e o `ResolvedPromptBytes`, entregue ao executor.

Esses objetos não podem ser condensados em um único JSON mutável. O source é reutilizável, o lock depende de uma resolução, o execution record depende de valores e o receipt depende de publicação. Misturá-los criaria auto-referências, invalidaria hashes ou exigiria alterar um bundle publicado para anexar resultados posteriores. Cada objeto tem identidade, schema e retenção próprios, embora esta primeira versão materialize source, lock e signature como contratos principais.

O catálogo guarda o source e o lock por conteúdo. A assinatura é verificada na importação e novamente antes da execução. O resolved bundle pode ser reconstituído, mas seu hash deve ser armazenado como evidence para detectar divergência de engine. O execution record é obrigatório quando um agente produz commit, decisão, relatório ou artifact que possa ser promovido.

## A.2 Perfil JSON normativo

A serialização JSON usada para hash não é o texto original enviado ao parser. O parser rejeita chaves duplicadas e números não finitos antes de construir a árvore. Strings são normalizadas para Unicode NFC. Nomes de chave permanecem case-sensitive. Valores numéricos não podem depender da representação binária específica da linguagem; quando um campo exige precisão normativa, ele deve ser integer em unidade declarada ou string decimal com regex e escala definida.

A canonicalização ordena chaves lexicalmente pelos code points normalizados, usa UTF-8, não inclui BOM e elimina whitespace fora de strings. Barras não são escapadas sem necessidade. Caracteres de controle usam escapes JSON. A implementação não deve confiar no `json.dumps` padrão sem configurar ordenação, separadores e rejeição de NaN. Um conformance test compara bytes, não apenas objetos equivalentes.

Objetos com `additionalProperties: false` impedem que um producer novo envie campo que um consumer antigo silenciosamente ignore. Essa rigidez é intencional para políticas e segurança. Quando extensibilidade for necessária, ela deve surgir em um campo explicitamente versionado, como `properties`, cujo conteúdo não pode alterar invariantes do objeto pai. A engine não promove extension field a comportamento executável sem especificação correspondente.

## A.3 Perfil YAML autoral

YAML serve para edição humana e nunca é a base direta do hash. A implementação aceita apenas o subconjunto que mapeia sem ambiguidade para JSON: mappings com chaves string, sequences, strings, booleans, null e números JSON finitos. Tags, merge keys, anchors recursivos, objetos Python, timestamps implícitos, binary scalars e constructors customizados são rejeitados. Anchors não recursivos podem ser proibidos integralmente para manter provenance local de cada valor.

O loader deve detectar chaves duplicadas; usar um loader que retenha somente a última ocorrência é falha de conformidade. Scalars como `yes`, `on`, `01` ou datas não devem adquirir tipos por regras YAML históricas. Recomenda-se profile compatível com YAML 1.2 JSON schema. Depois do parse, o objeto passa pelo mesmo JSON Schema e pela mesma canonicalização do input JSON.

A exportação YAML é meramente conveniência. Ela não precisa preservar comentários, estilos ou ordem do documento autoral. O receipt registra o hash do payload canônico, e opcionalmente o hash dos bytes originais para auditoria de origem. Dois YAML visualmente diferentes que mapeiam à mesma árvore produzem o mesmo payload hash; duas árvores diferentes nunca podem compartilhar identity/version.

## A.4 Algoritmo de resolução de versão

A resolução recebe bundle id, constraint solicitada, catálogo local, política de status e lock opcional. Com lock, a engine não escolhe versão: verifica se a versão e o hash pinados existem. Sem lock, operação permitida apenas durante criação do lock, nunca durante uma execução promovível. A seleção considera versões `ACTIVE` ou `DEPRECATED` dentro da janela; `RETIRED` é excluída para novas resolutions.

Constraints usam um subconjunto SemVer documentado: igualdade, intervalos comparativos e caret para major maior que zero. Wildcards amplos e tag `latest` são proibidos em locks. A engine ordena versões semanticamente, filtra compatibilidade de schema e engine, e escolhe a maior versão compatível. A decisão, candidates examinados e motivo de exclusão entram no resolution record.

Se dois pais exigirem constraints sem interseção para o mesmo bundle id, a resolução falha com `VERSION_CONFLICT`. A engine não instala duas versões da mesma identidade na mesma composição, porque isso permitiria fragment IDs e policies contraditórios. Uma futura major poderia autorizar namespaces independentes, mas a versão 1 não oferece esse comportamento.

## A.5 Algoritmo de detecção de ciclos

O grafo de herança usa identidade completa como nó depois da resolution. A engine executa busca em profundidade com estados `UNSEEN`, `VISITING` e `VISITED`. Encontrar aresta para `VISITING` produz o caminho do ciclo no erro. A ordem de traversal é estável para diagnósticos reproduzíveis. Um limite de nós e profundidade é aplicado antes de alocar estruturas grandes.

Ciclos por aliases ainda são ciclos, porque alias não cria identidade nova. Um bundle que herda versão anterior de si mesmo também é ciclo na composição atual; evolução deve copiar ou referenciar fragmentos por nova estratégia futura, não formar cadeia autorreferente. O lock contém apenas DAG resolvido.

Diamonds são permitidos quando o mesmo ancestral resolve para a mesma identidade, versão e hash. Ele aparece uma vez no conjunto resolvido. Se os caminhos especificarem merge strategies incompatíveis para fragmento compartilhado, a composição falha. Esse controle evita duplicar policies no prompt e evita que a ordem dependa da rota percorrida.

## A.6 Algoritmo de merge de fragments

A engine inicia com a sequência efetiva dos pais na ordem declarada, depois aplica a estratégia de cada relação. `APPEND` insere fragments novos após os fragments herdados dentro da espécie, sem deslocar a espécie na precedência global. `PREPEND` faz o inverso. `REPLACE_BY_FRAGMENT_ID` exige que o alvo exista uma única vez e substitui sua definição por inteiro; merge de campos não é permitido. `ERROR_ON_CONFLICT` rejeita qualquer fragment id repetido.

Dois fragments distintos podem conter texto semelhante; a engine não usa similaridade para fundi-los. Redundância semântica é responsabilidade de review e lint, não de merge automático. O fragment hash detecta igualdade exata. Um linter pode alertar sobre n-grams ou sentences duplicadas, mas não deve alterar o prompt.

Após merge, a engine verifica que cada fragment efetivo aparece exatamente uma vez em `composition_order`. Quando um child substitui fragment, o mesmo ID preserva sua posição, salvo order explicitamente alterada em versão compatível. Fragment novo deve ser inserido em order. Fragment removido em major deve ser removido de order. Qualquer divergência é erro antes do render.

## A.7 Precedência e conflito normativo

Precedência não é simplesmente a ordem textual. Uma policy de sistema não pode ser neutralizada por exemplo posterior. A engine preserva boundaries e metadados de espécie ao montar a mensagem. Quando o provider de modelo aceita múltiplos roles, policies e role fragments ocupam channels apropriados. Quando aceita somente texto, separadores canônicos e labels explícitos preservam a hierarquia.

Um conflito normativo ocorre quando fragment inferior ordena ação proibida por superior ou redefine autoridade. A detecção completa exige análise semântica e não pode ser garantida por parser; por isso, bundles passam por review humano e regras estáticas. A engine detecta conflitos estruturais, como tool solicitada fora da allowlist, network access contraditório, output mode divergente e variable sensível interpolada sem autorização.

Durante execução, o agente também possui condição de parada. Se conteúdo da história contradizer a policy ou specification, o executor não “escolhe a mais recente”; ele reporta IDs e trechos, sem executar a parte ambígua. O Prompt Bundle registra a precedência, mas não transforma um modelo em árbitro final de governança.

## A.8 Delimitadores e montagem de bytes

Cada fragment renderizado é cercado por header e footer canônicos que incluem fragment id, kind e content hash. Delimitadores não são configuráveis pelo usuário. Isso reduz prompt injection por texto que tente simular o fim de uma seção. Se o conteúdo contiver o delimitador literal, a engine o escapa ou escolhe encoding length-prefixed definido pelo adapter.

A montagem não usa newline do sistema operacional; usa `\n`. A ordem e os separadores entram no resolved prompt hash. Adapters que transformem o prompt para API específica devem produzir um `ProviderMessageProjection` versionado e calcular hash adicional. O execution record contém ambos, permitindo provar se divergência surgiu na resolução ou na adaptação.

Conteúdo vazio é inválido. Whitespace de fragmento é preservado conforme fonte depois de normalização de line ending. A engine não aplica trim global que altere exemplos ou markdown. Normalizações permitidas são listadas e testadas.

## A.9 Contrato de input e projeções

O input contract deve preferir uma projeção pequena de objetos normativos. Em vez de inserir um TaskEnvelope inteiro, o caller monta objeto com story id, outcome, acceptance criteria, allow paths e references estritamente necessárias. Cada projection possui schema e pode ser versionada. Isso reduz exposição e tokens.

O caller não pode omitir criterion para caber no orçamento. Se o input exceder limite, a história precisa ser decomposta ou uma specification deve definir resumidor determinístico e verificável. Resumo livre por outro modelo não pode substituir requisito original sem lineage e review.

Valores sensíveis são identificados pelo schema e pela policy do contexto. A engine mantém duas views: render view e audit view redigida. O hash de input pode ser calculado sobre uma canonical view com HMAC quando igualdade precisa ser detectada sem expor valor. A chave e o algoritmo pertencem à segurança da instância, não ao bundle.

## A.10 Contrato de output e reparo

Quando output é JSON, o adapter deve solicitar modo estruturado se disponível, mas ainda valida o resultado. A engine não confia em promessa do provider. Um output inválido pode passar por reparo sintático limitado: remover fence, localizar objeto único ou solicitar reemissão com diagnostics de schema. O reparo não inventa valor nem consulta fonte nova.

Cada tentativa registra raw output hash, diagnostics e reason. O limite máximo é dois e pode ser reduzido para zero. Depois do limite, status é `OUTPUT_INVALID`. Um output parcial nunca é entregue como sucesso. Texto livre pode ter checks de headings, regex allowlisted e maximum bytes.

O output contract também define campos que precisam ser citados ou acompanhados de evidence. Por exemplo, lista de arquivos alterados deve corresponder ao diff real em gate posterior. Schema garante forma; conformance workflow garante verdade factual.

## A.11 Canonicalização e vetores

A suíte deve conter vetores com ordem diferente de chaves, Unicode composto/decomposto, escapes, números inteiros e YAML equivalente. Todos os equivalentes produzem um hash conhecido. Vetores inválidos cobrem NaN, Infinity, duplicate key, surrogate inválido e tag YAML.

O algoritmo de payload zerando os dois digests e removendo signatures deve ser implementado em função pequena e testável. A função recebe objeto já validado e retorna nova árvore, sem mutar original. Lock digest zera somente seu próprio campo. A assinatura aponta para ambos os digests e sua cópia nos signature records deve corresponder exatamente.

Se o bundle carregado contém payload hash divergente, a engine não tenta “corrigir” o documento. Ela retorna mismatch e preserva os bytes como quarantine evidence. Um comando separado de authoring pode recalcular antes de assinar, mas nunca em execução.

## A.12 Gestão de chaves

Chaves privadas não ficam no repositório, bundle, container de runtime ou evidence. Signing ocorre em serviço ou ferramenta controlada. O repository pode conter public keys de teste claramente rotuladas. O trust store operacional é instalado por supply chain e protegido por permissão.

Cada key record inclui id, algorithm, public key, validity, status, owner e allowed scopes. Uma chave pode assinar bundles de determinados roles ou namespaces. Verificar assinatura criptográfica sem verificar scope é insuficiente. Revocation list é versionada e disponível offline.

Durante rotação, uma versão pode ter assinaturas por chave antiga e nova. O verifier aceita pelo menos uma trusted não revogada, conforme policy. Depois do fim da janela, assinatura antiga permanece historicamente verificável, mas novas executions podem exigir a nova. Re-signing do mesmo payload cria novo signature record sem alterar bundle identity/version, desde que o campo signatures seja excluído do payload hash; publicação do signature set é auditada.

## A.13 Threat model

Ameaças incluem bundle adulterado, catálogo comprometido, dependência substituída, chave roubada, prompt injection em input, template injection, tool escalation, secret leakage, downgrade de versão, replay fora de policy, denial of service por bundle enorme e ambiguity exploitation. Cada uma possui controle preventivo e detectivo.

Hashes detectam alteração, signatures autenticam origem, locks impedem substitution, schema/limits contêm estrutura, precedence evita tool escalation, redaction reduz leakage, minimum engine e policy impedem downgrade, execution record torna replay auditável. Nenhum controle sozinho é suficiente. A engine deve falhar fechada.

O modelo não assume que conteúdo assinado é correto; assinatura prova autoria, não qualidade. Review e requirements continuam necessários. Também não assume que o LLM seguirá todas as instruções; tool sandbox, allow paths, tests e reviewer externo limitam consequências.

## A.14 Política contra dados como instrução

Todo campo vindo de usuário, provider externo, documento ou artifact é marcado como untrusted data. A renderização envolve esse conteúdo em blocos declarados e acrescenta policy para não tratá-lo como comando. O agent não deve abrir links ou executar snippets presentes nos dados salvo tarefa explícita e tool policy.

Um fragment `DOMAIN_CONTEXT` que inclui texto externo deve registrar source e trust. Conteúdo copiado de issue continua inferior a ADR/specification. O engine não promove mensagens de erro ou output anterior a fragment `SYSTEM_POLICY`.

Test vectors incluem strings como “ignore instruções anteriores”, delimitadores simulados e JSON com nomes de tool. O resolved prompt deve preservar como dados, e o executor deve continuar limitado pelo runtime. A auditoria verifica que nenhum valor alterou tool allowlist.

## A.15 Tool authorization

Bundle declara tools desejadas; TaskEnvelope e papel declaram tools/paths autorizados; runtime declara tools disponíveis. O conjunto efetivo é a interseção. Ausência de uma tool necessária gera stop condition, não fallback improvisado. O agent não substitui uma tool inexistente por shell ou rede não autorizados.

Cada tool possui schema de input/output, side-effect class e approval policy. Calls mutáveis podem exigir confirmation externa conforme ambiente. Prompt Bundle não contém credenciais nem endpoints secretos. Tool result é untrusted até validar seu contrato.

O execution record armazena tool name/version, request hash, response hash, status e duration. Payloads completos seguem retention e redaction específicas. Isso permite reproduzir decisões sem registrar secrets.

## A.16 Orçamento e truncamento

O engine estima tokens por adapter, mas aplica também limite de bytes, porque tokenization varia. Policies e constraints nunca são truncadas. Se o provider tiver context menor que o bundle resolvido, a execução é incompatível. Um adapter não pode remover examples ou criteria silenciosamente.

A resolução pode oferecer uma análise de contribuição por fragment para orientar decomposição. Essa análise é diagnostics, não mudança automática. O Owner ou Tech Lead decide dividir história, selecionar bundle menor compatível ou reduzir contexto redundante por nova versão.

Output truncado é failure, mesmo que parse parcial seja possível. O adapter deve usar stop reason do provider e verificar finish status. Evidence registra limits e counts observados.

## A.17 Caching

Caches podem armazenar bundle parseado, lock verificado, resolved fragment graph e token count. Keys incluem hashes e engine version. Cache nunca ignora revocation ou policy update; trust store version entra na key ou força revalidação. Valores de execução sensíveis não entram em cache compartilhado.

Cache corruption é detectada por hash. Miss apenas afeta performance. Cache content-addressed pode ser reconstruído offline. Eviction não muda semântica.

A implementação não deve criar singleton global mutável com catálogo e prompts. Use ports e adapters injetados, permitindo testes isolados e evitando acoplamento circular. Cada bounded context consome o serviço de resolução por interface publicada.

## A.18 Persistência e transações

Publicar source, lock, signature set e catalog index exige transação coordenada. Bytes são publicados atomicamente no filesystem; metadata e outbox no PostgreSQL apontam para hashes. Em falha entre etapas, reconciliation completa ou compensa sem expor versão incompleta como ACTIVE.

O execution record é criado antes da chamada de modelo com status `STARTED`, hashes e policy. Ao terminar, recebe output hashes, tools e status, sem mutar partes imutáveis. Uma versão/revision otimista impede duas finalizações divergentes. Attempts podem existir para retries, cada uma ligada à mesma execution intention.

Backups preservam catálogo, trust store público, bundles, locks, records e artifacts. Restore drill verifica signature e hashes. Retention de bundles usados por evidence é reference-aware.

## A.19 Status de catálogo

`CANDIDATE` pode ser validado em ambiente de review; `ACTIVE` pode ser selecionado para novas resolutions; `DEPRECATED` continua disponível durante janela, com warning; `RETIRED` somente replay autorizado; `QUARANTINED` indica falha de integridade ou confiança. Status não muda bytes nem hash.

Promoção candidate→active exige receipt. Deprecation declara successor e data. Retirement não quebra records históricos. Quarantine suspende executions imediatamente e gera evento de segurança. Remover fisicamente só ocorre quando nenhuma evidence ou retention depende do bundle.

O status é metadata transacional e auditada. Um agent não pode promovê-lo. Pull request pode propor source, mas signing/promotion seguem gate independente.

## A.20 Compatibility matrix

A matriz cruza schema major, engine version, template engine version, TaskEnvelope version, provider adapter e role bundle version. Uma célula indica READ, EXECUTE, WRITE ou UNSUPPORTED. READ permite auditoria; EXECUTE permite replay; WRITE permite criar nova evidence. Writers nunca produzem versão fora da célula WRITE aprovada.

Antes de upgrade, CI executa corpus de bundles ativos e locks. Comparação verifica payload hash, resolved prompt hash e provider projection hash. Divergência esperada requer migration record; divergência não explicada bloqueia promoção.

Rollback mantém engine anterior e catalog snapshot. Bundles não são down-converted automaticamente. A decisão de upgrade é separada de mudança de conteúdo, evitando atribuir regressão à causa errada.

## A.21 Engine API interna

Uma interface recomendada separa `parse`, `validate_source`, `resolve`, `verify`, `render`, `project_provider` e `record_execution`. Cada função recebe tipos imutáveis e retorna result tipado. Não se exige esses nomes públicos, mas responsabilidades não devem se fundir em arquivo gigante ou função com múltiplos side effects.

Ports incluem BundleRepository, LockRepository, TrustStore, TemplateRenderer, ProviderAdapter, ExecutionRecordRepository e Clock somente onde timestamp é input explícito. Domain services não importam framework HTTP, ORM ou provider SDK. Adapters convertem contratos externos.

Erros são value objects com code e safe context. Exceções de biblioteca são mapeadas na boundary. Isso evita que cada caller interprete strings ou implemente verificação parcial.

## A.22 Estrutura de módulos sugerida

Dentro do bounded context de governança: `domain/prompt_bundle`, `application/resolve_bundle`, `application/publish_bundle`, `adapters/catalog`, `adapters/signatures`, `contracts`. Arquivos refletem conceito, não sprint ou issue. `resolver.py` não deve concentrar parser, SemVer, DAG, hashing, signing e persistence; cada responsabilidade tem módulo pequeno e tests.

Schemas vivem em contracts; dataclasses/Pydantic adapters são gerados ou mapeados, sem se tornarem domain model. O domain usa tipos que preservem invariantes. Provider adapters vivem fora do core.

Fitness functions verificam imports, line counts, duplicate functions e nomes genéricos. Uma mudança que exige cruzar contexts usa published contract, não import direto.

## A.23 SemVer detalhado

Correção ortográfica que não muda instruction pode ser patch. Alterar “pode” para “deve”, mudar priority, tool access, output schema, variable default com efeito ou merge strategy é semantic change e normalmente major ou minor conforme compatibilidade. Adicionar exemplo não executável pode ser patch; adicionar fragment EXAMPLE que entra no prompt é minor se não quebra output, mas exige regression corpus.

Adicionar variável opcional com default deterministic é minor. Torná-la obrigatória é major. Aumentar limites é minor; reduzir abaixo de bundles válidos é major. Adicionar trusted key não muda bundle version, mas muda trust store version e é auditado.

O reviewer deve avaliar comportamento, não apenas schema diff. Um tool gera structural diff e uma checklist humana cobre semântica.

## A.24 Migrações

Migration é função total para instâncias válidas da versão de origem ou retorna diagnóstico explícito quando informação necessária não existe. Ela não usa LLM para preencher campo normativo. O resultado valida no target e contém lineage com source hash, migration id/version e timestamp.

Migrations são composáveis major a major, não salto arbitrário não testado. Corpus inclui edge cases. Original permanece armazenado. Execution replay pode escolher source engine ou migrated view conforme purpose, e registra a escolha.

Para Prompt Bundle v1, não há migration anterior. O contract define desde já como futuras majors devem se comportar.

## A.25 Supply chain

Bundles oficiais entram no pacote de release ou em bundle de conteúdo assinado. SBOM lista engine, crypto e parser dependencies; Prompt Bundle contents podem ter inventory separado. Build reproduzível verifica schemas e golden vectors. Nenhum download pós-instalação é necessário para bundles baseline.

Um import externo exige provenance, licença, hash, signature e review. Conteúdo de terceiro não ganha status SYSTEM_POLICY automaticamente. O namespace identifica owner. Re-export preserva attribution quando aplicável.

Vulnerability em parser ou crypto pode exigir bloquear engine version mesmo com bundles válidos. Compatibility matrix e update gate tratam esse caso.

## A.26 Auditoria e privacy by design

O audit event registra quem publicou, aprovou, deprecou, executou e revogou, com IDs/hashes. Não registra conteúdo integral por default. Acesso ao conteúdo segue autorização e purpose. Export de audit permite verificar cadeia sem revelar inputs sensíveis.

Resolved prompts podem conter informação de projeto. Retention e encryption at rest seguem classificação. Um hash simples de dado de baixa entropia pode vazar igualdade; por isso input hashes sensíveis podem usar HMAC. Bundle source em si não deve conter secrets.

Support bundle sanitizado inclui versions, codes e hashes, não prompt ou variables, salvo opt-in explícito e redaction review.

## A.27 Observabilidade operacional

Dashboards mostram taxa de resolution failure, signature failure, unsupported version, output invalid, token budget exceeded e duration percentiles por bundle major. Cardinalidade de bundle id é limitada pelo catálogo; version patch pode ser attribute de trace, não label em toda métrica.

Alerts são por sintomas: aumento de signature failure, incompatibilidade após upgrade, output invalid acima de baseline ou tool denial recorrente. Não alertam por conteúdo. SLOs distinguem resolução local e chamada de modelo.

O execution ledger permite replay offline dos passos determinísticos até provider call. Divergência de resolved prompt hash é incidente de reproducibility.

## A.28 Conformance levels

`PARSER_CONFORMANT` valida JSON/YAML/schema. `RESOLVER_CONFORMANT` adiciona SemVer, DAG e merge. `INTEGRITY_CONFORMANT` adiciona hash, lock e signature. `EXECUTION_CONFORMANT` adiciona templates, provider projection, tools e records. O DSGeorref exige todos para runtime oficial.

Bibliotecas auxiliares podem implementar subset, mas não se anunciam como engine completa. O conformance report lista vectors e versions. Uma falha em nível inferior invalida superiores.

A suite é independente da implementação e deve poder testar adapters alternativos. Golden vectors ficam imutáveis; correção de vector inválido requer versionar a suite e justificar.

## A.29 Negative test catalog

Casos obrigatórios incluem duplicate key; unknown field; unsupported schema; malformed SemVer; inheritance depth excessiva; cycle simples e diamond conflict; fragment duplicado; composition order ausente; variable extra; sensitive interpolation proibida; unsafe Mustache; payload mismatch; lock mismatch; wrong key; revoked key; altered signature; tool escalation; network domain ausente; oversized input; output schema fail; provider truncation e record finalization concorrente.

Cada caso espera code e stage, não apenas “erro”. Mensagem pode evoluir. O runner garante que nenhuma falha gere artifact publicado ou status success. Fuzzing cobre parser e template.

A suíte de segurança inclui adversarial inputs e delimitadores. Ela não depende de comportamento probabilístico do modelo para validar sandbox; verifica a interseção de policies e tool enforcement diretamente.

## A.30 Positive test catalog

Golden path mínimo sem herança; bundle composto; YAML/JSON equivalentes; duas signatures em rotação; deprecated parent permitido; output JSON válido; tool read-only; offline resolution; replay com engine pinada; migration fixture futura. Cada caso fixa hashes.

Performance test mede 1, 10, 100 e 128 fragments dentro dos limites, com cache frio/quente. Resultado não altera semantics. Memory usage é bounded.

Cross-language test, quando houver segunda implementação, compara canonical bytes e hashes. Diferença é bug, não tolerância.

## A.31 Review checklist

Reviewer confirma owner, purpose, referências normativas, fragment kinds, precedência, variables, sensitive paths, tools, network, limits, output schema, inheritance, merge, SemVer, hashes, signatures, tests, compatibility e rollback. Security revisa trust, injection e egress. Domain owner revisa linguagem e ausência de requirement novo.

Aprovação do conteúdo e assinatura podem ser segregadas. O signer verifica receipt do review. Automação não substitui accountability.

Um PR que altera bundle e implementação simultaneamente deve evidenciar por que não há circularidade de aprovação. Preferencialmente, contract muda e congela antes do consumer.

## A.32 Publication ceremony

A ferramenta de authoring valida source, resolve lock em catálogo aprovado, calcula payload/lock, executa tests, gera candidate receipt e solicita signature. Depois de assinatura, o publisher verifica novamente a partir dos bytes, grava artifacts atomicamente e atualiza catálogo via transaction/outbox. O status só se torna ACTIVE depois do post-publication readback.

Se o catálogo update falhar após artifact rename, reconciliation detecta artifact não indexado e completa ou quarantine. Se metadata aponta para artifact ausente, status não pode ser ACTIVE. Receipt contém manifest hash e operator identity.

Publicação não ocorre por merge simples de arquivo no repositório operacional. O repositório é fonte de build; a instância usa pacote verificado.

## A.33 Runtime execution ceremony

O caller seleciona bundle id/version pinado pelo TaskEnvelope, carrega lock, verifica status/trust/compatibility, valida input projection, resolve bytes, calcula hash, cria execution record e invoca provider adapter. Tool sandbox recebe effective policy. Output é validado e record finalizado. Handoff inclui evidence.

Cada etapa tem timeout e error mapping. A chamada de provider é a única parte potencialmente nondeterminística; resolução e validation são deterministic. Retries preservam bundle/input e recebem attempt id novo. Não alteram prompt para “tentar melhorar” salvo repair policy explicitamente definida.

Em cancelamento, record é finalizado como CANCELLED com reason e sem output success. Artifacts de diagnóstico seguem retention.

## A.34 Replay

Replay pode ser `VERIFY_ONLY`, que recalcula determinísticos e compara hashes; `PROVIDER_REPLAY`, que chama modelo novamente sob policy; ou `FULL_REPRODUCTION`, que inclui tools em sandbox. O mode é explícito. Provider replay não promete output igual em bounded nondeterminism.

O sistema verifica disponibilidade de engine, adapter, model e tools. Ausência produz incompatibility report. Ele não substitui automaticamente versão nova. Records originais permanecem.

Replay é usado para auditoria, regression e incidentes, não para sobrescrever resultado anterior. Novo output é nova Attempt/evidence.

## A.35 Multi-provider adaptation

Cada provider adapter mapeia fragment kinds para roles/messages suportados. Se o provider não consegue preservar precedence ou output mode, adapter declara incompatível em `supports`, não achata silenciosamente. Token counting e stop reasons são provider-specific, mas policy limits permanecem.

Provider projection é versionada e testada com golden messages. Fields exclusivos não podem alterar requirement. Logs redigem conteúdo. Request id do provider entra em evidence protegida.

Trocar provider pode ser reversível em profile se contracts preservados; mudar trust, data egress ou output semantics pode exigir ADR. Prompt Bundle continua independente do SDK.

## A.36 Uso por agentes Codex

O registry de agentes aponta para bundle de role. Cada TASK referencia specs e arquivos. O runner compõe role bundle, task fragment derivado de projection e output template. Ele não copia repositório inteiro para o prompt. References são carregadas conforme allowlist e registradas por hash.

O agente deve produzir mudanças dentro de allow paths. Prompt não substitui enforcement de filesystem. Reviewer usa execution record para saber quais instruções foram fornecidas. Se a tarefa foi executada sem bundle conforme, o commit não satisfaz Definition of Done.

Prompts permanentes deixam de ser arquivos soltos sem identidade; tornam-se sources de bundles ou fragments com lineage. O texto original pode permanecer para leitura, mas runtime usa a versão empacotada.

## A.37 Integração com Template Contract

Fragments MUSTACHE_SAFE seguem `SPEC-004`. A engine pode delegar render a TemplateRenderer, passando somente variables declaradas. Template id/version/hashes entram no payload ou lock. Uma mudança no renderer que altera bytes exige compatibility review.

Output templates também podem formatar handoff, mas nunca transformar output inválido em válido. Structured outputs preferem serializer, não template textual. Partials são resolvidas antes do bundle hash quando embutidas ou pinadas no lock quando externas.

Template error é reportado na etapa correta e não como model failure.

## A.38 Integração com Artifact Contract

Bundle source, lock, signature record, execution record e receipts podem ser artifact kinds em extensão futura do registry. Nesta baseline, são arquivos contratuais e evidence; quando publicados operacionalmente, devem usar descriptors, hashes e manifests de `SPEC-005`.

Artifacts resultantes da execução registram prompt bundle id/version, payload hash, lock digest e resolved prompt hash em provenance quando permitido. Isso possibilita reconstruir contexto sem embutir prompt sensível.

A política de retenção considera referência por ResultSnapshot, audit e release evidence. GC não remove material necessário a reprodução.

## A.39 Integração com Edit Case

Agentes de revisão podem usar bundle específico para priorização ou explicação, mas decisões humanas e state machine pertencem a `SPEC-002`. Prompt não muda status diretamente sem command autorizado. Rationale sugerida por IA é marcada como suggestion e o reviewer assume decisão.

O execution record pode ser artifact associado ao case, respeitando privacy. Um bundle para aplicação nunca substitui revalidação SGV. Alucinação de GCP é contida pelos schemas e gates.

## A.40 Integração com AIBackend

Prompt Bundle pode configurar backends de linguagem, mas o protocolo `SPEC-003` governa supports/estimate/execute/validate/publish. Bundle não altera method order, budgets ou candidate-only publication. Backend manifest declara se usa prompts e quais schema majors suporta.

ModelPack pode incluir bundle default assinado, mas import verifica ambos e registra vínculo. Atualizar prompt sem ModelPack é permitido somente quando compatibility matrix autorizar. Regressions passam pelo corpus científico quando o prompt influencia resultado.

## A.41 Riscos residuais

Mesmo com contratos, um modelo pode desobedecer instruction, produzir conteúdo falso ou explorar ambiguidade não detectada. Controles residuais são sandbox, tests, independent validation, limited write scope e review. Assinatura não garante ausência de prompt injection em dados; delimiters e policy reduzem, não eliminam. Token estimators podem divergir; byte and provider limits tratam.

O report de risco deve evitar claim de “prompt seguro” absoluto. O objetivo é governabilidade, rastreabilidade e contenção. Incidentes alimentam nova versão e tests.

## A.42 Definition of Done do engine

A implementação está pronta quando todos os conformance levels passam, golden vectors são reproduzidos, negative cases falham com codes corretos, trust rotation e revocation funcionam, cache não altera resultado, offline resolution funciona, execution records são completos, tools são enforcement real, privacy review passa, restore/replay foi testado e arquivos permanecem dentro dos limites arquiteturais.

Nenhuma função única deve realizar parse, resolution, signature, render e provider call. Nenhum módulo de produção deve exceder hard limits sem exception aprovada. APIs públicas têm contracts e erros tipados. A documentação aponta para code owners e tests.

## A.43 Matriz de responsabilidades

Product Owner aprova propósito e comportamento de produto; Arquiteto aprova contract e compatibility; Security aprova trust, injection, egress e redaction; Tech Lead decompõe implementação; Backend implementa engine/ports; IA implementa provider adapters quando aplicável; QA mantém conformance corpus; DevOps integra signing/build; Reviewer audita evidence. Uma mesma automação pode executar passos, mas accountability permanece segregada.

## A.44 Handoff final da especificação

Os schemas e exemplos presentes em `contracts/prompts/` são a referência executável da major 1. Divergência entre este anexo e schema deve ser tratada como finding, não resolvida por preferência. A implementação começa pelos tipos e funções puras, depois repositories/trust, depois application workflows, adapters e integration tests. A ordem evita construir UI ou SDK antes de fixar semantics.

A Fase E congela esse contrato. Mudanças futuras seguem SemVer e gates descritos; nenhuma issue pode reduzir essas garantias por conveniência local.
