"""Create deterministic, synthetic source-style records for this analysis."""
from __future__ import annotations
import csv
import random
from datetime import date, timedelta
from pathlib import Path

R = random.Random(418)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BU = ["Collaboration", "Security", "Networking", "Customer Experience", "Finance", "Operations"]
DOMAINS = ["Knowledge assistant", "Forecasting", "Workflow automation", "Support copilot", "Document intelligence"]
OWNERS = ["Data & AI", "Risk", "Security", "Business Operations", "Product"]
BASE = date(2025, 1, 1)

def write(name, cols, rows):
    with (DATA / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

def main():
    initiatives=[]
    for i in range(1, 181):
        bu=BU[(i-1)%len(BU)]; domain=DOMAINS[(i*3)%len(DOMAINS)]
        status="Scaled" if i%7 in (0,1) else ("Pilot" if i%7 in (2,3,4) else "Discovery")
        initiatives.append(dict(initiative_id=f"AI-{i:03}", business_unit=bu, use_case=domain,
          lifecycle=status, owner=OWNERS[i%len(OWNERS)], launch_date=(BASE+timedelta(days=(i*11)%530)).isoformat(),
          estimated_annual_value=round(65000+(i*17391)%800000,2), regulated_data="Yes" if i%4==0 else "No"))
    write("ai_initiative_registry.csv", list(initiatives[0]), initiatives)
    controls=[]
    control_names=["Use-case inventory", "Data lineage review", "Privacy assessment", "Security review", "Human oversight", "Model monitoring"]
    for item in initiatives:
        for j, control in enumerate(control_names):
            passed=(int(item['initiative_id'][-3:])*7+j*11)%17 not in (0,1)
            controls.append(dict(control_id=f"{item['initiative_id']}-C{j+1}", initiative_id=item['initiative_id'], control_name=control,
              required="Yes", status="Pass" if passed else "Gap", evidence_date=(BASE+timedelta(days=(j*31+int(item['initiative_id'][-3:])*4)%560)).isoformat()))
    write("control_assessments.csv", list(controls[0]), controls)
    exceptions=[]
    severities=["Low","Medium","High","Critical"]
    for i in range(1, 421):
        opened=BASE+timedelta(days=(i*9)%570); age=3+(i*13)%94; status="Open" if i%5 else "Resolved"
        exceptions.append(dict(exception_id=f"EX-{i:04}", initiative_id=f"AI-{1+(i*5)%180:03}", severity=severities[i%4],
          category=["Lineage","Privacy","Security","Monitoring","Oversight"][i%5], opened_date=opened.isoformat(),
          age_days=age if status=="Open" else 0, status=status, owner=OWNERS[i%len(OWNERS)]))
    write("governance_exceptions.csv", list(exceptions[0]), exceptions)
    adoption=[]
    for i in range(1, 721):
        initiative=f"AI-{1+(i*7)%180:03}"; week=BASE+timedelta(days=(i%52)*7)
        eligible=100+(i*19)%2600
        active=min(65+(i*29)%1800, int(eligible*.94))
        adoption.append(dict(record_id=f"AD-{i:04}", initiative_id=initiative, week_start=week.isoformat(),
          eligible_users=eligible, active_users=active, workflow_runs=210+(i*41)%10000,
          business_unit=BU[(i*7)%len(BU)]))
    write("adoption_telemetry.csv", list(adoption[0]), adoption)
    value=[]
    for i in range(1, 301):
        init=f"AI-{1+(i*11)%180:03}"; planned=40000+(i*9137)%600000; realized=planned*(0.38+((i*17)%60)/100)
        value.append(dict(value_record_id=f"VR-{i:04}", initiative_id=init, quarter=["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1"][i%5],
          planned_value=round(planned,2), realized_value=round(realized,2), value_type=["Cost avoidance","Revenue enablement","Cycle-time reduction"][i%3], confidence=["Low","Medium","High"][i%3]))
    write("value_realization.csv", list(value[0]), value)

if __name__ == "__main__": main()
