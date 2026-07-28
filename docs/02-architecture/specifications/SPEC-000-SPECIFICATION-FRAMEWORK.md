# SPEC-000 — Framework de especificações executáveis

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-001`
- **ADRs governantes:** `ADR-006`, `ADR-010`, `ADR-024`
- **Bounded Contexts:** `BC-001`, transversal
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Finalidade

Este documento define como uma especificação normativa do DSGeorref é escrita, versionada, validada e promovida. Uma especificação não é uma descrição aspiracional: ela é um contrato verificável por schema, exemplo, vetor de teste e regra de compatibilidade. Texto e schema formam uma única unidade; divergência entre eles bloqueia a implementação.

## 2. Hierarquia normativa

A ordem de precedência é: políticas externas aplicáveis; ADRs aceitas; especificações `SPEC-*`; contratos de interface e domínio; Application e Benchmark Profiles; TaskEnvelope; história; implementação. Um nível inferior nunca pode ampliar autoridade, relaxar uma invariável ou criar estado não autorizado pelo nível superior.

## 3. Estrutura obrigatória

Cada especificação deve registrar: escopo, linguagem normativa, modelo de dados, estados quando aplicável, operações, invariantes, erros, segurança, privacidade, observabilidade, versionamento, compatibilidade, exemplos válidos, vetores negativos, algoritmo de validação, critérios de publicação e condições de parada.

## 4. Artefatos executáveis

Cada especificação possui pelo menos um JSON Schema Draft 2020-12 ou protocolo YAML equivalente, exemplos válidos, um conjunto de casos inválidos e um validador no repositório. Identificadores públicos são estáveis. Campos removidos ou reinterpretados exigem major version.

## 5. Compatibilidade

- patch: correção textual ou restrição que não altera instâncias válidas;
- minor: campo opcional, novo valor extensível ou nova operação compatível;
- major: remoção, alteração de significado, novo campo obrigatório ou mudança de canonicalização;
- leitores devem rejeitar major desconhecida e preservar campos extensíveis somente onde o schema autoriza;
- writers produzem apenas a versão explicitamente pinada no TaskEnvelope.

## 6. Estado de promoção

`DRAFT` permite discussão; `CANDIDATE` exige schemas e exemplos; `FROZEN` autoriza implementação; `DEPRECATED` mantém leitura por janela declarada; `RETIRED` proíbe novas gravações. As cinco especificações da Fase E são promovidas como `FROZEN`.

## 7. Condições de parada

A execução deve parar se um schema não existir, se texto e schema divergirem, se uma versão requerida não estiver suportada, se hash ou assinatura falhar, se houver transição de estado não autorizada ou se um backend tentar publicar sem validação obrigatória.
