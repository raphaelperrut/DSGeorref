# Visão de domínio

O DSGeorref transforma imagens históricas ou não georreferenciadas em resultados espaciais verificáveis, reproduzíveis e auditáveis. O diferencial central não é a interface, o broker ou o banco: é a combinação de **georreferenciamento**, **verificação geométrica fail-closed** e **recuperação por mosaico relativo**.

## Core domain

- Georreferenciamento (`BC-006`);
- Verificação Geométrica e Qualidade (`BC-007`);
- Mosaico Relativo (`BC-008`).

## Regra estratégica

Nenhum contexto, inclusive IA, UI ou jobs, pode aceitar um resultado geométrico em nome de `BC-007`. Nenhum componente técnico pode se tornar fonte de verdade de um bounded context.

## Linguagem

Termos iguais com significados diferentes recebem nomes explícitos por contexto. Por exemplo, `AttemptExecution` em Jobs é execução técnica; `GeoreferencingAttempt` é tentativa científica. Eles não compartilham classe, tabela ou state machine.
