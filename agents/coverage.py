import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def check_test_coverage(requirement: str) -> str:
    """
    Analyzes test coverage completeness for a requirement.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer analyzing test coverage.
    Based on the requirement, evaluate the test coverage status.
    
    Return your response in this exact format:
    
    TEST COVERAGE CHECKLIST:
    
    ✅ Positive Testing: Covered
    [Brief explanation of what is covered]
    
    ✅ Negative Testing: Covered
    [Brief explanation]
    
    ⚠️ Boundary Testing: Partially Covered
    [Brief explanation of what is missing]
    
    ❌ Security Testing: Missing
    [Brief explanation of what needs to be added]
    
    ❌ Regression Testing: Missing
    [Brief explanation]
    
    ⚠️ Usability Testing: Partially Covered
    [Brief explanation]
    
    ❌ Performance Testing: Missing
    [Brief explanation]
    
    COVERAGE SUMMARY:
    Covered: [number] / 7
    Missing: [list missing areas]
    Recommendation: [one sentence on what to prioritize]
    
    Use ✅ for Covered, ⚠️ for Partially Covered, and ❌ for Missing."""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Check test coverage for:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content