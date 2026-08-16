from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def rows(p):
    with (ROOT/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
ctx=rows("docs/02-architecture/ddd/BOUNDED_CONTEXT_INDEX.csv")
ctx_ids={r["context_id"] for r in ctx}
if len(ctx)!=16: errors.append(f"expected 16 contexts, found {len(ctx)}")
if sum(1 for r in ctx if r["classification"]=="Core")!=3: errors.append("expected 3 core contexts")
for rel,key,count in [("docs/06-delivery/EPIC_INDEX.csv","epic_id",110),("docs/06-delivery/STORY_INDEX.csv","story_id",759),("docs/06-delivery/ISSUE_INDEX.csv","issue_id",869),("docs/01-product/REQUIREMENT_INDEX.csv","requirement_id",376)]:
    rr=rows(rel)
    if len(rr)!=count: errors.append(f"{rel}: count drift")
    for r in rr:
        bc=r.get("bounded_context") or r.get("owning_context")
        if bc not in ctx_ids: errors.append(f"{rel} {r.get(key)}: invalid context {bc}")
for p in ROOT.glob(".codex/tasks/TASK-*.json"):
    o=json.loads(p.read_text())
    if o.get("bounded_context") not in ctx_ids: errors.append(f"{p.name}: missing context")
    if o.get("ddd_review_status")!="PASS": errors.append(f"{p.name}: DDD review not PASS")
    if any(re.match(r"src/backend/dsgeorref/(domain|application|adapters)/",x) for x in o.get("allow_paths",[])): errors.append(f"{p.name}: global layer path")
    if o.get("domain_model_impact") not in {"NONE","LOCAL_MODEL","PUBLIC_CONTRACT","CROSS_CONTEXT_INTEGRATION"}: errors.append(f"{p.name}: impact absent")
cm=rows("docs/02-architecture/ddd/CONTEXT_MAP.csv")
seen=set()
for e in cm:
    a,b=e["upstream"],e["downstream"]
    if a not in ctx_ids or b not in ctx_ids: errors.append(f"bad context map edge {a}->{b}")
    if a==b: errors.append(f"self context relationship {a}")
    key=(a,b,e.get("pattern",""))
    if key in seen: errors.append(f"duplicate context relationship {key}")
    seen.add(key)
    if not e.get("pattern") or not e.get("published_language"): errors.append(f"incomplete context relationship {a}->{b}")
# Context feedback loops are allowed only through published contracts/events.
# Direct implementation imports are prohibited by ADR-024/025 and the boundary contract;
# therefore the validator does not interpret business feedback as a code dependency cycle.
co=rows("contracts/contexts/CONTEXT_CONTRACT_OWNERSHIP.csv")
if not co: errors.append("contract ownership absent")
for r in co:
    if r["owner_context"] not in ctx_ids|{"TECHNICAL-SHARED"}: errors.append(f"bad contract owner {r}")
for n in range(23,26):
    if not list(ROOT.glob(f"docs/02-architecture/adrs/ADR-{n:03d}-*.md")): errors.append(f"ADR-{n:03d} absent")
for p in ROOT.glob("docs/06-delivery/stories/STORY-*.md"):
    if "## Domain-Driven Design — Fase C" not in p.read_text(): errors.append(f"{p.name}: DDD section absent")
rep=json.loads((ROOT/"docs/07-assurance/PHASE-C-DOMAIN-DRIVEN-DESIGN-REPORT.json").read_text())
if rep.get("approved") is not True or rep.get("blocking_findings_open")!=0: errors.append("Phase C not approved")
if errors:
    print("DOMAIN DRIVEN DESIGN REVIEW FAILED")
    for e in errors[:300]:print("-",e)
    sys.exit(1)
print("DOMAIN DRIVEN DESIGN REVIEW PASS")
print("contexts:",len(ctx))
print("context_map_edges:",len(cm))
print("contracts_owned:",len(co))
