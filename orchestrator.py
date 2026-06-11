from agents.analyzer import analyze_requirement
from agents.strategist import generate_strategy
from agents.generator import generate_output

def run_clarifyqa(requirement: str) -> dict:
    """
    Orchestrates all three agents in sequence.
    Takes a requirement and returns the full ClarifyQA analysis.
    """
    print("🔍 Analyzer Agent running...")
    analysis = analyze_requirement(requirement)

    print("🧠 Strategist Agent running...")
    strategy = generate_strategy(requirement, analysis)

    print("⚙️ Generator Agent running...")
    output = generate_output(requirement, strategy)

    return {
        "requirement": requirement,
        "analysis": analysis,
        "strategy": strategy,
        "output": output
    }