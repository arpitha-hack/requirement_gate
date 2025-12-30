import os
from dotenv import load_dotenv

from generators.user_story_generator import generate_user_story
from azure_devops_client import AzureDevOpsClient

load_dotenv()


def handle_post_gate_actions(gate_result, requirement):
    """
    Executes actions after requirement passes the quality gate
    """

    if not gate_result.get("passed"):
        return {
            "status": "skipped",
            "reason": "Quality gate failed"
        }

    azdo_org = os.getenv("AZDO_ORG")
    azdo_project = os.getenv("AZDO_PROJECT")
    azdo_pat = os.getenv("AZDO_PAT")

    if not all([azdo_org, azdo_project, azdo_pat]):
        return {
            "status": "skipped",
            "reason": "Azure DevOps environment variables not set"
        }

    user_story = generate_user_story(requirement)

    client = AzureDevOpsClient(
        organization=azdo_org,
        project=azdo_project,
        pat=azdo_pat
    )

    created_item = client.create_user_story(user_story)

    return {
        "status": "created",
        "work_item_id": created_item.get("id"),
        "url": created_item["_links"]["html"]["href"]
    }

