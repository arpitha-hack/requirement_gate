import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        if not api_key or not endpoint:
            raise RuntimeError(
                "Azure OpenAI config missing. "
                "Ensure AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are set."
            )

        _client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
    return _client


def call_llm(system_prompt: str, user_prompt: str) -> str:
    client = get_client()

    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment_name:
        raise RuntimeError("AZURE_OPENAI_DEPLOYMENT not set")

    response = client.chat.completions.create(
        model=deployment_name,  # Azure uses deployment name
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        # temperature=0.2
    )

    return response.choices[0].message.content
