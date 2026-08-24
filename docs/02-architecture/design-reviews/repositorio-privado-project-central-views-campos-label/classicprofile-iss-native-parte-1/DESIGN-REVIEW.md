# Design review — engineering foundation conformance

- **Candidate:** `ISSUE-0800` / `STORY-0690` / `TASK-0690`
- **Owner:** `BC-001 — Governança de Engenharia e Entrega`
- **Status:** implementação candidata; revisão independente pendente
- **Contract version:** `1.0.0`

## Propósito e limite

Este slice congela o menor contrato declarativo capaz de tornar verificáveis os dez
requisitos atribuídos à ISSUE-0800. Ele não implementa runtime, endpoint, persistência,
estado de produto ou ferramenta de enforcement. As histórias descendentes consomem o
profile publicado e materializam somente suas capacidades já atribuídas.

O contrato reutiliza `contracts/errors/problem-details.schema.json`,
`contracts/http/openapi.yaml` e o contrato existente de fronteiras da fundação. Nenhum
payload desses owners é duplicado.

## Contrato publicado

`foundation-conformance.schema.json` define um profile fail-closed com dez controles:

1. RootSIFT float32, profile pinado e baseline clássica anterior à IA elegível;
2. aceite e evidência derivados de contrato publicado, com revisão explícita de mudança;
3. CRS tipado por pyproj, `always_xy`, dupla precisão e rejeição de CRS inválido;
4. checkpoints entre produtor e consumidor compatíveis em schema, inputs, versões e hashes;
5. catálogo de estados versionado e somente transições registradas;
6. namespace `dsgeorref`, application services compartilhados e adapters finos;
7. erros tipados e mapping versionado para o Problem Details existente;
8. cliente TypeScript gerado exclusivamente do OpenAPI, com diff gate determinístico;
9. registry local, versionado, auditável e incapaz de contornar gates;
10. core, API e runners obrigatórios e separados pelo contrato já publicado.

O exemplo positivo contém todos os controles. Objetos normativos rejeitam propriedades
desconhecidas, campos ausentes e valores permissivos.

## Rastreabilidade e failure modes

O `contract-manifest.yaml` liga cada requisito ao JSON Pointer do seu controle, ao teste
canônico exigido pelo TaskEnvelope e aos failure modes rejeitados. A suíte cobre alteração
permissiva de cada controle, ausência de evidência, mudança sem review, checkpoint
incompatível, estado/transição não registrado, fallback genérico, geração manual e bypass
de gate.

Estados concretos do Project, IDs de produtores/consumidores e parâmetros científicos não
são definidos aqui porque pertencem aos contratos materializados por seus owners. O
profile exige catálogo/contrato versionado e falha fechado quando a referência obrigatória
não existe ou não é compatível.

## Compatibilidade

O contrato segue SemVer e JSON Schema Draft 2020-12. Adição opcional compatível pode usar
a major atual. Remoção, renomeação, mudança de tipo, relaxamento de invariante ou alteração
de authority exige nova major e revisão explícita do Arquiteto. Readers não ignoram campos
desconhecidos.

## Impacto operacional

- **Runtime:** não incluído.
- **HTTP:** não aplicável; o OpenAPI é somente uma referência normativa e não foi alterado.
- **Banco/migration:** não aplicável; nenhum estado persistido foi criado.
- **Frontend/Geo/IA:** nenhum código foi criado; apenas invariantes já governados foram
  publicados como conformance policy.
- **Artifact publication:** os três artefatos públicos estão registrados com owner `BC-001`.

## Riscos, limitações e rollback

- O contrato é declarativo; enforcement de runtime permanece nas histórias descendentes e
  não pode ser alegado por este candidato.
- Os testes provam schema, rastreabilidade e rejeição fail-closed, não performance,
  compatibilidade ABI nem qualidade científica.
- Antes de qualquer consumer integrado, rollback é a reversão deste candidato. Depois de
  consumo pinado, a versão permanece histórica e qualquer correção ocorre por versão
  sucessora; remoção ou sobrescrita é proibida.
- QA e Reviewer independentes permanecem pendentes e devem avaliar o mesmo commit candidato.

## TaskEnvelope

O envelope foi corrigido somente para incluir seu próprio arquivo de controle, o registry
de ownership, o teste diretamente obrigatório e a evidence já declarada. Não houve
ampliação de data plane, dependência ou grafo.
