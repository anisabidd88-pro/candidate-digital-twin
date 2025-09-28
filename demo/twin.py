"""Lightweight implementation of a 'digital twin' builder and simulator.

This file avoids external dependencies and uses plain Python heuristics to:
- extract skills (from provided lists / resume text)
- build a simple co-occurrence "knowledge graph" (as dicts)
- compute a simulation score per role using skill match + psychometric + interview

Replace heuristics with ML/NLP models when you install advanced requirements.
"""

from typing import Dict, List, Tuple
import re
import math

COMMON_SKILLS = [
    "communication", "negotiation", "crm", "data analysis", "leadership",
    "seo", "content creation", "social media", "analytics", "python",
    "machine learning", "sql", "javascript", "project management", "sales",
    "marketing", "problem solving"
]

def normalize_skill(s: str) -> str:
    return s.strip().lower()

def extract_skills_from_text(text: str, known_skills=COMMON_SKILLS) -> List[str]:
    text_lower = text.lower()
    found = set()
    for ks in known_skills:
        if ks in text_lower:
            found.add(normalize_skill(ks))
    # also look for "Skills:" lines with comma-separated values
    m = re.search(r"skills?:\s*(.+)", re.IGNORECASE)
    if m:
        parts = re.split(r"[,;]", m.group(1))
        for p in parts:
            p = normalize_skill(p)
            if p:
                found.add(p)
    return sorted(found)

def build_skill_graph(skills: List[str]) -> Dict[str, List[str]]:
    # simple co-occurrence graph: each skill connects to all other skills the candidate has
    graph = {}
    for s in skills:
        neighbors = [x for x in skills if x != s]
        graph[s] = neighbors
    return graph

def build_twin(candidate: Dict) -> Dict:
    skills = candidate.get("skills") or extract_skills_from_text(candidate.get("resume_text",""), COMMON_SKILLS)
    graph = build_skill_graph(skills)
    twin = {
        "id": candidate.get("id"),
        "name": candidate.get("name"),
        "skills": skills,
        "skill_graph": graph,
        "psychometric_score": float(candidate.get("psychometric_score", 50)),
        "interview_score": float(candidate.get("interview_score", 50))
    }
    return twin

def score_for_role(twin: Dict, role_profile: Dict) -> float:
    # role_profile: {"id":..., "name":..., "required_skills": [...], "weights": {"skills":0.6, ...}}
    required = [normalize_skill(s) for s in role_profile.get("required_skills",[])]
    candidate_skills = [normalize_skill(s) for s in twin.get("skills",[])]
    # skill match: fraction of required skills present
    if not required:
        skill_match = 0.0
    else:
        matched = sum(1 for r in required if r in candidate_skills)
        skill_match = matched / len(required)
    # psychometric & interview normalized 0..1
    psych = max(0.0, min(1.0, twin.get("psychometric_score",50) / 100.0))
    interview = max(0.0, min(1.0, twin.get("interview_score",50) / 100.0))
    # simple graph-based "team fit" proxy: average degree of required skills inside candidate graph
    graph = twin.get("skill_graph", {})
    if not required:
        team_fit = 0.0
    else:
        degs = []
        for r in required:
            degs.append(len(graph.get(r,[])))
        team_fit = (sum(degs) / (len(degs) * max(1, len(candidate_skills)))) if candidate_skills else 0.0
    # weights
    w = role_profile.get("weights", {"skills":0.6, "psych":0.3, "interview":0.08, "team":0.02})
    score = (
        w.get("skills",0.6)*skill_match +
        w.get("psych",0.3)*psych +
        w.get("interview",0.08)*interview +
        w.get("team",0.02)*team_fit
    )
    # normalize to 0..100
    return round(100.0 * max(0.0, min(1.0, score)), 2)

def simulate_all(candidates: List[Dict], roles: List[Dict]) -> List[Dict]:
    results = []
    for cand in candidates:
        twin = build_twin(cand)
        for role in roles:
            sc = score_for_role(twin, role)
            results.append({
                "candidate_id": twin["id"],
                "candidate_name": twin["name"],
                "role_id": role.get("id"),
                "role_name": role.get("name"),
                "score": sc
            })
    return results
