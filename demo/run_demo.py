"""Run a short demo of the digital twin prototype.

Produces:
- printed table of scores
- dashboard/results.json used by the static dashboard
"""

import json, os
from twin import build_twin, simulate_all

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "sample_data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

candidates = data.get("candidates", [])

# Define two example role profiles
roles = [
    {
        "id": "r_sales",
        "name": "Sales (B2B SaaS)",
        "required_skills": ["communication", "negotiation", "crm", "sales"],
        "weights": {"skills":0.6, "psych":0.25, "interview":0.12, "team":0.03}
    },
    {
        "id": "r_marketing",
        "name": "Marketing (Digital)",
        "required_skills": ["seo", "content creation", "analytics", "social media"],
        "weights": {"skills":0.6, "psych":0.25, "interview":0.12, "team":0.03}
    }
]

results = simulate_all(candidates, roles)

# Pretty-print results
print("Candidate performance simulation (scores 0..100):\n")
for r in results:
    print(f"{r['candidate_name']:20} | {r['role_name']:25} | Score: {r['score']}")
# Save results for dashboard
dashboard_dir = os.path.join(HERE, "..", "dashboard")
os.makedirs(dashboard_dir, exist_ok=True)
with open(os.path.join(dashboard_dir, "results.json"), "w", encoding="utf-8") as f:
    json.dump({"results": results}, f, indent=2, ensure_ascii=False)
print("\nWrote dashboard/results.json — open dashboard/index.html with a static server to view UI.")
