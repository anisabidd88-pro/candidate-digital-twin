from demo.twin import build_twin, score_for_role

def test_score_basic():
    candidate = {
        "id": "t1",
        "name": "Test Candidate",
        "skills": ["communication", "crm", "negotiation"],
        "psychometric_score": 80,
        "interview_score": 70
    }
    twin = build_twin(candidate)
    role = {"id":"r","name":"Sales","required_skills":["communication","negotiation","crm"], "weights":{"skills":0.6,"psych":0.3,"interview":0.09,"team":0.01}}
    s = score_for_role(twin, role)
    assert s > 75  # with good skill match and psych/interview, score should be high
