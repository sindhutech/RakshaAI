import pandas as pd

# Load raw CSV
df = pd.read_csv("hospital_raw.csv")

# Remove repeated headers
df = df[df["Hospital Name"] != "Hospital Name"]

# Remove empty rows
df = df.dropna(subset=["Hospital Name"])

# Keep only needed columns
df = df[[
    "Hospital Name",
    "District",
    "Address",
    "Phone No",
    "Mail-ID",
    "Scheme",
    "Speciality"
]]

# Save cleaned dataset
df.to_csv("hospital_data.csv", index=False)

print("Dataset cleaned successfully!")