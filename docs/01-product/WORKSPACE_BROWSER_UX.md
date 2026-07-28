# UX do navegador de diretórios do servidor

## Objetivo

Permitir que uma pessoa opere grandes acervos no servidor por uma interface gráfica clara, sem depender de terminal e sem expor o filesystem inteiro.

## Fluxo principal

1. abrir ou criar um projeto;
2. escolher **Adicionar lote por diretório do servidor**;
3. selecionar uma raiz autorizada por nome amigável;
4. navegar por árvore/lista com breadcrumbs;
5. pesquisar ou filtrar pastas e formatos;
6. selecionar diretório de origem e, quando aplicável, referências auxiliares;
7. revisar prévia: quantidade, volume, extensões, arquivos ignorados e problemas;
8. escolher destino dentro de uma raiz gravável;
9. confirmar e criar job;
10. acompanhar progresso, alertas e resultados no frontend.

## Requisitos de usabilidade

- não exigir digitação de comandos ou caminhos absolutos;
- permitir teclado, leitores de tela e navegação responsiva;
- exibir estados de carregamento, diretório vazio e falha de permissão;
- suportar paginação/virtualização para diretórios muito grandes;
- manter seleção ao navegar e voltar;
- indicar claramente raiz somente leitura versus gravável;
- impedir confirmação quando origem e destino criem risco de sobrescrita ou recursão;
- fornecer modo avançado opcional para colar caminho relativo validado.

## Fora de escopo inicial

- navegar livremente por discos não cadastrados;
- montar compartilhamentos de rede a partir do browser;
- agente desktop para acesso direto à máquina cliente;
- sincronização automática de diretórios remotos.
