import streamlit as st
import hashlib
import json
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
st.subheader("📤 Upload Requirements File")

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
    result=st.json(st.session_state.extracted_data)
    # st.subheader("📦 Final JSON Output")
    # st.json(result)
    if result:
        st.subheader("📥 Download Final JSON Output")
        json_data = json.dumps(st.session_state.extracted_data, indent=4)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="requirements_quality_gate_result.json",
            mime="application/json"
        )

        st.subheader("📋 Copy JSON to Clipboard")
        st.code(json_data, language="json")

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
