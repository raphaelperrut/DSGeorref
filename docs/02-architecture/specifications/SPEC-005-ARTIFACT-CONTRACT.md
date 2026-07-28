# SPEC-005 — Artifact Contract

- **Status:** `FROZEN`
- **Versão do contrato:** `1.0.0`
- **Baseline:** `SAR v2.8 — Fase E`
- **Owner normativo:** `BC-013`
- **ADRs governantes:** `ADR-021`, `ADR-022`, `ADR-023`, `ADR-024`, `ADR-025`, `ADR-043`
- **Bounded Contexts:** `BC-013`, transversal aos produtores
- **Compatibilidade:** `SemVer + JSON Schema Draft 2020-12`
- **Mudança breaking:** exige nova major version e revisão do Arquiteto


## 1. Propósito

O Artifact Contract define os arquivos e bundles produzidos pelo DSGeorref. Ele substitui listas vagas de “outputs” por tipos versionados, media types, validação, hashes, lineage e publicação. Um arquivo no filesystem não é automaticamente um artifact; ele se torna artifact somente quando descrito, validado e incluído em ArtifactSet publicado.

## 2. Modelo

`ArtifactDescriptor` descreve um arquivo imutável. `ArtifactSetManifest` agrega descriptors, inputs, producer, lineage, publication e root digest. `ArtifactValidationProfile` define validators. `ArtifactPublicationRecord` prova staging e promoção. O Artifact Kind Registry é a allowlist de espécies.

## 3. Identidade

Artifact tem UUID lógico e SHA-256 de conteúdo. ArtifactSet tem UUID e versão inteira. Conteúdo idêntico pode ser deduplicado, mas identidades lógicas e lineage permanecem. Relative path é locator interno, não identidade. Path absoluto é proibido em contrato de domínio.

## 4. Imutabilidade

Após publicação, bytes, descriptor e manifest não mudam. Correção cria novo artifact e novo ArtifactSet. A visão corrente aponta para sets, sem reescrever histórico. Scrubbing que detecta corrupção marca estado e inicia recuperação; não altera hash esperado.

## 5. Publicação atômica

Writer cria staging no mesmo filesystem, escreve bytes, fsync arquivos e diretório, valida, calcula hashes, escreve manifest, fsync e faz rename atômico. Banco é atualizado por UoW/outbox conforme ADR. Artifact parcial nunca recebe status PUBLISHED.

## 6. Root digest

Root digest cobre manifest canônico com o próprio campo zerado e descriptors ordenados por artifact id. Ele não substitui hashes individuais. Algoritmo SHA-256 é normativo. Canonicalização segue JSON profile do projeto.

## 7. Paths

Paths são relativos, NFC, sem `..`, symlink escape, controle ou nomes reservados. O resolver aplica root allowlist, openat/realpath safe pattern e orçamento de path. Usuário e navegador nunca fornecem path final do host.

## 8. COG Raster

`COG_RASTER` é GeoTIFF Cloud Optimized validado independentemente. Descriptor exige CRS, bbox, shape, resolution, nodata, pixel semantics e bands. Profile verifica tiling, internal overviews, IFD ordering, range readability, compression permitida, geotransform, CRS e ausência de corrupção. Extensão é `.tif`.

## 9. GeoTIFF intermediate

`GEOTIFF_INTERMEDIATE` pode não satisfazer COG, mas deve ser georreferenciado ou declarar explicitamente ausência/etapa. Ele é SUPPORTING e normalmente não é export final. Retenção é menor e depende de recomputabilidade. Não pode ser rotulado COG sem profile COG PASS.

## 10. Analysis Mask

`ANALYSIS_MASK` delimita pixels usados em matching e validação; não altera output extent por si. Deve declarar alinhamento, CRS, shape, semantic values e relação ao raster. Soft priors e hard exclusions são distinguidos por metadata. Preview não substitui mask científica.

## 11. Validity Mask

`VALIDITY_MASK` representa pixels válidos/nodata no output. Deve corresponder exatamente à grid do raster associado e declarar valores. Divergência é hard fail.

