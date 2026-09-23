import streamlit as st

st.set_page_config(
    page_title="RAD-ROUTE",
    page_icon="🩻",
    layout="centered"
)

FACILITY_RESOURCES = {
    "Facility A": ["X-ray"],
    "Facility B": ["X-ray", "CT", "Ultrasound",],
    "Facility C": ["X-ray", "MRI", "Mammography", "Nuclear Medicine"],
}

st.title("RAD-ROUTE")
st.subheader("Resource-Aware AI-Assisted Imaging Referral & Routing")

st.info(
    "Demonstration prototype — synthetic cases only.\n\n"
    "RAD-ROUTE supports healthcare professionals by checking referral "
    "completeness and matching imaging requirements with configured "
    "facility capabilities.\n\n"
    "AI-assisted decision support — professional approval required."
)

st.header("1. Referral Information")

age = st.number_input(
    "Patient Age",
    min_value=0,
    max_value=120,
    value=64
)

indication = st.text_input(
    "Clinical Indication",
    value="Sudden neurological symptoms"
)

clinical_question = st.text_input(
    "Clinical Question",
    value="Assess for acute intracranial abnormality"
)

imaging = st.selectbox(
    "Requested Imaging",
    ["X-ray", "CT", "MRI", "Nuclear Medicine", "Ultrasound", "Mammography"]
)

facility = st.selectbox(
    "Referring Facility",
    ["Facility A", "Facility B", "Facility C"]
)

urgency = st.selectbox(
    "Urgency",
    ["Routine", "Urgent", "Emergency"]
)

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "decision" not in st.session_state:
    st.session_state.decision = None

if st.button("Analyze Referral", type="primary"):

    missing = []

    if not indication.strip():
        missing.append("Clinical indication")

    if not clinical_question.strip():
        missing.append("Clinical question")

    if not imaging:
        missing.append("Requested imaging")

    if missing:
        readiness = "INCOMPLETE REFERRAL"
        information = "Missing: " + ", ".join(missing)
        routing = "Complete the missing referral information before routing."

    else:
        readiness = "READY FOR REVIEW"
        information = "No essential referral information identified as missing."

        if imaging in FACILITY_RESOURCES[facility]:
            routing = (
                f"{facility} has {imaging} capability.\n\n"
                "Referral can proceed to professional review."
            )
        else:
            alternatives = [
                name for name, resources in FACILITY_RESOURCES.items()
                if imaging in resources
            ]

            if alternatives:
                suggested = alternatives[0]
                routing = (
                    f"⚠️ {facility} does not have {imaging} capability.\n\n"
                    f"Suggested pathway: {suggested}\n\n"
                    "AI-assisted recommendation — professional review required."
                )
            else:
                routing = (
                    f"⚠️ {facility} does not have {imaging} capability.\n\n"
                    "No configured alternative facility was identified.\n\n"
                    "AI-assisted recommendation — professional review required."
                )

    st.session_state.analysis = {
        "readiness": readiness,
        "information": information,
        "routing": routing,
        "age": age,
        "indication": indication,
        "clinical_question": clinical_question,
        "imaging": imaging,
        "facility": facility,
        "urgency": urgency,
    }

    st.session_state.decision = None


if st.session_state.analysis:

    result = st.session_state.analysis

    st.header("2. RAD-ROUTE Analysis")

    st.write("**Referral Readiness**")
    st.success(result["readiness"])

    st.write("**Information Check**")
    st.write(result["information"])

    st.write("**Resource-Aware Routing**")
    st.warning(result["routing"])

    st.header("3. Professional Review")

    decision = st.radio(
        "Professional decision",
        ["Approved", "Edit / Do Not Approve"]
    )

    if st.button("Generate Structured Referral"):

        if decision == "Approved":

            st.session_state.decision = "APPROVED"

            structured = f"""
RAD-ROUTE STRUCTURED REFERRAL
=============================

Patient age: {result["age"]}
Clinical indication: {result["indication"]}
Clinical question: {result["clinical_question"]}
Requested imaging: {result["imaging"]}
Urgency: {result["urgency"]}
Referring facility: {result["facility"]}

RAD-ROUTE resource assessment:
{result["routing"]}

AI-assisted recommendation — professional review required.

Professional decision:
APPROVED

Status:
READY FOR TRANSFER TO EXISTING REFERRAL WORKFLOW

Note:
RAD-ROUTE is an AI-assisted decision-support prototype.
Final clinical responsibility remains with the authorized healthcare professional.
"""

            st.header("Structured Referral Output")
            st.code(structured)

        else:
            st.warning(
                "Referral not approved. The professional should edit or "
                "review the referral before proceeding."
            )

st.caption(
    "RAD-ROUTE is an AI-assisted decision-support prototype. "
    "Final clinical responsibility remains with the authorized healthcare professional."
)