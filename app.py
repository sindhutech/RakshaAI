import streamlit as st
import pandas as pd
from pypdf import PdfReader
from auth import authentication
import base64
import re

# -----------------------------
# BACKGROUND IMAGE
# -----------------------------

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}

        .block-container {{
            background-color: rgba(255,255,255,0.85);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("background.jpg")

# -----------------------------
# REPORT SUMMARIZER
# -----------------------------

def summarize_report(text):

    text = text.replace("\n", " ")

    patterns = {
        "Chief Complaint": r"(chief complaint[:\-]\s*)(.*?)(?=medical history|vital signs|clinical findings|diagnosis|treatment|$)",
        "Medical History": r"(medical history[:\-]\s*)(.*?)(?=vital signs|clinical findings|diagnosis|treatment|$)",
        "Vital Signs": r"(vital signs[:\-]\s*)(.*?)(?=clinical findings|diagnosis|treatment|$)",
        "Clinical Findings": r"(clinical findings[:\-]\s*)(.*?)(?=diagnosis|treatment|$)",
        "Diagnosis": r"(diagnosis[:\-]\s*)(.*?)(?=treatment|recommendation|$)",
        "Treatment": r"(treatment advice[:\-]\s*)(.*?)(?=$)"
    }

    summary = ""

    for section, pattern in patterns.items():

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            content = match.group(2).strip()
            summary += f"**{section}:** {content}\n\n"

    if summary == "":
        summary = text[:500]

    return summary

# -----------------------------
# AUTHENTICATION
# -----------------------------

if not authentication():
    st.warning("Please login to access RakshaAI")
    st.stop()

username = st.session_state.username

st.sidebar.write("Logged in as:", username)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -----------------------------
# LOAD DATASET
# -----------------------------

df = pd.read_csv("hospital_data.csv")

df = df.drop_duplicates(subset=["Hospital Name"])

df["District"] = (
    df["District"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

df["District"] = df["District"].replace({
    "BENGALU RU": "Bengaluru",
    "BENGALU": "Bengaluru",
    "BAGALKO TE": "Bagalkote"
})

df["District"] = df["District"].str.title()

df["Mail-ID"] = (
    df["Mail-ID"]
    .astype(str)
    .str.replace("\n", "")
    .str.replace(r"\s+", "", regex=True)
)

df["Speciality"] = (
    df["Speciality"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace(r"\s+", " ", regex=True)
)

df["Hospital Name"] = (
    df["Hospital Name"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace(r"\s+", " ", regex=True)
)

df["Address"] = (
    df["Address"]
    .astype(str)
    .str.replace("\n", " ")
    .str.replace(r"\s+", " ", regex=True)
)

# -----------------------------
# TITLE
# -----------------------------

st.title("RakshaAI - Emergency Healthcare Assistant")

st.write(
    "RakshaAI helps users analyze symptoms, determine emergency severity, "
    "recommend hospitals, store patient information, and track medical expenses."
)

# -----------------------------
# PATIENT DASHBOARD
# -----------------------------

st.header("Patient Dashboard")

patient_file = f"patients_{username}.csv"

default_name = ""
default_age = 0
default_gender = "Male"
default_blood = "A+"
default_allergies = ""
default_notes = ""

try:
    existing_patients = pd.read_csv(patient_file)
    last_patient = existing_patients.iloc[-1]

    default_name = last_patient["Name"]
    default_age = int(last_patient["Age"])
    default_gender = last_patient["Gender"]
    default_blood = last_patient["Blood Group"]
    default_allergies = last_patient["Allergies"]
    default_notes = last_patient["Notes"]

except:
    pass

name = st.text_input("Patient Name", value=default_name)
age = st.number_input("Age", 0, 120, value=default_age)

gender_options = ["Male", "Female", "Other"]
gender_index = gender_options.index(default_gender) if default_gender in gender_options else 0
gender = st.selectbox("Gender", gender_options, index=gender_index)

blood_options = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
blood_index = blood_options.index(default_blood) if default_blood in blood_options else 0
blood = st.selectbox("Blood Group", blood_options, index=blood_index)

allergies = st.text_area("Allergies", value=default_allergies)
notes = st.text_area("Medical Notes", value=default_notes)

if st.button("Save Patient Profile"):

    patient_data = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Blood Group": blood,
        "Allergies": allergies,
        "Notes": notes
    }

    patient_df = pd.DataFrame([patient_data])

    try:
        old = pd.read_csv(patient_file)
        patient_df = pd.concat([old, patient_df])
    except:
        pass

    patient_df.to_csv(patient_file, index=False)

    st.success("Patient profile saved!")

# -----------------------------
# SYMPTOM ANALYSIS
# -----------------------------

st.header("Symptom Analysis")

symptoms = st.text_input(
    "Enter symptoms (example: chest pain, fever, headache, kidney pain)"
)

district = st.selectbox(
    "Select your district",
    sorted(df["District"].dropna().unique())
)

if st.button("Analyze Symptoms"):

    symptoms_lower = symptoms.lower()

    if "chest" in symptoms_lower:
        severity = "HIGH"
        confidence = "88%"
        speciality = "CARDIO"
        advice = "Possible cardiac issue. Visit hospital immediately."

    elif "kidney" in symptoms_lower:
        severity = "HIGH"
        confidence = "85%"
        speciality = "UROLOGY"
        advice = "Possible kidney issue. Consult a urology specialist."

    elif "fever" in symptoms_lower:
        severity = "MEDIUM"
        confidence = "75%"
        speciality = "GENERAL"
        advice = "Monitor symptoms and consult doctor."

    else:
        severity = "LOW"
        confidence = "60%"
        speciality = ""
        advice = "Symptoms unclear. Consider visiting a general physician."

    st.subheader("AI Triage Result")

    if severity == "HIGH":
        st.error("⚠️ EMERGENCY: Seek immediate medical attention.")
    elif severity == "MEDIUM":
        st.warning("⚠️ Medical consultation recommended.")
    else:
        st.success("✅ Condition appears mild.")

    st.write("Severity Level:", severity)
    st.write("Confidence:", confidence)
    st.write("Advice:", advice)

    # -----------------------------
    # HOSPITAL RECOMMENDATION
    # -----------------------------

    st.subheader("Recommended Hospitals")

    district_hospitals = df[df["District"] == district]

    if speciality != "":
        speciality_hospitals = district_hospitals[
            district_hospitals["Speciality"].str.upper().str.contains(speciality, na=False)
        ]
    else:
        speciality_hospitals = district_hospitals

    display = speciality_hospitals.head(5) if not speciality_hospitals.empty else district_hospitals.head(5)

    for _, row in display.iterrows():

        email = row["Mail-ID"]

        if email == "nan":
            email = "Not Available"

        st.markdown(f"""
### 🏥 {row['Hospital Name']}

📍 **Address:** {row['Address']}

📞 **Phone:** {row['Phone No']}

📧 **Email:** {email}

💳 **Scheme:** {row['Scheme']}

🩺 **Speciality:** {row['Speciality']}
""")

# -----------------------------
# MEDICAL REPORT
# -----------------------------

st.header("Upload Medical Report")

uploaded_file = st.file_uploader(
    "Upload your medical report (PDF)", type="pdf"
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    st.subheader("AI Generated Report Summary")

    summary = summarize_report(text)

    st.write(summary)

# -----------------------------
# MEDICAL BUDGET & EXPENSE TRACKER
# -----------------------------

st.header("Medical Budget & Expense Tracker")

budget_file = f"budget_{username}.csv"
expense_file = f"expenses_{username}.csv"

try:
    budget_df = pd.read_csv(budget_file)
    initial_budget = int(budget_df["Budget"][0])
except:
    initial_budget = 0

if initial_budget == 0:

    st.subheader("Set Initial Medical Budget")

    new_budget = st.number_input("Enter Initial Budget (₹)", min_value=0)

    if st.button("Save Budget"):

        pd.DataFrame({"Budget":[new_budget]}).to_csv(budget_file,index=False)

        st.success("Budget saved!")

        st.rerun()

else:

    st.subheader(f"Initial Budget: ₹{initial_budget}")

treatment = st.text_input("Treatment / Medicine")
cost = st.number_input("Cost (₹)", min_value=0)

if st.button("Add Expense"):

    expense_data = {
        "Treatment": treatment,
        "Cost": cost
    }

    expense_df = pd.DataFrame([expense_data])

    try:
        old = pd.read_csv(expense_file)
        expense_df = pd.concat([old, expense_df])
    except:
        pass

    expense_df.to_csv(expense_file, index=False)

    st.success("Expense recorded!")

try:

    expenses = pd.read_csv(expense_file)

    st.subheader("Expense History")

    st.dataframe(expenses)

    total_spent = expenses["Cost"].sum()

    remaining = initial_budget - total_spent

    st.write(f"Total Spent: ₹{total_spent}")

    if remaining >= 0:
        st.success(f"Remaining Budget: ₹{remaining}")
    else:
        st.error(f"Budget Exceeded by ₹{abs(remaining)}")

except:
    st.info("No expenses recorded yet.")