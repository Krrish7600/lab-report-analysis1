PARAMETERS = {
    "hemoglobin":  {"min": 12,     "max": 16,     "unit": "g/dL",   "reference_range": "12 – 16 g/dL"},
    "wbc":         {"min": 4000,   "max": 11000,  "unit": "cells/µL","reference_range": "4,000 – 11,000"},
    "platelets":   {"min": 150000, "max": 450000, "unit": "cells/µL","reference_range": "150K – 450K"},
    "rbc":         {"min": 4.0,    "max": 6.0,    "unit": "M/µL",   "reference_range": "4.0 – 6.0 M/µL"},
    "glucose":     {"min": 70,     "max": 140,    "unit": "mg/dL",  "reference_range": "70 – 140 mg/dL"},
    "cholesterol": {"min": 0,      "max": 200,    "unit": "mg/dL",  "reference_range": "< 200 mg/dL"},
    "triglycerides":{"min": 0,     "max": 150,    "unit": "mg/dL",  "reference_range": "< 150 mg/dL"},
    "creatinine":  {"min": 0.6,    "max": 1.2,    "unit": "mg/dL",  "reference_range": "0.6 – 1.2 mg/dL"},
    "urea":        {"min": 7,      "max": 20,     "unit": "mg/dL",  "reference_range": "7 – 20 mg/dL"},
    "sodium":      {"min": 136,    "max": 145,    "unit": "mEq/L",  "reference_range": "136 – 145 mEq/L"},
    "potassium":   {"min": 3.5,    "max": 5.0,    "unit": "mEq/L",  "reference_range": "3.5 – 5.0 mEq/L"},
    "calcium":     {"min": 8.5,    "max": 10.5,   "unit": "mg/dL",  "reference_range": "8.5 – 10.5 mg/dL"},
    "bilirubin":   {"min": 0.1,    "max": 1.2,    "unit": "mg/dL",  "reference_range": "0.1 – 1.2 mg/dL"},
    "alt":         {"min": 7,      "max": 56,     "unit": "U/L",    "reference_range": "7 – 56 U/L"},
    "ast":         {"min": 10,     "max": 40,     "unit": "U/L",    "reference_range": "10 – 40 U/L"},
    "hba1c":       {"min": 0,      "max": 5.7,    "unit": "%",      "reference_range": "< 5.7%"},
    "tsh":         {"min": 0.4,    "max": 4.0,    "unit": "mIU/L",  "reference_range": "0.4 – 4.0 mIU/L"},
    "vitamin_d":   {"min": 20,     "max": 100,    "unit": "ng/mL",  "reference_range": "20 – 100 ng/mL"},
    "vitamin_b12": {"min": 200,    "max": 900,    "unit": "pg/mL",  "reference_range": "200 – 900 pg/mL"},
    "iron":        {"min": 60,     "max": 170,    "unit": "µg/dL",  "reference_range": "60 – 170 µg/dL"},
}

# Key metrics to highlight as cards in the dashboard
KEY_METRICS = ["hemoglobin", "glucose", "wbc", "platelets", "cholesterol", "hba1c", "creatinine", "tsh"]

def analyze_report(data):
    result = {}

    for param, value in data.items():
        key = param.lower().replace(" ", "_")
        if key in PARAMETERS:
            meta    = PARAMETERS[key]
            min_val = meta["min"]
            max_val = meta["max"]

            if value < min_val:
                status = "low"
            elif value > max_val:
                status = "high"
            else:
                status = "normal"

            result[key] = {
                "value":           value,
                "unit":            meta["unit"],
                "reference_range": meta["reference_range"],
                "status":          status,
            }
        else:
            # Unknown parameter — store as-is without range check
            result[key] = {
                "value":           value,
                "unit":            "",
                "reference_range": "—",
                "status":          "normal",
            }

    return result
