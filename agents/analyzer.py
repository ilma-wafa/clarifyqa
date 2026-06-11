import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

def analyze_requirement(requirement: str) -> str:
    """
    Analyzes a software requirement for clarity, completeness, and testability.
    """
    endpoint = os.getenv("AZURE_ENDPOINT")
    deployment = os.getenv("DEPLOYMENT_NAME")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer specializing in requirements analysis.
    Analyze the given requirement and evaluate:
    1. Clarity - Is it clear and unambiguous?
    2. Completeness - Does it have all necessary details?
    3. Testability - Can it be tested?
    
    Provide a structured analysis with findings for each criterion.
    Be specific about what is missing or unclear."""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this requirement:\n\n{requirement}"}
        ]
    )

    return response.choices[0].message.content