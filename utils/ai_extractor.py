def ai_extract_parameters(report_text, client):
    prompt = f"""
You are a medical data extractor.

<<<<<<< HEAD
Extract all lab parameters and their values from the report below.

Return ONLY in JSON format like this:
{{
  "hemoglobin": 10,
  "wbc": 12000,
  "platelets": 150000
}}

Rules:
- Extract as many parameters as possible
- Use lowercase keys
- No explanation, only JSON

=======
Extract ALL lab parameters and their numeric values from the report below.

IMPORTANT RULES:
- For blood pressure, extract as TWO separate keys: "systolic" and "diastolic"
  e.g. BP 140/90 → {{"systolic": 140, "diastolic": 90}}
- For cholesterol, extract: "total cholesterol", "ldl", "hdl", "triglycerides" separately
- Use lowercase keys with spaces (not underscores)
- Extract EVERY parameter you can find — do not skip any
- Values must be numeric only (no units in the value)
- Return ONLY valid JSON, no explanation

Example output:
{{
  "hemoglobin": 10.5,
  "total cholesterol": 240,
  "ldl": 160,
  "hdl": 38,
  "triglycerides": 200,
  "systolic": 145,
  "diastolic": 95,
  "fasting glucose": 110,
  "creatinine": 1.4
}}

>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
Report:
{report_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

<<<<<<< HEAD
    return response.choices[0].message.content
=======
    return response.choices[0].message.content
>>>>>>> dba419a332508878fc47ed5bddc846ff792eabe6
