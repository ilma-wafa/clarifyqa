import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def improve_requirement(requirement: str) -> str:
    """
    Shows the original requirement and an improved version side by side.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior Business Analyst and QA Engineer.
    Improve the given requirement by making it clear, complete, and testable.
    
    Return your response in this exact format:
    
    BEFORE (Original):
    "[original requirement as given]"
    
    ISSUES FOUND:
    - [issue 1]
    - [issue 2]
    - [issue 3]
    
    AFTER (Improved):
    "[rewritten requirement that is specific, measurable, and testable]"
    
    IMPROVEMENTS MADE:
    - [improvement 1]
    - [improvement 2]
    - [improvement 3]
    
    Make the improved version detailed, specific, and professional.
    It should include validation rules, security behavior, and edge case handling."""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Improve this requirement:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content