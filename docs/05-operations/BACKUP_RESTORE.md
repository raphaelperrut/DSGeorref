# Backup e restore

## Unidade de recuperação

A unidade normativa é o `BackupSet` coordenado definido na ADR-027. Uma cópia de banco ou diretório isolada pode ser útil operacionalmente, mas não constitui backup completo do DSGeorref.

Cada BackupSet registra:

- identificador, estado, tipo e policy;
- watermark de consistência;
- versão da aplicação, migrations e imagens OCI;
- dump/snapshot do PostgreSQL;
- catálogo de artefatos gerenciados incluídos e omitidos;
- checksums, tamanhos e manifests;
- referências lógicas a raízes externas;
- evidências da verificação e do restore drill.

## Classes de dados

| Classe | Comportamento padrão |
|---|---|
| PostgreSQL/PostGIS | incluído em todo BackupSet operacional |
| ArtifactSets e manifests vigentes | incluídos conforme policy e consistência |
| acervos originais externos | referenciados por fingerprint; cópia exige policy explícita |
| cache regenerável | normalmente excluído, salvo quando protegido por reprodução |
| staging e temporários | excluídos |
| audit logs | incluídos ou exportados segundo retenção de segurança |
| RabbitMQ | não autoritativo; filas reconstruídas do PostgreSQL |
| secrets | nunca em texto aberto; reprovisionados ou restaurados por mecanismo criptografado separado |

## Restore drill

Todo baseline de produção deverá definir frequência e amostragem de restore drills isolados. O exercício verifica:

1. provisionamento compatível;
2. restauração do banco e dos artefatos;
3. migrations e inicialização;
4. checksums e lineage;
5. abertura amostral de formatos geoespaciais;
6. raízes externas disponíveis ou explicitamente ausentes;
7. reconstrução de jobs;
8. RPO, RTO e evidência final.

Falha de restore drill bloqueia o gate operacional correspondente até remediação e repetição bem-sucedida.

## Requisitos de segurança

- ambiente de restauração sem egress ou efeitos externos por padrão;
- acesso por privilégio mínimo;
- dados temporários eliminados após o drill;
- nenhuma credencial em manifests ou logs;
- confirmação explícita antes de restaurar sobre uma instalação existente;
- documentação de rollback quando migrations forem aplicadas.
## Objetivos congelados pela Fase G

RPO/RTO e classes estão em `contracts/operations/recovery-objectives.yaml`. Produção exige restore drill isolado com checksums, tempo medido e evidência. A arquitetura é recovery-oriented e não declara failover automático.
