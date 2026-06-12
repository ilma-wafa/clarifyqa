from agents.analyzer import analyze_requirement
from agents.strategist import generate_strategy
from agents.generator import generate_output
from agents.scorer import score_requirement
from agents.ambiguity import detect_ambiguity
from agents.acceptance import generate_acceptance_criteria
from agents.improver import improve_requirement
from agents.coverage import check_test_coverage
from agents.severity import suggest_severity
from agents.jira import generate_jira_report
from agents.regression import analyze_regression_impact
from agents.qa_review import review_user_story
from concurrent.futures import ThreadPoolExecutor

def run_clarifyqa(requirement: str) -> dict:
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_score = executor.submit(score_requirement, requirement)
        future_ambiguity = executor.submit(detect_ambiguity, requirement)
        future_acceptance = executor.submit(generate_acceptance_criteria, requirement)
        future_improved = executor.submit(improve_requirement, requirement)
        future_analysis = executor.submit(analyze_requirement, requirement)
        future_coverage = executor.submit(check_test_coverage, requirement)
        future_severity = executor.submit(suggest_severity, requirement)
        future_jira = executor.submit(generate_jira_report, requirement)
        future_regression = executor.submit(analyze_regression_impact, requirement)
        future_qa_review = executor.submit(review_user_story, requirement)

        score = future_score.result()
        ambiguity = future_ambiguity.result()
        acceptance = future_acceptance.result()
        improved = future_improved.result()
        analysis = future_analysis.result()
        coverage = future_coverage.result()
        severity = future_severity.result()
        jira = future_jira.result()
        regression = future_regression.result()
        qa_review = future_qa_review.result()

    print("🧠 Strategist Agent running...")
    strategy = generate_strategy(requirement, analysis)

    print("⚙️ Generator Agent running...")
    output = generate_output(requirement, strategy)

    return {
        "requirement": requirement,
        "score": score,
        "ambiguity": ambiguity,
        "acceptance": acceptance,
        "improved": improved,
        "analysis": analysis,
        "coverage": coverage,
        "severity": severity,
        "jira": jira,
        "regression": regression,
        "qa_review": qa_review,
        "strategy": strategy,
        "output": output
    }