import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_acceptance_criteria(requirement: str) -> str:
    """
    Converts a vague requirement into proper acceptance criteria.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior Business Analyst and QA Engineer.
    Convert the given requirement into clear, testable acceptance criteria.
    
    Use the Given/When/Then format where appropriate.
    Cover positive, negative, and edge case scenarios.
    
    Return your response in this exact format:
    
    ACCEPTANCE CRITERIA:
    
    AC-001: [criterion]
    Given: [precondition]
    When: [action]
    Then: [expected result]
    
    AC-002: [criterion]
    Given: [precondition]
    When: [action]
    Then: [expected result]
    
    Continue for all relevant criteria.
    
    Aim for 5-8 acceptance criteria that cover the core functionality,
    error handling, security, and edge cases."""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate acceptance criteria for:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content