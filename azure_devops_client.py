import base64
import requests


class AzureDevOpsClient:
    def __init__(self, organization: str, project: str, pat: str):
        # 🔹 Normalize organization WITHOUT changing .env
        if organization.startswith("http"):
            organization = (
                organization.rstrip("/")
                .replace("https://", "")
                .replace(".visualstudio.com", "")
            )

        self.base_url = f"https://dev.azure.com/{organization}/{project}"

        auth = base64.b64encode(f":{pat}".encode()).decode()

        self.headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json-patch+json"
        }

    def create_user_story(self, user_story: dict):
        url = (
            f"{self.base_url}"
            "/_apis/wit/workitems/$User%20Story"
            "?api-version=7.0"
        )

        acceptance_criteria_html = "<br>".join(
            user_story.get("acceptance_criteria", [])
        )

        payload = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": user_story["title"]
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": user_story.get("description", "")
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
                "value": acceptance_criteria_html
            }
        ]

        response = requests.post(url, headers=self.headers, json=payload)

        if not response.ok:
            print("Azure DevOps error:", response.text)

        response.raise_for_status()
        return response.json()
