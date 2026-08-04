"""Reproduce portfolio KPIs, executive extracts, and rendered evidence."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=ROOT/'analysis'/'outputs'; IMG=ROOT/'docs'/'images'
OUT.mkdir(parents=True, exist_ok=True); IMG.mkdir(parents=True, exist_ok=True)
initiatives=pd.read_csv(DATA/'ai_initiative_registry.csv'); controls=pd.read_csv(DATA/'control_assessments.csv'); exc=pd.read_csv(DATA/'governance_exceptions.csv'); adopt=pd.read_csv(DATA/'adoption_telemetry.csv'); value=pd.read_csv(DATA/'value_realization.csv')
coverage=controls.groupby('initiative_id').status.apply(lambda x:(x=='Pass').mean()).rename('control_coverage')
portfolio=initiatives.join(coverage,on='initiative_id')
portfolio['control_coverage']=portfolio.control_coverage.fillna(0)
value_summary=value.groupby('initiative_id')[['planned_value','realized_value']].sum().assign(value_realization=lambda x:x.realized_value/x.planned_value)
portfolio=portfolio.join(value_summary,on='initiative_id')
portfolio.to_csv(OUT/'portfolio_health.csv',index=False)
open_exc=exc[exc.status=='Open']; aged=open_exc[open_exc.age_days>45]
kpis=pd.DataFrame([{'initiatives':len(initiatives),'governance_coverage_pct':round((portfolio.control_coverage>=.83).mean()*100,1),'open_exceptions':len(open_exc),'exceptions_over_45_days':len(aged),'value_realization_pct':round(value.realized_value.sum()/value.planned_value.sum()*100,1),'telemetry_rows':len(adopt)}])
kpis.to_csv(OUT/'executive_kpis.csv',index=False)
bu=portfolio.groupby('business_unit').agg(initiatives=('initiative_id','count'),control_coverage=('control_coverage','mean'),planned_value=('planned_value','sum'),realized_value=('realized_value','sum')).reset_index(); bu['value_realization']=bu.realized_value/bu.planned_value
bu.to_csv(OUT/'business_unit_scorecard.csv',index=False)
action=portfolio.merge(open_exc.groupby('initiative_id').agg(open_exceptions=('exception_id','count'),max_age_days=('age_days','max')),on='initiative_id',how='left').fillna({'open_exceptions':0,'max_age_days':0})
action['priority_score']=(1-action.control_coverage)*100+action.open_exceptions*5+action.max_age_days*.3
action.sort_values('priority_score',ascending=False).head(15).to_csv(OUT/'priority_remediation_queue.csv',index=False)
plt.style.use('seaborn-v0_8-whitegrid'); fig,ax=plt.subplots(figsize=(10,5)); b=ax.bar(bu.business_unit,bu.control_coverage*100,color='#0b5cab'); ax.bar_label(b,fmt='%.0f%%',padding=3); ax.set_ylim(0,110); ax.set_ylabel('Required control pass rate'); ax.set_title('Governance coverage by business unit'); plt.xticks(rotation=18,ha='right'); plt.tight_layout(); plt.savefig(IMG/'governance_coverage_by_unit.png',dpi=180); plt.close()
sev=open_exc.groupby('severity').size().reindex(['Low','Medium','High','Critical']); fig,ax=plt.subplots(figsize=(8,5)); b=ax.bar(sev.index,sev.values,color=['#8aa3bd','#e9b949','#e67e22','#c0392b']); ax.bar_label(b); ax.set_ylabel('Open exceptions'); ax.set_title('Open governance exceptions by severity'); plt.tight_layout(); plt.savefig(IMG/'open_exceptions_by_severity.png',dpi=180); plt.close()
print(kpis.to_string(index=False)); print('Wrote', OUT, 'and', IMG)
