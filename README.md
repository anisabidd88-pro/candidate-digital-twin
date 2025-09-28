# Candidate Digital Twin — MVP (Prototype)

This repository is a lightweight, dependency-free **MVP** that demonstrates the *concept* of an AI-powered
Candidate Digital Twin for recruitment simulation. It is designed so you can run the demo immediately with
only Python (no external packages required). Advanced features (GNNs, Knowledge Graph libs, ML models) are
described and prepared as optional upgrades.

## What’s included
- `demo/` — runnable demo:
  - `run_demo.py` — builds simple digital twins from sample data and simulates performance for roles.
  - `twin.py` — core logic (parsing, knowledge-graph-like co-occurrence, simulation logic).
  - `sample_data.json` — example candidates and interview data.
- `dashboard/` — a minimal static HTML dashboard that reads precomputed results (`results.json`).
- `tests/` — a basic unit test for the demo logic.
- `requirements.txt` — optional advanced libraries for production extensions.
- `LICENSE` — MIT license.

## How to run (minimum, no dependencies)
1. Make sure you have Python 3.8+ installed.
2. Run the demo script:
```bash
python demo/run_demo.py
```
That will print candidate simulation scores for two example roles (Sales, Marketing) and generate `dashboard/results.json`.

3. To view the static dashboard:
```bash
cd dashboard
python -m http.server 8000
# then open http://localhost:8000 in your browser
```

## Advanced options
If you want to add real NLP, Knowledge Graphs, or GNNs, install the optional requirements:
```bash
python -m pip install -r requirements.txt
```
Then follow the comments in `demo/twin.py` to replace heuristic methods with real ML pipelines.

## Notes
- This is a prototype focused on clarity and runnability. It demonstrates the architecture and core ideas:
  - Building a "twin" (feature vector + lightweight skill graph)
  - Simulating role performance using a mix of skill-match and psychometric/interview signals
  - Producing outputs usable by a dashboard

If you want, I can:
- Replace heuristics with a scikit-learn model trained on synthetic data.
- Add a Flask/FastAPI backend and a nicer React dashboard.
- Integrate knowledge-graph persistence (NetworkX / Neo4j) and a GNN (PyTorch Geometric).

Tell me which upgrade you prefer and I will produce updated code (or a new zip).
