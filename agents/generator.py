import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

def generate_output(requirement: str, strategy: str) -> str:
    """
    Generates test scenarios and professional bug report template
    based on the requirement and strategy.
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

    system_prompt = """You are a senior QA Engineer specializing in test design.
    Based on the requirement and strategy provided, generate:
    1. Test Scenarios - Positive, negative, edge, boundary, and security scenarios
    2. Bug Report Template - Professional bug report with title, steps to reproduce,
       expected result, actual result, severity, priority, and impact
    
    Be thorough and practical."""

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Requirement:\n{requirement}\n\nStrategy:\n{strategy}"}
        ]
    )

    return response.choices[0].message.content