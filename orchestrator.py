from agents.analyzer import analyze_requirement
from agents.strategist import generate_strategy
from agents.generator import generate_output
from agents.scorer import score_requirement

def run_clarifyqa(requirement: str) -> dict:
    """
    Orchestrates all agents in sequence.
    """
    print("📊 Scorer Agent running...")
    score = score_requirement(requirement)

    print("🔍 Analyzer Agent running...")
    analysis = analyze_requirement(requirement)

    print("🧠 Strategist Agent running...")
    strategy = generate_strategy(requirement, analysis)

    print("⚙️ Generator Agent running...")
    output = generate_output(requirement, strategy)

    return {
        "requirement": requirement,
        "score": score,
        "analysis": analysis,
        "strategy": strategy,
        "output": output
    }