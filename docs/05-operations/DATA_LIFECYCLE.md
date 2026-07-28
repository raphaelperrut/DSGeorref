# Ciclo de vida, retenção e garbage collection

## Princípio

A remoção é orientada por classe, estado e dependência; nunca apenas por idade ou caminho. O DSGeorref deve preservar resultados vigentes, lineage, snapshots fixados, evidências de qualidade e holds administrativos.

## Estados do ciclo de remoção

```text
eligible
  ↓
tombstoned
  ↓
quarantined
  ↓
purged
```

Um objeto pode retornar de `quarantined` quando uma referência protegida reaparecer ou um administrador cancelar a operação durante o período de graça.

## RetentionPolicy

Cada policy deve informar:

- classes e estados cobertos;
- prazos e condições;
- período de graça;
- proteções e holds;
- comportamento para conteúdo deduplicado;
- autorização necessária;
- dry-run e estimativa de bytes;
- versão, autor e data de vigência.

## Regras por classe

- acervos externos: somente desvinculação do catálogo por padrão;
- ArtifactSets vigentes: protegidos;
- versões superseded: elegíveis conforme lineage e policy;
- diagnósticos e temporários: menor retenção;
- GCPs, CorrectionSets e manifests: preservados enquanto necessários à reprodução;
- checkpoints: removíveis quando incompatíveis, expirados ou não protegidos;
- cache externo: respeita licença, retenção do provider e reprodução;
- audit logs: seguem baseline de segurança independente da telemetria operacional;
- BackupSets: removidos somente sem quebrar a cadeia restaurável.
- RelativeMosaicReportSnapshots: preservados quando protegidos por lineage, publicação, comparação ou bundle de reprodução;
- previews, tiles visuais e mapas densos de provenance: derivados e elegíveis conforme policy, desde que possam ser reconstruídos;
- exports técnicos e de reprodução: tratados conforme pinning, licença, auditoria e dependências registradas.

## Garantias

- nenhuma exclusão direta por path;
- nenhum objeto compartilhado é purgado enquanto houver referência protegida;
- toda purga tem tombstone e evento de auditoria;
- falhas parciais são reconciliáveis;
- relatórios apresentam objetos bloqueados e justificativas;
- testes cobrem corrida entre criação de referência e GC.
