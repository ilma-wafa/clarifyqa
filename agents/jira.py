import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_jira_report(requirement: str) -> str:
    """
    Generates a bug report in Jira-ready format.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer who writes professional Jira bug reports.
    Based on the requirement, generate a sample Jira bug report for the most critical
    potential bug in this feature.
    
    Return your response in this exact format:
    
    ============================================
    JIRA BUG REPORT
    ============================================
    
    Project: [Project name based on requirement]
    Issue Type: Bug
    
    Summary: [One line bug title]
    
    Environment:
    - Application Version: [version]
    - Platform: Web / Mobile
    - Browser: Chrome / Firefox / Safari
    - OS: Windows / macOS / Linux
    - Network: Stable
    
    Labels: [relevant labels e.g. security, authentication, critical]
    Component: [component name]
    Fix Version: [next release]
    
    Priority: P1 / P2 / P3
    Severity: Critical / High / Medium / Low
    
    Assignee: [Developer name - use placeholder]
    Reporter: QA Engineer
    
    Description:
    [Detailed description of the bug]
    
    Preconditions:
    - [precondition 1]
    - [precondition 2]
    
    Steps to Reproduce:
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]
    4. [Step 4]
    
    Expected Result:
    [What should happen]
    
    Actual Result:
    [What actually happens]
    
    Impact:
    [Business and user impact]
    
    Attachments:
    - Screenshots
    - Error logs
    - Network traces
    
    ============================================"""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate a Jira bug report for:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content