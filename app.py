# # import streamlit as st
# # import json
# # from main import run_quality_gate

# # st.set_page_config(
# #     page_title="Requirements Quality Gate",
# #     page_icon="✅",
# #     layout="centered"
# # )

# # st.title("🧠 Requirements Quality Gate AI Agent")
# # st.caption("AI-powered governance for requirement quality")

# # st.divider()

# # # -----------------------------
# # # Input Section
# # # -----------------------------
# # st.subheader("📌 Requirement Details")

# # req_id = st.text_input("Requirement ID", placeholder="FR-LOGIN-01")
# # title = st.text_input("Title", placeholder="Secure User Login")

# # description = st.text_area(
# #     "User Story / Requirement Description",
# #     height=120,
# #     placeholder="As a user, I want to..."
# # )

# # st.subheader("📋 Acceptance Criteria")

# # auto_generate = st.checkbox("Auto-generate acceptance criteria using AI", value=True)

# # acceptance_criteria = []
# # if not auto_generate:
# #     ac_text = st.text_area(
# #         "Enter Acceptance Criteria (one per line)",
# #         height=120,
# #         placeholder="Given ..., when ..., then ..."
# #     )
# #     acceptance_criteria = [
# #         line.strip()
# #         for line in ac_text.split("\n")
# #         if line.strip()
# #     ]

# # st.subheader("⚙️ Non-Functional Requirements (NFRs)")

# # nfr_options = [
# #     "Security",
# #     "Performance",
# #     "Usability",
# #     "Availability"
# # ]

# # selected_nfrs = st.multiselect(
# #     "Select applicable NFRs",
# #     nfr_options
# # )

# # # formatted_nfrs = [f"{nfr}" for nfr in selected_nfrs]
# # nfr_details = []

# # for nfr in selected_nfrs:
# #     st.markdown(f"**{nfr} Details**")

# #     if nfr == "Performance":
# #         response_time = st.text_input(
# #             "Max Response Time",
# #             placeholder="e.g., ≤ 2 seconds"
# #         )
# #         throughput = st.text_input(
# #             "Throughput (optional)",
# #             placeholder="e.g., 100 requests/second"
# #         )

# #         detail = f"Performance: Response time {response_time}"
# #         if throughput:
# #             detail += f", Throughput {throughput}"

# #         nfr_details.append(detail)

# #     elif nfr == "Security":
# #         auth = st.text_input(
# #             "Authentication Requirement",
# #             placeholder="e.g., OAuth2, MFA"
# #         )
# #         encryption = st.text_input(
# #             "Encryption Requirement",
# #             placeholder="e.g., AES-256, HTTPS"
# #         )

# #         detail = f"Security: Auth={auth}, Encryption={encryption}"
# #         nfr_details.append(detail)

# #     elif nfr == "Usability":
# #         usability = st.text_input(
# #             "Usability Constraint",
# #             placeholder="e.g., Error messages understandable by non-technical users"
# #         )

# #         detail = f"Usability: {usability}"
# #         nfr_details.append(detail)

# #     elif nfr == "Availability":
# #         sla = st.text_input(
# #             "Availability SLA",
# #             placeholder="e.g., 99.9% uptime"
# #         )

# #         detail = f"Availability: SLA {sla}"
# #         nfr_details.append(detail)
# # st.divider()

# # # -----------------------------
# # # Run Gate
# # # -----------------------------
# # if st.button("🚦 Run Requirements Quality Gate", type="primary"):

# #     if not description.strip():
# #         st.error("Requirement description is mandatory.")
# #     else:
# #         req_payload = {
# #             "id": req_id,
# #             "title": title,
# #             "description": description,
# #             "acceptance_criteria": [] if auto_generate else acceptance_criteria,
# #             "nfrs": nfr_details
# #         }

# #         with st.spinner("Running AI quality checks..."):
# #             result = run_quality_gate(req_payload)

# #         st.divider()

# #         # -----------------------------
# #         # Results
# #         # -----------------------------
# #         decision = result["decision"]
# #         score = result["total_score"]

# #         if decision == "PASS":
# #             st.success(f"✅ QUALITY GATE PASSED — Score: {score}/100")
# #         else:
# #             st.error(f"❌ QUALITY GATE FAILED — Score: {score}/100")

# #         st.subheader("📊 Score Breakdown")
# #         st.json(result["scores"])

# #         st.subheader("📝 AI Feedback")

# #         feedback = result["feedback"]

# #         if feedback["clarity_issues"]:
# #             st.warning("🔍 Clarity Issues")
# #             for issue in feedback["clarity_issues"]:
# #                 st.write(f"- {issue}")

