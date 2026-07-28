# Threat model inicial

Principais ameaças: arquivo malicioso, decompression bomb, parser GIS vulnerável, SSRF, credenciais em URL, path traversal, escape por symlink, leitura/escrita fora do workspace, IDOR entre projetos, elevação de privilégio, operações administrativas sem auth, exfiltração por logs, checkpoint malicioso, supply chain, consumo abusivo de CPU/GPU/disco, acionamento indevido de operação paga em provider, plano de processamento enganoso e falso positivo geoespacial.

Controles prioritários: autenticação para exposição em rede, RBAC da instância, raízes de workspace registradas, canonicalização de caminhos, sandbox/limits, scanner real fail-closed, gateway de fontes com compra bloqueada, consentimento explícito para IA/serviços externos, secrets manager, SBOM, model manifest, audit log, ProcessingPlan versionado e revisão humana para baixa confiança.
## Providers externos e cache

Ameaças específicas incluem redirects para rede privada, DNS rebinding, arquivos remotos maliciosos, decompression bomb, URL assinada vazada, alteração de termos, ativo pago classificado incorretamente, cache poisoning, checksum substituído, redistribuição indevida e exfiltração por query. Mitigações: gateway allowlisted, egress policy, validação de URL/redirect/DNS, limites, quarentena, checksums, estados fail-closed, audit log, secrets fora de logs e cache governado por licença.
