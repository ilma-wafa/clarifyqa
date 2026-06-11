import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

def generate_strategy(requirement: str, analysis: str) -> str:
    """
    Generates clarification questions and risk-based test plan
    based on the requirement and its analysis.
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

    system_prompt = """You are a senior QA Engineer specializing in test strategy.
    Based on the requirement and its analysis, provide:
    1. Clarification Questions - Smart questions to ask the BA, PO, or developer
    2. Gap Detection - Missing details like validation rules, error handling, edge cases
    3. Risk-Based Test Plan - Rank testing areas as High, Medium, or Low risk
    
    Be specific and practical."""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Requirement:\n{requirement}\n\nAnalysis:\n{analysis}"}
        ]
    )

    return response.choices[0].message.content