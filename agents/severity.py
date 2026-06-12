import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def suggest_severity(requirement: str) -> str:
    """
    Suggests bug severity and priority based on the requirement.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer specializing in defect management.
    Based on the requirement, identify the top potential bugs and suggest severity and priority.
    
    Return your response in this exact format:
    
    POTENTIAL BUG ANALYSIS:
    
    Bug 1: [Bug title]
    Severity: Critical / High / Medium / Low
    Priority: P1 / P2 / P3
    Reason: [Why this severity and priority]
    
    Bug 2: [Bug title]
    Severity: Critical / High / Medium / Low
    Priority: P1 / P2 / P3
    Reason: [Why this severity and priority]
    
    [Continue for 4-6 bugs]
    
    SEVERITY GUIDE USED:
    Critical: System crash, data loss, security breach
    High: Major feature broken, significant impact on users
    Medium: Feature partially works, workaround available
    Low: Minor issue, cosmetic, no functional impact
    
    PRIORITY GUIDE USED:
    P1: Fix immediately
    P2: Fix in next release
    P3: Fix when time permits"""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Suggest bug severity and priority for:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content