# #         if feedback["missing_items"]:
# #             st.warning("📌 Missing Items")
# #             for item in feedback["missing_items"]:
# #                 st.write(f"- {item}")

# #         if feedback["non_testable"]:
# #             st.warning("🧪 Non-testable Acceptance Criteria")
# #             for item in feedback["non_testable"]:
# #                 st.write(f"- {item}")

# #         if feedback["missing_nfrs"]:
# #             st.warning("⚠️ Missing NFR Coverage")
# #             for nfr in feedback["missing_nfrs"]:
# #                 st.write(f"- {nfr}")

# #         st.subheader("📦 Raw JSON Output")
# #         st.json(result)

# import streamlit as st
# from main import run_quality_gate
# from utils.file_parser import extract_text_from_file
# from extractors.requirement_extractor import extract_requirements
# from utils.json_utils import extract_json_object
# import hashlib

# def file_hash(uploaded_file):
#     return hashlib.md5(uploaded_file.getvalue()).hexdigest()
# def hard_reset_form():
#     for key in [
#         "req_id",
#         "title",
#         "description",
#         "acceptance_criteria",
#         "nfrs",
#     ]:
#         st.session_state.pop(key, None)

# def reset_requirement_form(data: dict):
#     st.session_state.req_id = data.get("id", "")
#     st.session_state.title = data.get("title", "")
#     st.session_state.description = data.get("description", "")
#     st.session_state.acceptance_criteria = "\n".join(data.get("acceptance_criteria", []))
#     st.session_state.nfrs = "\n".join(data.get("nfrs", []))

# st.set_page_config(page_title="Requirements Quality Gate", layout="centered")
# if "last_file_hash" not in st.session_state:
#     st.session_state["last_file_hash"] = None
# for key, default in {
#     "req_id": "FR-01",
#     "title": "",
#     "description": "",
#     "acceptance_criteria": "",
#     "nfrs": "",
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# st.title("🧠 Requirements Quality Gate AI")
# st.caption("Manual input or AI-extracted from uploaded requirements")

# st.divider()

# # -------------------------
# # Upload Section
# # -------------------------
# st.subheader("📤 Upload Requirements File (Optional)")

# uploaded_file = st.file_uploader(
#     "Upload TXT, DOCX, or PDF",
#     type=["txt", "docx", "pdf"]
# )

# extracted_data = {}

# if uploaded_file:
#     current_hash = file_hash(uploaded_file)

#     if st.session_state["last_file_hash"] != current_hash:
#         st.session_state["last_file_hash"] = current_hash

#         with st.spinner("Extracting requirements using AI..."):
#             raw_text = extract_text_from_file(uploaded_file)
#             raw_json = extract_requirements(raw_text)
#             extracted_data = extract_json_object(raw_json)

#             hard_reset_form()
#             reset_requirement_form(extracted_data)

#         st.success("Requirements extracted successfully!")
#         st.json(extracted_data)


# st.divider()

# # -------------------------
# # Editable Requirement Form
# # -------------------------
# st.subheader("✏️ Requirement Details")

# req_id = st.text_input(
#     "Requirement ID",
#     key="req_id"
# )

# title = st.text_input(
#     "Title",
#     key="title"
# )

# description = st.text_area(
#     "Description / User Story",
#     key="description",
#     height=120
# )

# st.subheader("📋 Acceptance Criteria")

# ac_text = st.text_area(
#     "Acceptance Criteria (one per line)",
#     key="acceptance_criteria",
#     height=120
# )

# acceptance_criteria = [
#     line.strip()
#     for line in ac_text.split("\n")
#     if line.strip()
# ]

# st.subheader("⚙️ Non-Functional Requirements (NFRs)")

# nfr_text = st.text_area(
#     "NFRs (one per line)",
#     key="nfrs",
#     height=120
# )

# nfrs = [
#     line.strip()
#     for line in nfr_text.split("\n")
#     if line.strip()
# ]

# st.divider()

# # -------------------------
# # Run Gate
# # -------------------------
# if st.button("🚦 Run Requirements Quality Gate", type="primary"):

#     if not description:
#         st.error("Description is required.")
#     else:
#         payload = {
#             "id": req_id,
#             "title": title,
#             "description": description,
#             "acceptance_criteria": acceptance_criteria,
#             "nfrs": nfrs
#         }

#         with st.spinner("Running quality gate..."):
#             result = run_quality_gate(payload)

#         st.divider()