## 12. Vector GPKG

`VECTOR_GPKG` é o formato vetorial canônico para entrega rica. Profile verifica SQLite/GPKG, SRS, geometry types, spatial indexes quando exigidos, encoding e layers allowlisted. Schemas de atributos são versionados.

## 13. GeoJSON preview

`VECTOR_GEOJSON_PREVIEW` é simplificado e voltado à visualização. Deve declarar CRS normalizado na boundary, tolerância de simplificação e source artifact. Não é substituto do GPKG científico quando precisão ou schema completo forem requeridos.

## 14. GCP Vector

`GCP_VECTOR` contém IDs, coordenadas nos espaços explícitos, incerteza, provenance, lifecycle e status. Nunca mistura pixel center/corner implicitamente. Exports preservam referência ao CorrectionSet/EditCase.

## 15. Footprint Vector

`FOOTPRINT_VECTOR` registra footprint e topology diagnostics. Geometria inválida, orientation ou self-intersection são tratadas pelo profile. CRS e datum são obrigatórios.

## 16. Quality Report

`QUALITY_REPORT` contém métricas, thresholds/profile version, verdicts, diagnostics e links para evidence. JSON é canônico; HTML/PDF são renderizações. Relatório não decide sozinho a visão corrente.

## 17. Deformation Report

`DEFORMATION_REPORT` registra jacobians, scale, anisotropy, shear, foldovers e mapas derivados em escalas definidas. Deve distinguir medidas científicas de visualização.

## 18. SGV Report

`SGV_REPORT` é JSON tipado com hard gates, gray zone e verdict. É assinado pelo componente/verificador e referencia candidate transform e inputs. Hard fail não pode ser sobrescrito por outro artifact.

## 19. Audit Report

`AUDIT_REPORT` é export derivado do canal append-only. Inclui intervalo, filtros, digests e redaction profile. Não contém secrets. CSV/PDF são views; JSON mantém estrutura.

## 20. Validation Report

`VALIDATION_REPORT` agrega validators executados, versões, status, parâmetros e detalhes. Um ArtifactSet só publica se todos hard validators passarem. Soft warning permanece no manifest/evidence.

## 21. Provenance Manifest

`PROVENANCE_MANIFEST` registra inputs, software, profiles, models, parameters, environment class e lineage. Ele complementa o ArtifactSet manifest e pode ter granularidade científica maior.

## 22. Snapshots

`PROCESSING_PLAN_SNAPSHOT` e `RESULT_SNAPSHOT_RECORD` são representações imutáveis de planos e resultados. Eles referenciam artifacts por ID/hash e schemas de domínio; não embutem bytes grandes.

## 23. Edit artifacts

`EDIT_BUNDLE`, `REVIEW_DECISION` e `APPLICATION_RECEIPT` implementam `SPEC-002`. Eles preservam revisão, actors, rationale, hash e result lineage. Bundle inválido nunca é aplicado.

## 24. AI Execution Report

`AI_EXECUTION_REPORT` registra backend/protocol/model pack, supports decision, estimate, runtime record, validation e publication candidate. Não contém pesos nem dados brutos e declara que SGV independente é requerido.

## 25. Thumbnail

`THUMBNAIL` é visualização pequena, sem autoridade geoespacial. Pode remover metadata sensível conforme profile. Dimensões, orientação e source hash são registrados.

## 26. Map Preview

`MAP_PREVIEW` é composição renderizada com extent, style id e source artifacts. Não é output científico e deve ter watermark/status quando candidate ou reviewable.

## 27. Diff Preview

`DIFF_PREVIEW` compara base e candidate com método declarado. Escala, palette e clipping entram em properties. Ele auxilia revisão e não substitui métricas.

## 28. Mask Preview

`MASK_PREVIEW` visualiza mask com legenda e source hash. Downsampling deve preservar semântica descrita. Não pode ser usado como input de pipeline.

## 29. Media types

