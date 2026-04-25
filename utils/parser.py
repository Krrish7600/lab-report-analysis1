# All keys are lowercase with spaces (no underscores) to match AI extractor output
PARAMETERS = {
    # ── CBC ──────────────────────────────────────────────────────────────────
    "hemoglobin":               {"min": 12.0,   "max": 17.5,   "unit": "g/dL",     "reference_range": "12 – 17.5 g/dL"},
    "hgb":                      {"min": 12.0,   "max": 17.5,   "unit": "g/dL",     "reference_range": "12 – 17.5 g/dL"},
    "wbc":                      {"min": 4000,   "max": 11000,  "unit": "cells/µL", "reference_range": "4,000 – 11,000"},
    "white blood cells":        {"min": 4000,   "max": 11000,  "unit": "cells/µL", "reference_range": "4,000 – 11,000"},
    "platelets":                {"min": 150000, "max": 450000, "unit": "cells/µL", "reference_range": "150K – 450K"},
    "platelet count":           {"min": 150000, "max": 450000, "unit": "cells/µL", "reference_range": "150K – 450K"},
    "rbc":                      {"min": 4.0,    "max": 6.0,    "unit": "M/µL",     "reference_range": "4.0 – 6.0 M/µL"},
    "red blood cells":          {"min": 4.0,    "max": 6.0,    "unit": "M/µL",     "reference_range": "4.0 – 6.0 M/µL"},
    "hematocrit":               {"min": 36.0,   "max": 52.0,   "unit": "%",        "reference_range": "36 – 52%"},
    "hct":                      {"min": 36.0,   "max": 52.0,   "unit": "%",        "reference_range": "36 – 52%"},
    "mcv":                      {"min": 80.0,   "max": 100.0,  "unit": "fL",       "reference_range": "80 – 100 fL"},
    "mch":                      {"min": 27.0,   "max": 33.0,   "unit": "pg",       "reference_range": "27 – 33 pg"},
    "mchc":                     {"min": 32.0,   "max": 36.0,   "unit": "g/dL",     "reference_range": "32 – 36 g/dL"},
    "rdw":                      {"min": 11.5,   "max": 14.5,   "unit": "%",        "reference_range": "11.5 – 14.5%"},
    "neutrophils":              {"min": 40.0,   "max": 75.0,   "unit": "%",        "reference_range": "40 – 75%"},
    "lymphocytes":              {"min": 20.0,   "max": 45.0,   "unit": "%",        "reference_range": "20 – 45%"},
    "monocytes":                {"min": 2.0,    "max": 10.0,   "unit": "%",        "reference_range": "2 – 10%"},
    "eosinophils":              {"min": 1.0,    "max": 6.0,    "unit": "%",        "reference_range": "1 – 6%"},
    "basophils":                {"min": 0.0,    "max": 1.0,    "unit": "%",        "reference_range": "0 – 1%"},

    # ── Blood Glucose ─────────────────────────────────────────────────────────
    "glucose":                  {"min": 70,     "max": 100,    "unit": "mg/dL",    "reference_range": "70 – 100 mg/dL"},
    "fasting glucose":          {"min": 70,     "max": 100,    "unit": "mg/dL",    "reference_range": "70 – 100 mg/dL"},
    "fasting blood sugar":      {"min": 70,     "max": 100,    "unit": "mg/dL",    "reference_range": "70 – 100 mg/dL"},
    "fbs":                      {"min": 70,     "max": 100,    "unit": "mg/dL",    "reference_range": "70 – 100 mg/dL"},
    "blood sugar":              {"min": 70,     "max": 100,    "unit": "mg/dL",    "reference_range": "70 – 100 mg/dL"},
    "random blood sugar":       {"min": 70,     "max": 140,    "unit": "mg/dL",    "reference_range": "70 – 140 mg/dL"},
    "rbs":                      {"min": 70,     "max": 140,    "unit": "mg/dL",    "reference_range": "70 – 140 mg/dL"},
    "postprandial glucose":     {"min": 70,     "max": 140,    "unit": "mg/dL",    "reference_range": "70 – 140 mg/dL"},
    "hba1c":                    {"min": 4.0,    "max": 5.7,    "unit": "%",        "reference_range": "< 5.7%"},
    "glycated hemoglobin":      {"min": 4.0,    "max": 5.7,    "unit": "%",        "reference_range": "< 5.7%"},

    # ── Lipid Profile ─────────────────────────────────────────────────────────
    "total cholesterol":        {"min": 0,      "max": 200,    "unit": "mg/dL",    "reference_range": "< 200 mg/dL"},
    "cholesterol":              {"min": 0,      "max": 200,    "unit": "mg/dL",    "reference_range": "< 200 mg/dL"},
    "ldl":                      {"min": 0,      "max": 100,    "unit": "mg/dL",    "reference_range": "< 100 mg/dL"},
    "ldl cholesterol":          {"min": 0,      "max": 100,    "unit": "mg/dL",    "reference_range": "< 100 mg/dL"},
    "hdl":                      {"min": 40,     "max": 9999,   "unit": "mg/dL",    "reference_range": "> 40 mg/dL"},
    "hdl cholesterol":          {"min": 40,     "max": 9999,   "unit": "mg/dL",    "reference_range": "> 40 mg/dL"},
    "triglycerides":            {"min": 0,      "max": 150,    "unit": "mg/dL",    "reference_range": "< 150 mg/dL"},
    "vldl":                     {"min": 2,      "max": 30,     "unit": "mg/dL",    "reference_range": "2 – 30 mg/dL"},

    # ── Blood Pressure ────────────────────────────────────────────────────────
    "systolic":                 {"min": 90,     "max": 120,    "unit": "mmHg",     "reference_range": "90 – 120 mmHg"},
    "systolic bp":              {"min": 90,     "max": 120,    "unit": "mmHg",     "reference_range": "90 – 120 mmHg"},
    "diastolic":                {"min": 60,     "max": 80,     "unit": "mmHg",     "reference_range": "60 – 80 mmHg"},
    "diastolic bp":             {"min": 60,     "max": 80,     "unit": "mmHg",     "reference_range": "60 – 80 mmHg"},
    "blood pressure systolic":  {"min": 90,     "max": 120,    "unit": "mmHg",     "reference_range": "90 – 120 mmHg"},
    "blood pressure diastolic": {"min": 60,     "max": 80,     "unit": "mmHg",     "reference_range": "60 – 80 mmHg"},

    # ── Kidney Function ───────────────────────────────────────────────────────
    "creatinine":               {"min": 0.6,    "max": 1.2,    "unit": "mg/dL",    "reference_range": "0.6 – 1.2 mg/dL"},
    "serum creatinine":         {"min": 0.6,    "max": 1.2,    "unit": "mg/dL",    "reference_range": "0.6 – 1.2 mg/dL"},
    "bun":                      {"min": 7,      "max": 20,     "unit": "mg/dL",    "reference_range": "7 – 20 mg/dL"},
    "blood urea nitrogen":      {"min": 7,      "max": 20,     "unit": "mg/dL",    "reference_range": "7 – 20 mg/dL"},
    "urea":                     {"min": 15,     "max": 45,     "unit": "mg/dL",    "reference_range": "15 – 45 mg/dL"},
    "uric acid":                {"min": 3.5,    "max": 7.2,    "unit": "mg/dL",    "reference_range": "3.5 – 7.2 mg/dL"},
    "egfr":                     {"min": 60,     "max": 9999,   "unit": "mL/min",   "reference_range": "> 60 mL/min"},

    # ── Liver Function ────────────────────────────────────────────────────────
    "alt":                      {"min": 7,      "max": 56,     "unit": "U/L",      "reference_range": "7 – 56 U/L"},
    "sgpt":                     {"min": 7,      "max": 56,     "unit": "U/L",      "reference_range": "7 – 56 U/L"},
    "ast":                      {"min": 10,     "max": 40,     "unit": "U/L",      "reference_range": "10 – 40 U/L"},
    "sgot":                     {"min": 10,     "max": 40,     "unit": "U/L",      "reference_range": "10 – 40 U/L"},
    "alkaline phosphatase":     {"min": 44,     "max": 147,    "unit": "U/L",      "reference_range": "44 – 147 U/L"},
    "alp":                      {"min": 44,     "max": 147,    "unit": "U/L",      "reference_range": "44 – 147 U/L"},
    "bilirubin":                {"min": 0.1,    "max": 1.2,    "unit": "mg/dL",    "reference_range": "0.1 – 1.2 mg/dL"},
    "total bilirubin":          {"min": 0.1,    "max": 1.2,    "unit": "mg/dL",    "reference_range": "0.1 – 1.2 mg/dL"},
    "direct bilirubin":         {"min": 0.0,    "max": 0.3,    "unit": "mg/dL",    "reference_range": "0 – 0.3 mg/dL"},
    "albumin":                  {"min": 3.5,    "max": 5.0,    "unit": "g/dL",     "reference_range": "3.5 – 5.0 g/dL"},
    "total protein":            {"min": 6.0,    "max": 8.3,    "unit": "g/dL",     "reference_range": "6.0 – 8.3 g/dL"},
    "ggt":                      {"min": 9,      "max": 48,     "unit": "U/L",      "reference_range": "9 – 48 U/L"},

    # ── Thyroid ───────────────────────────────────────────────────────────────
    "tsh":                      {"min": 0.4,    "max": 4.0,    "unit": "mIU/L",    "reference_range": "0.4 – 4.0 mIU/L"},
    "t3":                       {"min": 80,     "max": 200,    "unit": "ng/dL",    "reference_range": "80 – 200 ng/dL"},
    "t4":                       {"min": 5.0,    "max": 12.0,   "unit": "µg/dL",    "reference_range": "5.0 – 12.0 µg/dL"},
    "free t3":                  {"min": 2.3,    "max": 4.2,    "unit": "pg/mL",    "reference_range": "2.3 – 4.2 pg/mL"},
    "free t4":                  {"min": 0.8,    "max": 1.8,    "unit": "ng/dL",    "reference_range": "0.8 – 1.8 ng/dL"},

    # ── Electrolytes ──────────────────────────────────────────────────────────
    "sodium":                   {"min": 136,    "max": 145,    "unit": "mEq/L",    "reference_range": "136 – 145 mEq/L"},
    "potassium":                {"min": 3.5,    "max": 5.0,    "unit": "mEq/L",    "reference_range": "3.5 – 5.0 mEq/L"},
    "chloride":                 {"min": 98,     "max": 107,    "unit": "mEq/L",    "reference_range": "98 – 107 mEq/L"},
    "calcium":                  {"min": 8.5,    "max": 10.5,   "unit": "mg/dL",    "reference_range": "8.5 – 10.5 mg/dL"},
    "magnesium":                {"min": 1.7,    "max": 2.2,    "unit": "mg/dL",    "reference_range": "1.7 – 2.2 mg/dL"},
    "phosphorus":               {"min": 2.5,    "max": 4.5,    "unit": "mg/dL",    "reference_range": "2.5 – 4.5 mg/dL"},
    "bicarbonate":              {"min": 22,     "max": 29,     "unit": "mEq/L",    "reference_range": "22 – 29 mEq/L"},

    # ── Iron Studies ──────────────────────────────────────────────────────────
    "iron":                     {"min": 60,     "max": 170,    "unit": "µg/dL",    "reference_range": "60 – 170 µg/dL"},
    "serum iron":               {"min": 60,     "max": 170,    "unit": "µg/dL",    "reference_range": "60 – 170 µg/dL"},
    "ferritin":                 {"min": 12,     "max": 300,    "unit": "ng/mL",    "reference_range": "12 – 300 ng/mL"},
    "tibc":                     {"min": 250,    "max": 370,    "unit": "µg/dL",    "reference_range": "250 – 370 µg/dL"},
    "transferrin saturation":   {"min": 20,     "max": 50,     "unit": "%",        "reference_range": "20 – 50%"},

    # ── Vitamins ──────────────────────────────────────────────────────────────
    "vitamin d":                {"min": 30,     "max": 100,    "unit": "ng/mL",    "reference_range": "30 – 100 ng/mL"},
    "vitamin b12":              {"min": 200,    "max": 900,    "unit": "pg/mL",    "reference_range": "200 – 900 pg/mL"},
    "folate":                   {"min": 2.7,    "max": 17.0,   "unit": "ng/mL",    "reference_range": "2.7 – 17.0 ng/mL"},

    # ── Cardiac ───────────────────────────────────────────────────────────────
    "troponin":                 {"min": 0,      "max": 0.04,   "unit": "ng/mL",    "reference_range": "< 0.04 ng/mL"},
    "creatine kinase":          {"min": 22,     "max": 198,    "unit": "U/L",      "reference_range": "22 – 198 U/L"},
    "ck":                       {"min": 22,     "max": 198,    "unit": "U/L",      "reference_range": "22 – 198 U/L"},
    "ck-mb":                    {"min": 0,      "max": 25,     "unit": "U/L",      "reference_range": "< 25 U/L"},
    "bnp":                      {"min": 0,      "max": 100,    "unit": "pg/mL",    "reference_range": "< 100 pg/mL"},

    # ── Inflammation ──────────────────────────────────────────────────────────
    "crp":                      {"min": 0,      "max": 1.0,    "unit": "mg/dL",    "reference_range": "< 1.0 mg/dL"},
    "c-reactive protein":       {"min": 0,      "max": 1.0,    "unit": "mg/dL",    "reference_range": "< 1.0 mg/dL"},
    "esr":                      {"min": 0,      "max": 20,     "unit": "mm/hr",    "reference_range": "0 – 20 mm/hr"},

    # ── Coagulation ───────────────────────────────────────────────────────────
    "pt":                       {"min": 11,     "max": 13.5,   "unit": "seconds",  "reference_range": "11 – 13.5 sec"},
    "inr":                      {"min": 0.8,    "max": 1.1,    "unit": "",         "reference_range": "0.8 – 1.1"},
    "aptt":                     {"min": 25,     "max": 35,     "unit": "seconds",  "reference_range": "25 – 35 sec"},
    "ptt":                      {"min": 25,     "max": 35,     "unit": "seconds",  "reference_range": "25 – 35 sec"},
}