#         if result["decision"] == "PASS":
#             st.success(f"✅ PASS — Score {result['total_score']}/100")
#         else:
#             st.error(f"❌ FAIL — Score {result['total_score']}/100")

#         st.subheader("📊 Score Breakdown")
#         st.json(result["scores"])

#         st.subheader("📝 AI Feedback")
#         st.json(result["feedback"])

#         st.subheader("📦 Final JSON Output")
#         st.json(result)

import streamlit as st
import hashlib

from main import run_quality_gate
from utils.file_parser import extract_text_from_file
from extractors.requirement_extractor import extract_requirements
from utils.json_utils import extract_json_object


# -------------------------
# Helpers
# -------------------------
def file_hash(uploaded_file):
    uploaded_file.seek(0)
    data = uploaded_file.getvalue()
    uploaded_file.seek(0)
    return hashlib.md5(data).hexdigest()


def reset_form_state():
    st.session_state.update({
        "req_id": "",
        "title": "",
        "description": "",
        "acceptance_criteria": "",
        "nfrs": "",
    })


def populate_form(data: dict):
    st.session_state.update({
        "req_id": data.get("id", ""),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "acceptance_criteria": "\n".join(data.get("acceptance_criteria", [])),
        "nfrs": "\n".join(data.get("nfrs", [])),
    })


# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Requirements Quality Gate",
    layout="centered"
)

st.title("🧠 Requirements Quality Gate AI")
st.caption("Manual input or AI-extracted from uploaded requirements")
st.divider()


# -------------------------
# Session State Init
# -------------------------
defaults = {
    "last_file_hash": None,
    "req_id": "FR-01",
    "title": "",
    "description": "",
    "acceptance_criteria": "",
    "nfrs": "",
    "extracted_data": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# -------------------------
# Upload Section
# -------------------------
st.subheader("📤 Upload Requirements File (Optional)")

uploaded_file = st.file_uploader(
    "Upload TXT, DOCX, or PDF",
    type=["txt", "docx", "pdf"]
)

if uploaded_file:
    current_hash = file_hash(uploaded_file)

    if current_hash != st.session_state.last_file_hash:
        st.session_state.last_file_hash = current_hash

        with st.spinner("Extracting requirements using AI..."):
            raw_text = extract_text_from_file(uploaded_file)
            raw_json = extract_requirements(raw_text)
            extracted = extract_json_object(raw_json)

            reset_form_state()
            populate_form(extracted)

            st.session_state.extracted_data = extracted

        st.success("✅ Requirements extracted successfully")
        st.experimental_set_query_params(refresh="true")
        #st.rerun()   # 🔑 FORCE UI REFRESH


# -------------------------
# Display Extracted JSON
# -------------------------
if st.session_state.extracted_data:
    st.subheader("📦 Extracted Requirement JSON")
    st.json(st.session_state.extracted_data)


st.divider()


# -------------------------
# Editable Requirement Form
# -------------------------
st.subheader("✏️ Requirement Details")

st.text_input("Requirement ID", key="req_id")
st.text_input("Title", key="title")

st.text_area(
    "Description / User Story",
    key="description",
    height=120
)

st.subheader("📋 Acceptance Criteria")

st.text_area(
    "Acceptance Criteria (one per line)",
    key="acceptance_criteria",
    height=120
)

acceptance_criteria = [
    line.strip()
    for line in st.session_state.acceptance_criteria.split("\n")
    if line.strip()
]

st.subheader("⚙️ Non-Functional Requirements (NFRs)")

st.text_area(
    "NFRs (one per line)",
    key="nfrs",
    height=120
)

nfrs = [
    line.strip()
    for line in st.session_state.nfrs.split("\n")
    if line.strip()
]


st.divider()


# -------------------------
# Run Quality Gate
# -------------------------
if st.button("🚦 Run Requirements Quality Gate", type="primary"):

    if not st.session_state.description:
        st.error("❗ Description is required")
    else:
        payload = {
            "id": st.session_state.req_id,
            "title": st.session_state.title,
            "description": st.session_state.description,
            "acceptance_criteria": acceptance_criteria,
            "nfrs": nfrs,
        }

        with st.spinner("Running quality gate..."):
            result = run_quality_gate(payload)

        st.divider()

        if result["decision"] == "PASS":
            st.success(f"✅ PASS — Score {result['total_score']}/100")
        else:
            st.error(f"❌ FAIL — Score {result['total_score']}/100")

        st.subheader("📊 Score Breakdown")
        st.json(result["scores"])

        st.subheader("📝 AI Feedback")
        st.json(result["feedback"])

        st.subheader("📦 Final JSON Output")
        st.json(result)
