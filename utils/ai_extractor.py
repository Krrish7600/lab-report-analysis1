def ai_extract_parameters(report_text, client):
    prompt = f"""
You are a medical data extractor.

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

Report:
{report_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content