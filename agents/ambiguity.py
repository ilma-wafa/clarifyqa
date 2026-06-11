import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def detect_ambiguity(requirement: str) -> str:
    """
    Detects vague and ambiguous words in a requirement and explains why they are unclear.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer specializing in requirements clarity.
    Identify all vague, ambiguous, or unclear words and phrases in the requirement.
    
    Common ambiguous words include: fast, simple, secure, user-friendly, proper, valid, 
    quickly, easy, robust, reliable, efficient, appropriate, reasonable, good, nice, better,
    "system should handle", "as needed", "etc", "and so on".
    
    For each ambiguous word or phrase found, explain:
    1. The word/phrase
    2. Why it is ambiguous
    3. What specific detail should replace it
    
    Return your response in this exact format:
    
    AMBIGUOUS WORDS FOUND: [number]
    
    1. "[word/phrase]"
       Why it's unclear: [explanation]
       Should be replaced with: [specific suggestion]
    
    If no ambiguous words are found, return:
    AMBIGUOUS WORDS FOUND: 0
    This requirement has no ambiguous language detected.
    """

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Detect ambiguity in this requirement:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content