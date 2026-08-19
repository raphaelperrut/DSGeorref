from pathlib import Path
import csv,json,re,sys,yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def rows(rel):
    with (ROOT/rel).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
required=[
"docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.md","docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.json","docs/07-assurance/PHASE-G-ISSUE-INVESTMENT-REVIEW.csv","docs/07-assurance/CTO_INVESTMENT_GATE_MATRIX.csv","docs/06-delivery/PHASE-G-CTO-REVIEW-CHARTER.md","docs/02-architecture/sar/SAR-220-PHASE-G-CTO-REVIEW.md","contracts/operations/cto-control-catalog.yaml","contracts/operations/slo-sli-catalog.yaml","contracts/operations/lock-and-queue-policy.yaml","contracts/operations/recovery-objectives.yaml","contracts/operations/cost-model.yaml","contracts/operations/operational-cost-assessment.schema.json","contracts/operations/version-and-rollback-matrix.yaml","contracts/operations/external-dependency-register.csv","contracts/operations/vendor-exit-matrix.csv","contracts/privacy/lgpd-control-matrix.csv","contracts/assurance/phase-g-cto-review.schema.json","docs/05-operations/PRODUCTION_READINESS_GATES.md","docs/06-delivery/RISK_REGISTER.csv"]
for rel in required:
    if not (ROOT/rel).exists():errors.append("missing "+rel)
report=json.loads((ROOT/"docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.json").read_text())
if report.get("status")!="APPROVED" or report.get("blocking_findings_open")!=0:errors.append("Phase G not approved")
if report.get("investment_recommendation")!="PROCEED_STAGED":errors.append("investment recommendation drift")
controls=yaml.safe_load((ROOT/"contracts/operations/cto-control-catalog.yaml").read_text())["controls"]
ids={c["id"] for c in controls}
if len(ids)!=15:errors.append("expected 15 CTO controls")
matrix=rows("docs/07-assurance/PHASE-G-ISSUE-INVESTMENT-REVIEW.csv")
issues=rows("docs/06-delivery/ISSUE_INDEX.csv")
if len(matrix)!=870 or {r["issue_id"] for r in matrix}!={r["issue_id"] for r in issues}:errors.append("Phase G issue coverage drift")
risk=rows("docs/06-delivery/RISK_REGISTER.csv")
if len(risk)!=40:errors.append("active risk register must contain 40 consolidated risks")
for r in risk:
    if r.get("owner_role") in {"","Owner"}:errors.append(r["risk_id"]+": invalid owner")
    if re.search(r"\b(?:DP|DEC|IS)-", " ".join(r.values())):errors.append(r["risk_id"]+": obsolete reference")
gates=rows("docs/07-assurance/CTO_INVESTMENT_GATE_MATRIX.csv")
if len(gates)!=9:errors.append("expected 9 CTO gates")
phase_schema=json.loads((ROOT/"contracts/assurance/phase-g-cto-review.schema.json").read_text())
phase_validator=Draft202012Validator(phase_schema)
for p in ROOT.glob(".codex/tasks/TASK-*.json"):
    o=json.loads(p.read_text()); rv=o.get("phase_g_review",{})
    for e in phase_validator.iter_errors(rv):errors.append(p.name+": "+e.message)
    if o.get("cto_review_status")!="PASS" or o.get("cto_review_baseline")!="SAR-v3.0-PHASE-G":errors.append(p.name+": CTO metadata drift")
    if set(rv.get("applicable_controls",[]))|set(rv.get("non_applicable_controls",[])) != ids:errors.append(p.name+": control partition incomplete")
status=(ROOT/"docs/06-delivery/CURRENT_STATUS.md").read_text()
road=(ROOT/"docs/06-delivery/PHASE_ROADMAP.md").read_text()
if "ADR-001` a `ADR-058" not in status or "Fases A–G:** concluídas" not in status:errors.append("current status stale")
if "G — CTO Review | CONCLUÍDA" not in road:errors.append("phase roadmap stale")
lock=yaml.safe_load((ROOT/"contracts/operations/lock-and-queue-policy.yaml").read_text())
if lock["broker"]["message_max_bytes"]!=262144 or lock["broker"]["ack"]!="after authoritative commit":errors.append("queue policy drift")
rec=yaml.safe_load((ROOT/"contracts/operations/recovery-objectives.yaml").read_text())
if len(rec.get("classes",[]))!=3:errors.append("recovery classes incomplete")
slo=yaml.safe_load((ROOT/"contracts/operations/slo-sli-catalog.yaml").read_text())
if slo["availability"]["ha_claim_allowed"] is not False:errors.append("HA claim must remain false")
if errors:
 print("CTO REVIEW FAILED")
 for e in errors[:300]:print("-",e)
 sys.exit(1)
print("CTO REVIEW PASS")
print("controls: 15")
print("issues: 870")
print("active risks: 40")
print("gates: 9")