Media type e extensão devem concordar com registry. Valores não listados são rejeitados até nova versão. Parâmetros de media type são normalizados. Content sniffing é validação adicional, nunca substitui declaração.

## 30. Geospatial metadata

Artifacts geoespaciais declaram CRS, bbox, shape, resolution, nodata, pixel semantics e bands conforme espécie. Axis order é normalizado na boundary. Valores devem ser conferidos diretamente contra o arquivo por validator independente.

## 31. Validation profiles

Cada espécie aponta para profile versionado. Validators têm severidade HARD ou SOFT e parameters. Profile é imutável; promoção de thresholds segue benchmark/evidence. Writer não pode escolher profile mais permissivo sem autorização.

## 32. ArtifactSet

Um set reúne outputs semanticamente consistentes de uma Attempt/execução. Deve conter ao menos um artifact. Primary único quando o tipo de set exigir. Inputs e parent sets formam DAG. Ciclo de lineage é erro.

## 33. Manifest v2

A major 2 adiciona descriptors tipados, producer, publication e lineage obrigatórios. O schema v1 permanece em compatibility para leitura. Novos writers geram apenas v2. Migração v1→v2 exige enriquecimento por fontes verificáveis; ausência não pode ser inventada.

## 34. Backward compatibility

Leitores aceitam major anterior durante janela. Artifact bytes não são reescritos para migrar manifest. Adapter produz uma view v2 com indicação de campos unavailable quando o schema permitir; campos obrigatórios sem fonte bloqueiam promoção.

## 35. Retenção

Retenção depende de classe, estado, dependências e recomputabilidade. Primary, audit e snapshots têm políticas distintas de intermediate/previews. GC é reference-aware e nunca remove artifact alcançável por snapshot, case, hold ou backup.

## 36. Serving

Download passa por autorização e locator seguro. Content-Disposition, media type, length e checksum são definidos. Offload ao ingress usa token/headers internos controlados. Range é permitido para COG quando configurado.

## 37. Segurança

Parsers usam allowlist, limites e isolation. Zip bombs e arquivos poliglotas são rejeitados. Manifests não contêm secret/path host. HTML report é sanitizado e servido com headers apropriados.

## 38. Privacidade

Properties e reports seguem allowlist e redaction. Geolocalização pode ser sensível conforme projeto; exports exigem autorização. Thumbnail/preview não devem vazar margens ou metadata excluída.

## 39. Observabilidade

Métricas usam kind, status e size bucket. IDs e paths não são labels. Scrubbing, validation e publication produzem traces/evidence. Hash mismatch é alerta de integridade.

## 40. Erros

Códigos: `ARTIFACT_KIND_UNKNOWN`, `MEDIA_TYPE_MISMATCH`, `PATH_UNSAFE`, `HASH_MISMATCH`, `SIZE_MISMATCH`, `GEOSPATIAL_METADATA_MISMATCH`, `VALIDATION_HARD_FAIL`, `MANIFEST_INVALID`, `LINEAGE_CYCLE`, `STAGING_FAILED`, `FSYNC_FAILED`, `PUBLICATION_CONFLICT`, `UNSUPPORTED_MANIFEST_VERSION` e `ARTIFACT_NOT_AUTHORIZED`.

## 41. Testes

Golden files para cada kind, valid/invalid COG, truncated TIFF, unsafe path, wrong hash, wrong CRS, mask mismatch, invalid GPKG, manifest cycle, crash before rename, crash after rename e reconciliation. Restores verificam bytes e manifests.

## 42. Critérios de aceite

- registry completo para os kinds da Fase E;
- descriptor e manifest schemas válidos;
- COG/GeoTIFF/masks/vectors/reports/previews diferenciados;
- publication atomic e reconciliável;
- hashes e lineage explícitos;
- v1 preservada somente para leitura;
- validators e exemplos passam;
- producers listam `SPEC-005` no TaskEnvelope.

## 43. Condições de parada

A implementação para se um output não tiver kind, media type, schema/profile, hash, owner, retention ou publication semantics; se houver tentativa de mutar artifact publicado; ou se preview for usado como autoridade científica.
