import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def score_requirement(requirement: str) -> str:
    """
    Scores a requirement out of 100 and explains deductions.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer who scores software requirements.
    Score the requirement out of 100 based on these criteria:
    
    - Acceptance Criteria present (20 points)
    - Validation rules defined (20 points)
    - Error handling mentioned (20 points)
    - Security behavior defined (20 points)
    - Edge cases covered (20 points)
    
    Return your response in this exact format:
    
    SCORE: [number]/100 — [one line verdict]
    
    DEDUCTIONS:
    - [criterion]: [points deducted] — [reason]
    
    SUMMARY:
    [2-3 sentence summary of what needs to be improved]
    """

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Score this requirement:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content