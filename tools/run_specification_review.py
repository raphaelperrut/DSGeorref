from __future__ import annotations
import base64, copy, csv, hashlib, json, re, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
ROOT=Path(__file__).resolve().parents[1]
errors=[]
ZERO='0'*64

def load(rel):
 p=ROOT/rel
 if not p.exists(): errors.append(f'missing {rel}'); return None
 return json.loads(p.read_text()) if p.suffix=='.json' else yaml.safe_load(p.read_text())
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(o):return hashlib.sha256(canon(o)).hexdigest()
def validate(schema_rel,instance_rel):
 s=load(schema_rel);i=load(instance_rel)
 if s is None or i is None:return
 for e in Draft202012Validator(s,format_checker=FormatChecker()).iter_errors(i):errors.append(f'{instance_rel}: {e.message}')

specs=sorted((ROOT/'docs/02-architecture/specifications').glob('SPEC-00[1-5]-*.md'))
if len(specs)!=5:errors.append(f'expected 5 specifications, found {len(specs)}')
for p in specs:
 t=p.read_text()
 for section in ['Propósito','Version','Critérios de aceite','Condições de parada']:
  if section.lower() not in t.lower():errors.append(f'{p.name}: missing semantic section {section}')
 if len(t.split())<700:errors.append(f'{p.name}: specification too shallow')

pairs=[
 ('contracts/prompts/prompt-bundle.schema.json','contracts/prompts/examples/prompt-bundle.minimal.yaml'),
 ('contracts/prompts/prompt-bundle.schema.json','contracts/prompts/examples/prompt-bundle.composed.yaml'),
 ('contracts/prompts/prompt-bundle-lock.schema.json','contracts/prompts/examples/prompt-bundle.lock.json'),
 ('contracts/prompts/prompt-bundle-signature.schema.json','contracts/prompts/test-vectors/prompt-bundle-signature.json'),
 ('contracts/edit-cases/edit-case.schema.json','contracts/edit-cases/examples/edit-case-approved.json'),
 ('contracts/ai/capability-request.schema.json','contracts/ai/examples/capability-request.json'),
 ('contracts/templates/template.schema.json','contracts/templates/examples/issue-handoff-template.yaml'),
 ('contracts/artifacts/artifact-descriptor.schema.json','contracts/artifacts/examples/artifact-descriptor-cog.json'),
 ('contracts/artifacts/artifact-set-manifest.schema.json','contracts/artifacts/examples/artifact-set-manifest-2.0.0.json')]
for a,b in pairs:validate(a,b)

# Prompt hashes and signature.
b=load('contracts/prompts/examples/prompt-bundle.minimal.yaml');lock=load('contracts/prompts/examples/prompt-bundle.lock.json');v=load('contracts/prompts/test-vectors/prompt-bundle-signature.json')
if b and lock and v:
 proj=copy.deepcopy(b);proj['integrity']['payload_sha256']=ZERO;proj['integrity']['lock_digest_sha256']=ZERO;proj['signatures']=[]
 pd=digest(proj)
 lp=copy.deepcopy(lock);lp['lock_digest_sha256']=ZERO;ld=digest(lp)
 if pd!=b['integrity']['payload_sha256'] or pd!=lock['root_payload_sha256']:errors.append('prompt payload digest mismatch')
 if ld!=b['integrity']['lock_digest_sha256'] or ld!=lock['lock_digest_sha256']:errors.append('prompt lock digest mismatch')
 msg=b'DSGEOREF-PROMPT-BUNDLE-V1\0'+b['bundle_id'].encode()+b'\0'+b['bundle_version'].encode()+b'\0'+pd.encode()+b'\0'+ld.encode()
 pad=lambda s:s+'='*((4-len(s)%4)%4)
 try:Ed25519PublicKey.from_public_bytes(base64.urlsafe_b64decode(pad(v['public_key']))).verify(base64.urlsafe_b64decode(pad(v['signature'])),msg)
 except Exception as e:errors.append(f'prompt signature invalid: {e}')

