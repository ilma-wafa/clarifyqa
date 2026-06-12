import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def review_user_story(requirement: str) -> str:
    """
    Reviews a user story before sprint planning and checks QA readiness.
    """
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-05-01-preview"
    )

    system_prompt = """You are a senior QA Engineer reviewing user stories before sprint planning.
    Review the given requirement and check it against QA readiness criteria.
    
    Return your response in this exact format:
    
    QA REVIEW — USER STORY READINESS:
    
    ✅ User Role Clear: Yes / ❌ No
    [Brief explanation]
    
    ✅ Goal Clear: Yes / ❌ No
    [Brief explanation]
    
    ✅ Business Value Clear: Yes / ❌ No
    [Brief explanation]
    
    ✅ Acceptance Criteria Present: Yes / ❌ No
    [Brief explanation]
    
    ✅ Validation Rules Defined: Yes / ❌ No
    [Brief explanation]
    
    ✅ Edge Cases Mentioned: Yes / ❌ No
    [Brief explanation]
    
    ✅ Dependencies Listed: Yes / ❌ No
    [Brief explanation]
    
    ✅ Story Testable: Yes / ❌ No
    [Brief explanation]
    
    READINESS SCORE: [number] / 8 criteria met
    
    VERDICT: Ready for Sprint / Needs Refinement / Not Ready
    
    QA RECOMMENDATIONS:
    - [Recommendation 1]
    - [Recommendation 2]
    - [Recommendation 3]"""

    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this user story:\n\n{requirement}"}
        ],
        timeout=30
    )

    return response.choices[0].message.content