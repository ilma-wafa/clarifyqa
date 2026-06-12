import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def analyze_regression_impact(requirement: str) -> str:
    """
    Analyzes which existing areas should be retested if this feature changes.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer specializing in regression testing.
    Based on the requirement, identify which existing system areas would be impacted
    if this feature is implemented or changed.
    
    Return your response in this exact format:
    
    REGRESSION IMPACT ANALYSIS:
    
    Primary Impact Areas (Must Retest):
    1. [Area name] — [Why it is affected]
    2. [Area name] — [Why it is affected]
    3. [Area name] — [Why it is affected]
    
    Secondary Impact Areas (Should Retest):
    1. [Area name] — [Why it might be affected]
    2. [Area name] — [Why it might be affected]
    
    Low Risk Areas (Optional Retest):
    1. [Area name] — [Brief reason]
    
    REGRESSION TEST PRIORITY:
    Critical: [list areas]
    High: [list areas]
    Medium: [list areas]
    
    RECOMMENDATION:
    [2-3 sentences on regression testing approach for this feature]"""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze regression impact for:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content