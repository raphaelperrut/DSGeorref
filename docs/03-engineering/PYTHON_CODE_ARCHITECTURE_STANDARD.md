# Padrão de arquitetura de código Python

## Objetivo

Evitar módulos monolíticos, funções redundantes, importações circulares e implementações que apenas deslocam o problema entre camadas.

## Limites normativos

| Elemento | Alvo | Revisão obrigatória | Limite bloqueante |
|---|---:|---:|---:|
| Arquivo Python de produção | até 300 linhas físicas | acima de 400 | acima de 600 |
| Função ou método | até 40 linhas | acima de 60 | acima de 80 |
| Definições top-level por arquivo | até 12 | acima de 16 | acima de 20 |
| Métodos públicos por classe | até 10 | acima de 15 | acima de 20 |
| Branch points aproximados por função | até 8 | acima de 12 | acima de 15 |

Linhas em branco e comentários continuam contando no limite físico porque arquivos longos também aumentam custo de navegação e revisão. Código gerado deve ficar em diretório identificado e é excluído apenas quando reproduzível por comando versionado.

## Regras de desenho

- cada módulo possui uma responsabilidade primária expressa por nome de domínio;
- casos de uso são implementados uma vez em `application` e reutilizados por API, CLI e worker;
- regras e invariantes ficam em `domain`, sem dependência de framework;
- I/O, ORM, filas, HTTP, filesystem e providers ficam em adapters;
- composition roots apenas montam dependências;
- funções públicas exigem tipos explícitos e comportamento de erro definido;
- não criar `utils.py`, `helpers.py`, `common.py` ou `misc.py` como depósito genérico;
- duplicação literal de implementação não trivial é bloqueada; similaridade semântica é revisada pelo Tech Lead;
- qualquer exceção aos limites exige Design Review com prazo ou justificativa permanente.

## Anti-alucinação

Antes de escrever código, o agente deve localizar o requisito, ADR, contrato, módulo, história e TaskEnvelope. Endpoint, tabela, estado, evento, path, profile ou regra inexistente não pode ser inventado. Contradição ou ausência interrompe a tarefa.

## Testes de arquitetura

O gate executa:

1. grafo de imports sem ciclos;
2. regras de camadas e imports proibidos;
3. limites de arquivo, função, classe e branch points;
4. detecção de duplicação exata de funções não triviais;
5. ausência de código em paths orientados por épico/issue;
6. compatibilidade sintática com Python 3.12.
