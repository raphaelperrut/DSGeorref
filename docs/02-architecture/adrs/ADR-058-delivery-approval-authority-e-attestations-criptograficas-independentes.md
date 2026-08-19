# ADR-058 — Delivery Approval Authority e attestations criptográficas independentes

- **Status:** `Accepted`
- **Baseline:** `Owner Decision — APPROVE_OPTION_B — 2026-08-17`
- **Aprovador:** `Project Owner`
- **Owner normativo:** `ADR-058`
- **Boundary independente:** `SIM`
- **Decisões em aberto:** `Nenhuma`
- **Bounded Contexts:** `BC-001` — Governança de Engenharia e Entrega

## Contexto

O fluxo de entrega exige que Executor, QA e Reviewer atuem de forma independente sobre o mesmo commit candidato. A baseline anterior declarava os papéis, o TaskEnvelope e o candidate SHA, mas não possuía autoridade machine-verifiable que vinculasse principal autenticado, papel autorizado, atuação, aprovação e SHA.

Role ou label declarada, IDs de tarefas distintos, CODEOWNERS, contagem de approvals do GitHub, autoria Git não verificada e assinatura de Prompt Bundle não provam esse vínculo. A ausência do contrato é fail-closed e mantém consumidores, incluindo `ISSUE-0799`, bloqueados.

## Decisão

- `BC-001` possui a `Delivery Approval Authority`, separada das autoridades de identidade e autorização do produto.
- Identidade autenticada usa principal estável no formato lógico `issuer + subject`. Workloads também declaram o accountable subject em nome do qual atuam.
- Uma política assinada e versionada da Delivery Approval Authority vincula principal, accountable subject, papel autorizado, escopo e período de validade.
- Cada atuação relevante produz attestation criptográfica imutável que vincula principal, papel, TaskEnvelope validado e seu digest canônico SHA-256, candidate SHA exato, decisão e versão da política aplicada.
- Executor, QA e Reviewer são independentes quando seus conjuntos de accountable subjects são dois a dois disjuntos para o mesmo TaskEnvelope e candidate SHA.
- O verifier falha fechado diante de issuer, signer, binding ou papel ausente, desconhecido, expirado ou revogado; assinatura inválida; digest ou SHA divergente; aprovação ausente; ou sobreposição de accountable subjects.
- Issuers, chaves, algoritmos aceitos, rotação e revogação são valores versionados no trust profile próprio da autoridade. Mudá-los dentro do modelo aprovado não cria nova decisão arquitetural.
- `EPIC-001` possui a semântica e o contrato. `EPIC-091` somente consome o veredito para enforcement no repositório.

## Invariantes

- A attestation de aprovação não é uma assinatura de Prompt Bundle e não pode usar o trust scope da `SPEC-001`.
- Autenticação não concede papel; papel declarado no TaskEnvelope ou em label não substitui binding autorizado.
- Contas distintas não provam independência quando mapeiam para o mesmo accountable subject.
- Aprovação para um candidate SHA não é reutilizável após mudança do SHA ou do digest do TaskEnvelope.
- Ausência ou ambiguidade de evidência nunca degrada para approval manual implícito.
- O contrato e seus records preservam imutabilidade, canonicalização, hashes, lineage e verificação offline quando o trust material requerido estiver disponível.

## Alternativas consideradas

- GitHub como autoridade canônica: rejeitado por acoplar identidade, histórico de papel e prova de aprovação à retenção e às semânticas da plataforma.
- Serviço autoritativo próprio com ledger em PostgreSQL: rejeitado por ampliar prematuramente superfície operacional, segurança e dependências de bootstrap.
- Attestations criptográficas independentes: selecionado por fornecer prova portátil e imutável com o menor boundary semântico completo.

## Racional da seleção

A alternativa selecionada separa autenticação, autorização e aprovação sem transformar GitHub, `SPEC-001`, `EPIC-091` ou identidade do produto em autoridade indevida. O statement mínimo é verificável por conteúdo, assinatura, trust scope e identidade estável, e permite enforcement em diferentes plataformas sem mudar sua semântica.

## Consequências e trade-offs

- O projeto precisa publicar contrato versionado, trust profile, role bindings, attestations e casos de conformidade positivos e negativos.
- Rotação, revogação, validade temporal e recuperação de identidade passam a ser dependências operacionais explícitas.
- GitHub pode transportar ou exigir o veredito, mas seus approvals, labels, CODEOWNERS e autoria Git não são prova suficiente isoladamente.
- Primitives de canonicalização, SHA-256 e trust store podem ser reutilizadas tecnicamente, desde que namespace, key scope, payload e finalidade permaneçam separados da `SPEC-001` e da supply chain.
- Mudança futura da plataforma de repositório não invalida attestations já verificáveis.

## Dependências arquiteturais

`ADR-003`, `ADR-006`, `ADR-007`, `ADR-010`

## Compatibilidade e migration

Não existe contrato anterior compatível a migrar. Aprovações legadas sem vínculo verificável não são promovidas automaticamente; consumidores permanecem bloqueados até receberem attestations conformes. O contrato futuro deve versionar mudanças breaking e preservar verificação histórica durante a retenção aplicável.

## Segurança e operação

O trust profile deve distinguir issuer de identidade, autoridade de role binding e signer de attestations; limitar scopes; registrar validade e revogação; e impedir cross-use de chaves da `SPEC-001` ou da supply chain. Evidence não deve conter credenciais ou secrets. Falhas preservam diagnóstico seguro sem aceitar fallback.

## Gate de mudança

Mudança na authority source, identidade canônica, regra de independência, payload obrigatório ou semântica fail-closed exige ADR substituta. Issuers, chaves, algoritmos aprovados e parâmetros de rotação permanecem em profile versionado quando preservarem este boundary.

## Verificação de conformidade

- O contrato deve definir schemas e canonicalização para trust profile, role binding e delivery approval attestation.
- Vetores devem provar vínculo ao TaskEnvelope/digest e ao candidate SHA exato.
- Casos negativos devem rejeitar assinatura, issuer, binding, papel ou scope inválido; revogação; expiração; mismatch de hashes; approval ausente; replay; e sobreposição entre Executor, QA e Reviewer.
- Nenhum verifier pode considerar role/label declarada, IDs distintos, CODEOWNERS, contagem de approvals, autoria Git não verificada ou assinatura de Prompt Bundle como substituto isolado.
- Histórias e TaskEnvelopes que produzam ou consumam este boundary devem referenciar `ADR-058`.

## Rastreabilidade SAR

- **Requisitos owned:** `Nenhum`; controle arquitetural derivado de `ROLE_AUTHORITY_MATRIX.md`, `DEFINITION_OF_DONE.md` e do TaskEnvelope.
- **Épico owner:** `EPIC-001`.
- **Épico consumidor:** `EPIC-091`.
- **Matriz canônica:** `docs/07-assurance/ADR_APPLICABILITY_MATRIX.csv`.
- **Grafo de decisões:** `docs/02-architecture/ADR_DEPENDENCY_GRAPH.json`.
- **Decisão do Owner:** `APPROVE_OPTION_B`, registrada em 2026-08-17.

## Relação com especificações existentes

`SPEC-001` continua responsável exclusivamente por Prompt Bundles. Seus hashes, canonicalização e trust-store patterns podem orientar componentes reutilizáveis, mas suas signatures não autenticam role binding, atuação, approval ou candidate SHA. Nenhuma alteração da `SPEC-001` é necessária por esta decisão.
