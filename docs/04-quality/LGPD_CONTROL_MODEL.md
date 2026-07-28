# Modelo de controle LGPD — baseline 3.0

Este documento é uma arquitetura de privacidade, não substitui a decisão jurídica do controlador.

## Invariantes

- nenhuma categoria de dado é coletada sem finalidade e decisão de base pelo controlador;
- minimização, acesso por projeto, redaction e retenção por classe são obrigatórios;
- imagens e geolocalização não treinam modelos automaticamente;
- egress e providers são allowlisted e auditados;
- direitos, incidentes, exclusão e legal hold possuem workflow e evidência;
- audit ledger não é usado como analytics nem expõe secret, raster ou path absoluto;
- support bundle exige ação explícita e expira em no máximo 30 dias sem incident hold.

O inventário por categoria está em `contracts/privacy/lgpd-control-matrix.csv`. Antes de uso público, o Owner deve aprovar ROPA, papéis de controlador/operador, canal de direitos, política de retenção e avaliação de impacto quando aplicável.
