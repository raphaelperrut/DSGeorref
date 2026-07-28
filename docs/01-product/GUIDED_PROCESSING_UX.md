# Experiência guiada de processamento

## Problema a evitar

O frontend não deve reproduzir a taxonomia interna de sistemas anteriores com múltiplos modos parcialmente sobrepostos. Um usuário não deveria precisar saber antecipadamente se “bootstrap”, “busca espacial” ou “IA” constituem o fluxo correto.

## Modelo conceitual proposto

```text
Objetivo + condições dos dados + políticas
                  │
                  ▼
         recomendação explicável
                  │
                  ▼
       ProcessingPlan versionado
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
 localização   referências   matching/IA
       │          │          │
       └──────────┼──────────┘
                  ▼
       Strong Geometric Verifier e revisão
                  ▼
          artefatos e lineage
```

## Princípios de UX

- perguntar primeiro sobre o problema e os dados, não sobre algoritmos;
- progressive disclosure: parâmetros raros aparecem apenas no modo avançado;
- recomendação sempre explica motivo, limitações e impactos;
- usuário revisa o plano antes da execução;
- uso de IA e serviços externos é explícito;
- bootstrap é estratégia reutilizável dentro do plano;
- planos podem ser salvos, clonados e comparados;
- cada execução referencia uma versão imutável do plano;
- falhas sugerem próximos passos acionáveis, não apenas stack traces ou códigos.

## Material de aprendizagem esperado

- exemplos visuais de diferentes décadas e condições de dados;
- projeto demonstrativo isolado dos projetos reais;
- tutorial de navegação, configuração, execução, revisão e exportação;
- explicação visual de GCPs, resíduos, confiança, transformação e reprojeção;
- exemplos de quando não aceitar um resultado automático;
- ajuda contextual ligada à mesma versão dos contratos e parâmetros.

## Resultado e triagem em escala

- toda imagem terá um resultado lógico, mesmo quando falhar antes da transformação;
- a interface exibirá nome e diretório relativo em sucessos e falhas;
- o painel de lote priorizará filtros, agregações e revisão dos casos problemáticos;
- resultados rejeitados pelo Strong Geometric Verifier não serão apresentados como sucesso;
- recomendações de contorno explicarão riscos e nunca sugerirão relaxar silenciosamente gates críticos;
- para lotes e catálogos grandes, paginação, busca e exportação serão executadas no servidor.

A direção de produto, o contrato de resultados, os QualityProfiles, a revisão, os recursos e a deformação são governados por ADR-046, ADR-039, ADR-048 e pelos requisitos desta baseline.

## Escalonamento classic-first — AP-009

A UX deve distinguir tentativa clássica, motivo da falha, elegibilidade para IA, tentativa neural e resultado do SGV. IA não será apresentada como correção automática universal; entradas inválidas e falhas não elegíveis permanecerão explícitas.
