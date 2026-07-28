# SPEC-004 — Template Contract

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-001`
- **ADRs governantes:** `ADR-006`, `ADR-008`, `ADR-010`
- **Bounded Contexts:** `BC-001`, transversal
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Propósito

O Template Contract define templates usados por agentes, relatórios, issues, handoffs, manifests auxiliares e mensagens operacionais. Ele impede que cada implementação invente sintaxe, variável, escaping e validação. Template é artifact versionado e determinístico, não uma função Python arbitrária.

## 2. Classes

`TEXT` e `MARKDOWN` produzem texto; `JSON` e `YAML` produzem estrutura. `LITERAL` não interpola; `MUSTACHE_SAFE` usa subconjunto; `STRUCTURED` monta árvore a partir de schema e bindings explícitos. A classe faz parte da identidade e não pode mudar em patch.

## 3. Identidade

`template_id` é estável e `template_version` SemVer. O par é imutável. Catálogo rejeita hash divergente. Depreciação não remove versão necessária a replay.

## 4. Fonte

Fonte é string para LITERAL/MUSTACHE ou árvore para STRUCTURED. Encoding é UTF-8 e normalização NFC. Chaves duplicadas em YAML/JSON são erro. Linha final é governada pelo template, não adicionada implicitamente.

## 5. Mustache seguro

Permite `{{name}}`, seções booleanas e iteração em arrays declarados. `{{.}}` é permitido apenas dentro de array escalar. Proíbe lambdas, helpers, expressão, acesso a objeto por reflexão, include por valor de usuário, delimitador customizado, execução de código, leitura de arquivo, ambiente, rede, relógio e aleatoriedade.

## 6. Escaping

Markdown/texto usa escaping definido por contexto quando variável é marcada untrusted. JSON/YAML não são produzidos por concatenação textual; usam serializer estruturado. HTML não é classe permitida nesta versão. Raw interpolation exige variável declarada `trusted_literal` em futura versão e revisão de segurança; não existe na v1.

## 7. Variáveis

Cada variável tem nome, tipo, obrigatoriedade, default, sensibilidade e limites. Variável não declarada é erro. Ausência de obrigatória é erro. Coerção automática string→número ou string→boolean é proibida. Array e objeto são validados por schema específico quando usados.

## 8. Partials

Partials são referenciadas por identidade e constraint, resolvidas no catálogo e pinadas em lock. Include dinâmico é proibido. Grafo deve ser acíclico. Conflito de variável entre template e partial é erro salvo definição idêntica.

## 9. Herança e composição

Template não herda conteúdo implicitamente. Composição ocorre por partials ou por Prompt Bundle. Uma partial não pode modificar contrato de saída do pai. A ordem é declarada pela fonte.

## 10. Render request

O request inclui render id, template id/version, variables, locale e idempotency key. Locale não muda semântica normativa nem nomes de campos; apenas recursos textuais explicitamente catalogados. Valores de ambiente não entram automaticamente.

## 11. Render pipeline

Resolver versão; verificar hash; validar request; validar variáveis; resolver partials; detectar ciclos; render em memória limitada; validar tamanho; parsear output estruturado; validar schema/seções; calcular output hash; produzir RenderResult. Nenhuma saída parcial é publicada após erro.

## 12. Structured template

JSON/YAML estruturado usa bindings em folhas e serializer canônico. Isso evita vírgulas, escaping e tipos incorretos. Bindings ausentes seguem regras da variável. Campos adicionais dependem do output schema.

## 13. Output validation

Todo template declara maximum bytes. Estruturados declaram JSON Schema. Markdown pode declarar headings obrigatórios. Validação acontece antes da publicação. Resultado inválido é FAIL, não texto “melhor esforço”.

## 14. Determinismo

Mesmo template, versão, variables e engine produzem mesmos bytes. Locale e line ending entram no input explícito. Timestamps, UUIDs e random devem ser variáveis fornecidas pelo chamador e persistidas na evidence.

## 15. Segurança

Templates não concedem tools, não executam código e não interpretam conteúdo renderizado como instrução. Valores sensíveis são redigidos de logs. Output path é definido pelo chamador autorizado, não pelo template.

## 16. Versionamento

Patch corrige texto sem alterar variáveis ou estrutura exigida. Minor adiciona variável opcional ou seção opcional. Major remove/renomeia variável, muda tipo, engine, escaping ou output schema incompatível. Alterar hash exige nova versão.

## 17. Backward compatibility

Engine lê versões anteriores durante janela. Migração gera nova versão e golden diff. Consumers devem piná-la. “Latest” não é permitido em execução reprodutível.

## 18. Erros

Códigos: `TEMPLATE_NOT_FOUND`, `VERSION_UNSUPPORTED`, `HASH_MISMATCH`, `VARIABLE_MISSING`, `VARIABLE_UNKNOWN`, `VARIABLE_TYPE_INVALID`, `PARTIAL_CYCLE`, `PARTIAL_CONFLICT`, `RENDER_LIMIT_EXCEEDED`, `OUTPUT_PARSE_FAILED`, `OUTPUT_SCHEMA_INVALID` e `UNSAFE_SYNTAX`.

## 19. Testes

Golden tests comparam bytes e hash. Casos negativos cobrem variável ausente/extra, type mismatch, loop excessivo, partial cycle, unsafe syntax, output inválido e limite. Property tests asseguram determinismo.

## 20. Relação com Prompt Bundle

Prompt Bundle usa templates, mas controla precedência, assinatura e runtime policy. Template Contract não substitui essas responsabilidades. O hash da fonte entra no payload do bundle quando embutido ou no lock quando referenciado.

## 21. Relação com artifacts

Output publicado segue `SPEC-005`, com media type, hash e provenance. RenderResult sozinho não é ArtifactSet. Reports podem embutir template id/version no manifest.

## 22. Critérios de aceite

- schema e exemplos válidos;
- sintaxe segura;
- variáveis completas e tipadas;
- output validado;
- golden hash estável;
- partial DAG sem ciclos;
- nenhuma dependência implícita de ambiente;
- TaskEnvelope referencia a especificação.

## 23. Condições de parada

A implementação para se houver necessidade de helper arbitrário, raw HTML, include dinâmico, coercion não definida, output sem schema, variável implícita ou dependência de horário/rede não fornecida explicitamente.
