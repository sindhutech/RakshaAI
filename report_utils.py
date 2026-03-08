import re

def summarize_medical_report(text):

    text = text.replace("\n", " ")

    sections = {}

    patterns = {
        "Chief Complaint": r"(chief complaint[:\-]\s*)(.*?)(?=medical history|vital signs|clinical findings|diagnosis|treatment|$)",
        "Medical History": r"(medical history[:\-]\s*)(.*?)(?=vital signs|clinical findings|diagnosis|treatment|$)",
        "Diagnosis": r"(diagnosis[:\-]\s*)(.*?)(?=treatment|recommendation|$)",
        "Clinical Findings": r"(clinical findings[:\-]\s*)(.*?)(?=diagnosis|treatment|$)",
        "Vital Signs": r"(vital signs[:\-]\s*)(.*?)(?=clinical findings|diagnosis|$)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            sections[key] = match.group(2).strip()

    summary = ""

    if "Chief Complaint" in sections:
        summary += f"**Chief Complaint:** {sections['Chief Complaint']}\n\n"

    if "Medical History" in sections:
        summary += f"**Medical History:** {sections['Medical History']}\n\n"

    if "Vital Signs" in sections:
        summary += f"**Vital Signs:** {sections['Vital Signs']}\n\n"

    if "Clinical Findings" in sections:
        summary += f"**Clinical Findings:** {sections['Clinical Findings']}\n\n"

    if "Diagnosis" in sections:
        summary += f"**Diagnosis:** {sections['Diagnosis']}\n\n"

    if summary == "":
        summary = text[:500]

    return summary