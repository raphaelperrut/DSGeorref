# Custo e unit economics — baseline 3.0

## Resposta executiva

O custo monetário exato não pode ser afirmado antes de benchmark e cotação de infraestrutura. Publicar um valor agora seria uma suposição. O SAR fecha o método de cálculo em BRL e transforma orçamento em gate do `ImplementationAuthorizationRecord` e da produção.

## TCO mensal

`TCO = compute + memória + storage primário + temporário + backup + bandwidth + energia/hosting + GPU + observabilidade + certificados + trabalho operacional + contingência`

## Unidades obrigatórias

- R$/job admitido;
- R$/imagem processada;
- R$/imagem aceita pelo SGV;
- R$/GiB-mês retido;
- R$/restore drill;
- R$/aquisição de referência.

## Decisão de investimento

- implementação inicia CPU-first;
- nenhuma compra de GPU é autorizada pela arquitetura;
- orçamento mensal e TCO de doze meses são inputs do Owner;
- variação acima de 20% contra o orçamento gera reforecast;
- capacidade ou qualidade não pode ser relaxada para esconder custo.

O schema `contracts/operations/operational-cost-assessment.schema.json` impede uma aprovação econômica sem valores e evidências reais.