# State machine.
sm=load('contracts/edit-cases/edit-case-state-machine.yaml')
if sm:
 states={sm['initial']}|set(sm['terminal'])|{x[k] for x in sm['transitions'] for k in ['from','to']}
 required={'DRAFT','IN_REVIEW','CHANGES_REQUESTED','APPROVED','APPLYING','APPLIED','VALIDATING','ACCEPTED','REJECTED','ROLLED_BACK','SUPERSEDED','CANCELLED'}
 if states!=required:errors.append('edit case states differ from contract')
 if len({(x['from'],x['event']) for x in sm['transitions']})!=len(sm['transitions']):errors.append('edit case nondeterministic transition')

# AI method order.
proto=load('contracts/ai/ai-backend-protocol.yaml')
if proto and proto.get('method_order')!=['supports','estimate','execute','validate','publish']:errors.append('AIBackend method order invalid')
if proto and [m['name'] for m in proto['methods']]!=proto['method_order']:errors.append('AIBackend method declaration mismatch')

# Artifact registry/manifest.
reg=load('contracts/artifacts/artifact-kind-registry.yaml');man=load('contracts/artifacts/examples/artifact-set-manifest-2.0.0.json')
required_kinds={'COG_RASTER','GEOTIFF_INTERMEDIATE','ANALYSIS_MASK','VALIDITY_MASK','VECTOR_GPKG','VECTOR_GEOJSON_PREVIEW','AUDIT_REPORT','THUMBNAIL','MAP_PREVIEW'}
if reg and not required_kinds.issubset({k['kind'] for k in reg['kinds']}):errors.append('artifact kind registry incomplete')
if reg and man:
 allowed={k['kind'] for k in reg['kinds']}
 if any(a['artifact_kind'] not in allowed for a in man['artifacts']):errors.append('manifest uses unknown artifact kind')

# Contract ownership.
with (ROOT/'contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
owned={r['contract'] for r in rows}
actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'contracts').rglob('*') if p.is_file() and p.name!='CONTEXT_CONTRACT_OWNERSHIP.csv'}
if owned!=actual:
 for x in sorted(actual-owned):errors.append(f'contract without owner: {x}')
 for x in sorted(owned-actual):errors.append(f'ownership points to missing contract: {x}')

# Task envelope applicability.
for p in (ROOT/'.codex/tasks').glob('TASK-*.json'):
 o=json.loads(p.read_text())
 if o.get('specification_review_status')!='PASS' or o.get('specification_baseline')!='SAR-v2.9-PHASE-F':errors.append(f'{p.name}: Phase E metadata invalid')
 if len(o.get('applicable_specifications',[]))<2:errors.append(f'{p.name}: insufficient applicable specifications')
 for sid in o.get('applicable_specifications',[]):
  if not list((ROOT/'docs/02-architecture/specifications').glob(sid+'-*.md')):errors.append(f'{p.name}: missing {sid}')

# No unresolved placeholders in Phase E artifacts.
for root in [ROOT/'docs/02-architecture/specifications',ROOT/'contracts/prompts',ROOT/'contracts/edit-cases',ROOT/'contracts/ai',ROOT/'contracts/templates',ROOT/'contracts/artifacts']:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix in {'.md','.json','.yaml','.yml','.csv'}:
   if re.search(r'\b(TBD|TODO|FIXME)\b',p.read_text(errors='ignore')):errors.append(f'placeholder in {p.relative_to(ROOT)}')

result={'schema_version':'1.0.0','phase':'E','approved':not errors,'blocking_findings_open':len(errors),'specifications':5,'task_envelopes':len(list((ROOT/'.codex/tasks').glob('TASK-*.json'))),'checked_at':'2026-07-27T00:00:00Z','errors':errors}
(ROOT/'docs/07-assurance/PHASE-E-SPECIFICATION-REVIEW-RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if errors:
 print('SPECIFICATION REVIEW FAILED')
 for e in errors[:200]:print('-',e)
 sys.exit(1)
print('SPECIFICATION REVIEW PASS')
print('specifications: 5')
print(f"task envelopes: {result['task_envelopes']}")
