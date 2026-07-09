# AI Agent Performance Monitoring System
**Task 28 — AI & ML Internship Program | AssistanceFloxyz AI**

An operations-intelligence platform that evaluates AI agents the way a business leader evaluates a team of employees — with clear health scores, cost analysis, customer experience tracking, and optimization recommendations.

---

## 1. Business Understanding

### Why AI agent monitoring matters
AssistanceFloxyz AI's agents are deployed across 5,000+ organizations handling customer support, sales, HR, IT helpdesk, knowledge search, and appointment scheduling. Leadership can see conversation *volume*, but not *quality* — whether agents resolve issues quickly, escalate too often, run up token costs, or satisfy customers. Without a standardized framework, businesses can't compare agents, catch underperformers early, or control AI operating costs.

### Business challenges addressed
- No visibility into which agents are worth scaling vs. retraining
- No cost-efficiency lens (token usage vs. business value delivered)
- No standardized way to compare agents across very different domains
- No systematic trigger for retraining, prompt fixes, or workflow redesign

---

## 2. Data Understanding

### Data source
Since no public "AI agent operations" dataset exists, this project **simulates a realistic AI agent environment** (as explicitly recommended in the task brief) — 10,000 synthetic conversation records across 12 AI agents and 6 business domains (Customer Support, Sales Assistance, HR Queries, IT Helpdesk, Internal Knowledge Search, Appointment Scheduling), spanning 8 client industries over a full year.

Each agent was generated with a distinct underlying "skill" and "cost-efficiency" profile, which drives realistic, correlated outcomes across resolution time, escalation rate, satisfaction, token usage, and consistency — so the resulting scores tell a believable business story (some agents are clearly top performers, some are clearly struggling).

### Fields
`conversation_id`, `agent_name`, `agent_domain`, `department_industry`, `query_type`, `conversation_date`, `resolution_time_sec`, `resolution_status`, `escalated`, `customer_satisfaction`, `tokens_used`, `cost_per_conversation_usd`, `response_consistency_score`, `repetitive_response_flag`

### Data quality
- No missing values (synthetic generation).
- Distributions checked via `describe()` in the notebook — resolution time, cost, and satisfaction all fall within realistic bounds.
- Class balance across agents is intentionally uneven (mirrors real-world usage where some agents handle more volume).

---

## 3. Performance Framework

All raw metrics are min-max normalized to 0–100 so scores combine fairly across different units.

| Score | Formula | Rationale |
|---|---|---|
| **Efficiency Score** | Cost (45%) + Tokens (30%) + Resolution Rate (25%) | Measures cost vs. value — a cheap agent that doesn't resolve issues isn't efficient |
| **Customer Experience Score** | Satisfaction (55%) + Escalation, inverted (30%) + Repetition, inverted (15%) | Satisfaction is the primary CX signal; escalations and repetitive answers are direct friction points |
| **Reliability Score** | Consistency (45%) + Resolution Rate (30%) + Escalation, inverted (25%) | Reliability is about *consistent*, correct outcomes, not just one good conversation |
| **Agent Health Score** | Efficiency (30%) + CX (40%) + Reliability (30%) | CX is weighted highest since customer impact is leadership's top strategic concern |

### Performance status thresholds
- **Top Performer**: Health Score ≥ 85 → Recommend expansion
- **Solid Performer**: 70–84 → Maintain, minor tuning
- **Needs Improvement**: 55–69 → Targeted retraining
- **Underperforming**: < 55 → Retrain or replace

---

## 4. Insights & Recommendations

(See `reports/agent_benchmark_report.csv` for full numbers.)

- **Top performers**: SupportBot-v4, SchedulerBot, KnowledgeFinder-X — low cost, high satisfaction, low escalation. Recommended for expanded deployment.
- **Underperformers**: IT-Legacy-Bot, ITHelpDesk-AI, SalesAssist-Lite — high escalation and token cost drag down their Health Score. Recommended for retraining or retirement.
- **Domain-level pattern**: IT Helpdesk agents score lowest as a category — suggests a systemic workflow issue in that domain, not just an isolated agent problem.
- **Cost optimization opportunity**: Several mid-tier agents (SupportBot-v3, KnowledgeFinder-Lite) have good satisfaction but poor efficiency — prompt/token optimization could lift them into "Solid Performer" without retraining.

---

## 5. Future Roadmap

- **Real-time monitoring**: Stream conversation events into the scoring pipeline instead of batch CSV processing.
- **Drift detection**: Track Health Score over rolling windows to catch performance degradation early (statistical control charts / CUSUM).
- **AI governance integration**: Log every scoring run with model version, prompt version, and dataset snapshot for auditability.

---

## 6. Project Structure

```
TASK_28_AI_AGENT_PERFORMANCE_MONITORING_SYSTEM/
├── data/
│   └── ai_agent_performance_dataset.csv       # 10,000-row simulated dataset
├── notebooks/
│   ├── scoring_pipeline.py                    # Plain-python version of the pipeline
│   └── 01_agent_scoring_pipeline.ipynb        # Full annotated notebook (run this)
├── reports/
│   ├── agent_benchmark_report.csv             # Final scored + ranked output
│   └── health_score_chart.png                 # Quick static chart
├── app/
│   └── dashboard.py                            # Streamlit dashboard
├── dashboards/                                  # (reserved for Power BI / Tableau exports)
├── presentation/                                # (reserved for slide deck)
├── requirements.txt
└── README.md
```

## 7. How to Run

```bash
pip install -r requirements.txt

# 1. Regenerate scores (optional — already committed in reports/)
cd notebooks && jupyter nbconvert --to notebook --execute --inplace 01_agent_scoring_pipeline.ipynb

# 2. Launch the dashboard
cd ../app && streamlit run dashboard.py
```

## 8. Technology Stack
Python, Pandas, NumPy, Scikit-learn (normalization patterns), Matplotlib, Plotly, Streamlit, Jupyter.
