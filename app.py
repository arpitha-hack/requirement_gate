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

req_id = st.text_input("Requirement ID", placeholder="FR-LOGIN-01")
title = st.text_input("Title", placeholder="Secure User Login")

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

# formatted_nfrs = [f"{nfr}" for nfr in selected_nfrs]
nfr_details = []

for nfr in selected_nfrs:
    st.markdown(f"**{nfr} Details**")

    if nfr == "Performance":
        response_time = st.text_input(
            "Max Response Time",
            placeholder="e.g., ≤ 2 seconds"
        )
        throughput = st.text_input(
            "Throughput (optional)",
            placeholder="e.g., 100 requests/second"
        )

        detail = f"Performance: Response time {response_time}"
        if throughput:
            detail += f", Throughput {throughput}"

        nfr_details.append(detail)

    elif nfr == "Security":
        auth = st.text_input(
            "Authentication Requirement",
            placeholder="e.g., OAuth2, MFA"
        )
        encryption = st.text_input(
            "Encryption Requirement",
            placeholder="e.g., AES-256, HTTPS"
        )

        detail = f"Security: Auth={auth}, Encryption={encryption}"
        nfr_details.append(detail)

    elif nfr == "Usability":
        usability = st.text_input(
            "Usability Constraint",
            placeholder="e.g., Error messages understandable by non-technical users"
        )

        detail = f"Usability: {usability}"
        nfr_details.append(detail)

    elif nfr == "Availability":
        sla = st.text_input(
            "Availability SLA",
            placeholder="e.g., 99.9% uptime"
        )

        detail = f"Availability: SLA {sla}"
        nfr_details.append(detail)
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
            "nfrs": nfr_details
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
