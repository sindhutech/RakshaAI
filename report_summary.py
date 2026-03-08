def generate_summary(text):

    text_lower = text.lower()

    summary_points = []

    if "chest pain" in text_lower:
        summary_points.append("Patient reports chest pain.")

    if "breathing" in text_lower:
        summary_points.append("Breathing discomfort detected.")

    if "kidney" in text_lower:
        summary_points.append("History of kidney-related condition mentioned.")

    if "irregular heartbeat" in text_lower:
        summary_points.append("ECG indicates irregular heartbeat.")

    if "cholesterol" in text_lower:
        summary_points.append("Blood tests show elevated cholesterol levels.")

    if "blood pressure" in text_lower:
        summary_points.append("Blood pressure readings detected in report.")

    if len(summary_points) == 0:
        summary_points.append("General medical report information detected.")

    if "heart" in text_lower or "cardiac" in text_lower:
        recommendation = "Recommendation: Consult a cardiologist immediately."

    elif "kidney" in text_lower:
        recommendation = "Recommendation: Consult a urology specialist."

    else:
        recommendation = "Recommendation: Consult a general physician."

    summary = "\n".join(summary_points)

    return summary + "\n\n" + recommendation