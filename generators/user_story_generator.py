def generate_user_story(requirement):
    """
    Converts a validated requirement into a User Story dictionary
    matching sample_inputs/user_story.json
    """

    title = requirement.get(
        "title",
        requirement.get("summary", "Generated User Story")
    )

    description = f"""
    As a user,
    I want {requirement.get('description', '')}
    So that {requirement.get('business_value', 'business value is achieved')}
    """.strip()

    acceptance_criteria = requirement.get("acceptance_criteria", [])

    return {
        "title": title,
        "description": description,
        "acceptance_criteria": acceptance_criteria
    }
