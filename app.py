import streamlit as st
import json
from main import run_quality_gate

st.set_page_config(
    page_title="Requirements Quality Gate",
    page_icon="✅",
    layout="centered"
)

st.title("🧠 Requirements Quality Gate AI Agent")
st.caption("AI-powered governance for requirement quality")

st.divider()

# -----------------------------
# Input Section
# -----------------------------
st.subheader("📌 Requirement Details")

req_id = st.text_input("Requirement ID", value="FR-LOGIN-01")
title = st.text_input("Title", value="Secure User Login")

description = st.text_area(
    "User Story / Requirement Description",
    height=120,
    placeholder="As a user, I want to..."
)

st.subheader("📋 Acceptance Criteria")

auto_generate = st.checkbox("Auto-generate acceptance criteria using AI", value=True)

acceptance_criteria = []
if not auto_generate:
    ac_text = st.text_area(
        "Enter Acceptance Criteria (one per line)",
        height=120,
        placeholder="Given ..., when ..., then ..."
    )
    acceptance_criteria = [
        line.strip()
        for line in ac_text.split("\n")
        if line.strip()
    ]

st.subheader("⚙️ Non-Functional Requirements (NFRs)")

nfr_options = [
    "Security",
    "Performance",
    "Usability",
    "Availability"
]

selected_nfrs = st.multiselect(
    "Select applicable NFRs",
    nfr_options
)

formatted_nfrs = [f"{nfr}" for nfr in selected_nfrs]

st.divider()

# -----------------------------
# Run Gate
# -----------------------------
if st.button("🚦 Run Requirements Quality Gate", type="primary"):

    if not description.strip():
        st.error("Requirement description is mandatory.")
    else:
        req_payload = {
            "id": req_id,
            "title": title,
            "description": description,
            "acceptance_criteria": [] if auto_generate else acceptance_criteria,
            "nfrs": formatted_nfrs
        }

        with st.spinner("Running AI quality checks..."):
            result = run_quality_gate(req_payload)

        st.divider()

        # -----------------------------
        # Results
        # -----------------------------
        decision = result["decision"]
        score = result["total_score"]

        if decision == "PASS":
            st.success(f"✅ QUALITY GATE PASSED — Score: {score}/100")
        else:
            st.error(f"❌ QUALITY GATE FAILED — Score: {score}/100")

        st.subheader("📊 Score Breakdown")
        st.json(result["scores"])

        st.subheader("📝 AI Feedback")

        feedback = result["feedback"]

        if feedback["clarity_issues"]:
            st.warning("🔍 Clarity Issues")
            for issue in feedback["clarity_issues"]:
                st.write(f"- {issue}")

        if feedback["missing_items"]:
            st.warning("📌 Missing Items")
            for item in feedback["missing_items"]:
                st.write(f"- {item}")

        if feedback["non_testable"]:
            st.warning("🧪 Non-testable Acceptance Criteria")
            for item in feedback["non_testable"]:
                st.write(f"- {item}")

        if feedback["missing_nfrs"]:
            st.warning("⚠️ Missing NFR Coverage")
            for nfr in feedback["missing_nfrs"]:
                st.write(f"- {nfr}")

        st.subheader("📦 Raw JSON Output")
        st.json(result)
