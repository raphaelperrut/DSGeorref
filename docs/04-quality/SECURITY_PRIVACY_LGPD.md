# Segurança, privacidade e LGPD

Imagens, coordenadas, nomes de arquivos, metadados, identidades, IPs e logs podem revelar pessoas, propriedades ou locais sensíveis. O projeto aplica minimização, classificação, privilégio mínimo, criptografia quando aplicável, retenção e trilha de auditoria.

Dados processados por uma instalação não serão usados para treinamento de modelos por padrão. Qualquer uso futuro para pesquisa ou melhoria exige política específica, base legal aplicável, informação transparente, controles de retirada e aprovação explícita do operador responsável.

Quem instala e opera DSGeorref é responsável por configuração, base legal, avisos e controles organizacionais. A documentação oficial fornecerá defaults seguros sem declarar conformidade automática.
## Instalação e supply chain

- secrets seguem contrato em camadas, princípio do menor privilégio e rotação auditável;
- apenas o ingress é publicado; banco, broker e workers permanecem em redes privadas;
- TLS é obrigatório para acesso remoto;
- imagens OCI e artefatos de release exigem checksum, assinatura, SBOM e provenance;
- Actions, imagens base e dependências críticas são fixadas por identificadores imutáveis;
- upgrades são iniciados pelo administrador, com preflight, migrations explícitas e recuperação testada;
- configurações inseguras bloqueiam startup ou publicação em vez de gerar warning permissivo.
## Modelos e conectividade

- pesos e runtimes são tratados como componentes de supply chain;
- ModelPacks exigem licença, hashes, assinatura, provenance e allowlist;
- modelos opcionais não são adquiridos sem ação explícita;
- modos de egress são aplicados por infraestrutura e aplicação;
- telemetria externa permanece desabilitada por padrão e opt-in;
- dados de usuários não são enviados a serviços de IA externos sem capability e consentimento explícitos.

## Mecanismos concretos — AP-003 e BP-003

ADR-028 exige contas locais, OIDC opcional, cookies seguros, CSRF, PATs escopados, RBAC server-side, bootstrap único e auditoria. AP-003 materializa sessões, request provenance, tokens, linking OIDC, enforcement, throttling, revogação, recovery e headers; BP-003 calibra Argon2id e limites operacionais.

## Implementação de autenticação aprovada

As regras consolidadas em AP-003 e BP-003 exigem sessão opaca server-side, Argon2id calibrado, CSRF vinculado à sessão, PATs hasheados, identidade OIDC por issuer/subject, autorização central, throttling persistente, sessões revogáveis, recovery kit offline e same-origin com headers verificáveis.