# Key metrics shown as highlight cards in the dashboard
KEY_METRICS = [
    "hemoglobin", "glucose", "wbc", "platelets",
    "total cholesterol", "cholesterol", "hba1c",
    "creatinine", "tsh", "systolic", "diastolic",
    "ldl", "hdl", "triglycerides"
]


def _normalise(key: str) -> str:
    """Lowercase + strip only — preserve spaces so keys match PARAMETERS."""
    return key.strip().lower()


def _find_ref(key: str):
    """Exact match first, then substring fallback."""
    if key in PARAMETERS:
        return PARAMETERS[key]
    for pkey in PARAMETERS:
        if pkey in key or key in pkey:
            return PARAMETERS[pkey]
    return None


def analyze_report(data: dict) -> dict:
    result = {}

    for raw_key, value in data.items():
        key = _normalise(raw_key)
        ref = _find_ref(key)

        try:
            numeric = float(value)
        except (TypeError, ValueError):
            result[raw_key] = {"value": value, "unit": "", "reference_range": "—", "status": "unrecognized"}
            continue

        if ref is None:
            # Unknown parameter — flag as unrecognized, do NOT default to normal
            result[raw_key] = {"value": numeric, "unit": "", "reference_range": "—", "status": "unrecognized"}
            continue

        if numeric < ref["min"]:
            status = "low"
        elif numeric > ref["max"]:
            status = "high"
        else:
            status = "normal"

        result[raw_key] = {
            "value":           numeric,
            "unit":            ref["unit"],
            "reference_range": ref["reference_range"],
            "status":          status,
        }

    return result
